# Foresight-RX: AI-Driven Early Ransomware Prediction

Foresight-RX is a real-time, AI-powered endpoint security system designed to predict and detect ransomware attacks **before mass file encryption occurs**. By leveraging behavioral monitoring and a PyTorch-based Deep Learning Autoencoder, Foresight-RX identifies ransomware precursors in real time, shifting the paradigm from reactive signature-matching to proactive behavioral anomaly detection.

## 🚀 Key Features

* **Real-Time Behavior Monitoring**: Continuously tracks OS-level telemetry including process creation rates, file write frequency, file renames, CPU spikes, and Shannon entropy delta without relying on static file scanning.
* **AI Anomaly Detection Engine**: Utilizes a Deep Learning Autoencoder to establish a "healthy baseline" of system behavior. When anomalous activity (like rapid high-entropy file encryption) occurs, the reconstruction error spikes, triggering an alert.
* **Low-Latency Inference**: Designed for high performance with hardware flexibility, supporting AMD ROCm GPU acceleration for lightning-fast inference (< 200 ms latency) with seamless CPU fallback.
* **Live Security Dashboard**: A zero-dependency React frontend served via a Python backend, providing a real-time visualization of system status, anomaly scores, file I/O rates, and CPU metrics.
* **Zero-Day Threat Detection**: Catches unknown and newly developed ransomware variants by recognizing their behavioral fingerprint rather than relying on known signatures.

## 📁 System Architecture

```
System Monitor Agent (CPU/IO/Entropy tracking)
        ↓
Feature Extractor (Translates telemetry to ML vectors)
        ↓
AI Inference Engine (PyTorch Autoencoder / ROCm GPU)
        ↓
Threat Scoring Engine (Anomaly Score evaluation)
        ↓
Live React Dashboard & Alerts
```

## 🛠️ Technology Stack

* **Backend / Monitoring**: Python, `psutil`
* **Machine Learning**: PyTorch (Autoencoder model), AMD ROCm / CUDA
* **Frontend Panel**: React, Plotly (for real-time metric visualization)
* **Deployment**: Localhost accessible zero-dependency UI

## 🎯 The Why

Traditional antivirus solutions often fail against zero-day ransomware because they wait to match malicious file signatures. Foresight-RX understands the **behavior** of ransomware—such as sudden bursts of file writes and increasing data entropy—allowing for critical early warnings and potential automated isolation before significant damage and data loss can occur.

## 🏁 Demo Summary

1. User opens `http://localhost:8000` to access the Live Security Dashboard. The baseline OS-level metrics and system status indicate "**SAFE**".
2. **Trigger Attack Simulation**: Running the included ransomware simulator generates rapid file writes and manipulates file extensions. 
3. The Feature Extractor detects a sudden rise in File Entropy and Writes/Sec.
4. The Autoencoder detects anomalous system behavior from the healthy baseline, triggering a high Reconstruction Error (Anomaly Score).
5. The system instantly scores the threat as "**CRITICAL: Ransomware Likely**".
6. Understanding the ransomware signature, the system can clear the threat and reset back to the normal state.