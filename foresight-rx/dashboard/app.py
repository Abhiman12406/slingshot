import streamlit as st
import time
import pandas as pd
import sys
import os

# Add root project dir to path to find src
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.monitoring.system_metrics import MockTelemetryGenerator
from src.features.feature_extractor import FeatureExtractor
from src.detection.threat_scorer import ThreatScorer
import yaml

# Page Config
st.set_page_config(page_title="Foresight-RX | Anti-Ransomware", layout="wide", page_icon="🛡️")

@st.cache_resource
def load_core_components():
    config_path = os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml")
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    gen = MockTelemetryGenerator(config_path)
    extractor = FeatureExtractor(config["features"]["vector_size"])
    scorer = ThreatScorer()
    return gen, extractor, scorer

gen, extractor, scorer = load_core_components()

# UI Layout
st.title("Foresight-RX: Real-Time Ransomware Prediction")
st.markdown("Powered by PyTorch Autoencoders & AMD ROCm Architecture")

# Top Metrics Row
metrics_cols = st.columns(4)
sys_status_col = metrics_cols[0]
score_col = metrics_cols[1]
writes_col = metrics_cols[2]
cpu_col = metrics_cols[3]

# Charts
st.subheader("Live Telemetry")
chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    st.write("Anomaly Score Trend")
    score_chart_placeholder = st.empty()
with chart_col2:
    st.write("File Writes / Sec (Burst Indicator)")
    writes_chart_placeholder = st.empty()
    
# Control Panel
st.sidebar.header("Simulator Controls")
if st.sidebar.button("Trigger Ransomware Attack", type="primary"):
    gen.trigger_attack()
    st.sidebar.warning("Attack simulation started!")
    
if st.sidebar.button("Reset Normal State"):
    gen.reset_state()
    st.sidebar.success("System returned to normal.")

# Real-time state management
if "history_scores" not in st.session_state:
    st.session_state.history_scores = []
if "history_writes" not in st.session_state:
    st.session_state.history_writes = []

def ui_loop():
    while True:
        # 1. Get raw metrics
        raw_metrics = gen.get_latest_metrics()
        
        # 2. Extract Features
        feature_vec = extractor.process_telemetry(raw_metrics)
        
        # 3. AI Prediction Inference
        anomaly_score = scorer.compute_anomaly_score(feature_vec)
        risk_level = scorer.get_risk_level(anomaly_score)
        
        # 4. Update History
        st.session_state.history_scores.append(anomaly_score)
        st.session_state.history_writes.append(raw_metrics["writes_per_sec"])
        
        if len(st.session_state.history_scores) > 50:
            st.session_state.history_scores.pop(0)
            st.session_state.history_writes.pop(0)
            
        # 5. UI Updates
        color = "red" if risk_level == "Ransomware Likely" else ("orange" if risk_level == "Suspicious" else "green")
        sys_status_col.metric("System Status", risk_level, delta_color="inverse")
        score_col.metric("AI Anomaly Score", f"{anomaly_score:.2f}", delta=f"Risk: {risk_level}", delta_color="off" if risk_level=="Safe" else "inverse")
        writes_col.metric("File Writes", f"{raw_metrics['writes_per_sec']:.1f} /s")
        cpu_col.metric("CPU Spikes", f"{raw_metrics['cpu_spike']:.1f}%")
        
        if risk_level == "Ransomware Likely":
            st.error("⚠️ CRITICAL THREAT DETECTED: Anomalous file encryption pattern (Ransomware precursor) identified!")
        
        # Update Charts
        score_df = pd.DataFrame(st.session_state.history_scores, columns=["Anomaly Score"])
        score_chart_placeholder.line_chart(score_df, color="#FF4B4B")
        
        writes_df = pd.DataFrame(st.session_state.history_writes, columns=["Writes/Sec"])
        writes_chart_placeholder.line_chart(writes_df, color="#0068C9")
        
        time.sleep(1) # Poll interval
        st.rerun()

# Run the UI loop if not initialized
ui_loop()
