from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import sys
import os
import uvicorn
from pydantic import BaseModel
import asyncio
import yaml

# Add root project dir to path to find src
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.monitoring.process_monitor import ProcessMonitor
from src.monitoring.file_monitor import FileMonitor
from src.features.feature_extractor import FeatureExtractor
from src.detection.threat_scorer import ThreatScorer
import time

app = FastAPI(title="Foresight-RX API")

# Setup CORS for the React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"], # Secured from wildcard
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global State
class EngineState:
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml")
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
            
        dummy_dir = os.path.join(os.path.dirname(__file__), "..", "data", "samples", "dummy_files")
        # We still need the simulator just for the trigger attack button
        sys.path.append(os.path.join(os.path.dirname(__file__), "..", "simulator"))
        from ransomware_simulator import RansomwareSimulator
        self.simulator = RansomwareSimulator()
        self.simulator.setup_normal_state() # Initialize files before OS monitoring begins
        
        self.proc_monitor = ProcessMonitor(self.config["monitoring"]["rolling_window_sec"])
        self.file_monitor = FileMonitor(target_dir=dummy_dir)
        self.file_monitor.start() # Start watchdog background thread
        
        self.extractor = FeatureExtractor(self.config["features"]["vector_size"])
        self.scorer = ThreatScorer()
        self.history_scores = []
        self.history_writes = []
        self.history_timestamps = []
        
    def __del__(self):
        if hasattr(self, 'file_monitor'):
            self.file_monitor.stop()

state = EngineState()

def background_monitoring_loop():
    """Runs continuously to process telemetry and keep history updated."""
    pass # In a real background loop, we could do this async. For MVP polling is fine.

@app.get("/api/metrics")
async def get_metrics():
    # 1. Get real OS metrics from monitors
    proc_metrics = state.proc_monitor.poll()
    file_metrics = state.file_monitor.poll()
    
    # Merge for the feature extractor
    # Note: Entropy delta requires more advanced state tracking of modified files which
    # isn't fully wired in this MVP polling loop, so we'll simulate a mock mapping for the autoencoder.
    # In a full system, you would calculate entropy of the specific `event.src_path` hooked from watchdog.
    raw_metrics = {
        "timestamp": time.time(),
        "writes_per_sec": file_metrics["writes"], # Assuming ~1s poll
        "renames_per_sec": file_metrics["renames"],
        "entropy_delta": 0.8 if file_metrics["renames"] > 5 else 0.05, # Proxy for MVP Demo Visuals
        "unique_exts": file_metrics["unique_exts_count"],
        "burst_score": proc_metrics["burst_score"],
        "cpu_spike": proc_metrics["cpu_spike"]
    }
    
    # 2. Extract Features
    feature_vec = state.extractor.process_telemetry(raw_metrics)
    
    # 3. AI Prediction Inference
    anomaly_score = state.scorer.compute_anomaly_score(feature_vec)
    risk_level = state.scorer.get_risk_level(anomaly_score)
    
    # 4. Update History
    state.history_scores.append(anomaly_score)
    state.history_writes.append(raw_metrics["writes_per_sec"])
    state.history_timestamps.append(raw_metrics["timestamp"])
    
    if len(state.history_scores) > 50:
        state.history_scores.pop(0)
        state.history_writes.pop(0)
        state.history_timestamps.pop(0)
        
    return {
        "status": risk_level,
        "anomaly_score": round(anomaly_score, 4),
        "writes_per_sec": round(raw_metrics["writes_per_sec"], 2),
        "cpu_spike": round(raw_metrics["cpu_spike"], 2),
        "history": {
            "scores": state.history_scores,
            "writes": state.history_writes,
            "timestamps": state.history_timestamps
        }
    }

@app.post("/api/trigger")
async def trigger_attack(background_tasks: BackgroundTasks):
    background_tasks.add_task(state.simulator.trigger_attack)
    return {"message": "Attack triggered successfully"}

@app.post("/api/reset")
async def reset_state():
    state.file_monitor.pause()
    state.simulator.reset()
    await asyncio.sleep(0.5) # Allow any pending valid OS events to drain
    state.proc_monitor.reset()
    state.file_monitor.reset()
    state.file_monitor.resume()
    # Also reset history for cleaner graphs
    state.history_scores = []
    state.history_writes = []
    state.history_timestamps = []
    return {"message": "System reset successfully"}

# Mount the static React UI
ui_dir = os.path.join(os.path.dirname(__file__), "ui")
if os.path.exists(ui_dir):
    app.mount("/", StaticFiles(directory=ui_dir, html=True), name="ui")
else:
    @app.get("/")
    async def root():
        return RedirectResponse(url="/docs")

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
