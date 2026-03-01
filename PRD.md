# Product Requirements Document (PRD)

## Product Name

**Foresight-RX: AI-Driven Early Ransomware Prediction on AMD Platforms**

---

# 1. Product Overview

## 1.1 Vision

Build a real-time AI-powered endpoint security system that predicts ransomware attacks **before mass file encryption occurs**, leveraging AMD GPU acceleration for low-latency inference.

## 1.2 Problem Statement

Traditional antivirus solutions detect ransomware only after encryption begins, leading to irreversible data loss. Organizations need proactive behavioral detection that can identify ransomware precursors in real time and respond immediately.

## 1.3 Objectives (Hackathon Scope)

### Primary Objectives

* Monitor live system and file behavior
* Detect ransomware precursors using AI
* Demonstrate early-warning capability
* Utilize AMD ROCm GPU acceleration
* Provide a real-time visualization dashboard

### Secondary Objectives (Stretch Goals)

* Automated process termination
* Explainable AI insights
* Lightweight edge deployment

---

# 2. Target Users

* Security researchers
* SOC analysts
* Enterprise IT administrators
* Endpoint security developers
* AMD edge/data center customers

---

# 3. Value Proposition

Foresight-RX enables:

* Early ransomware detection before damage
* Detection of unknown/zero-day ransomware
* Efficient execution on AMD hardware
* Real-time visual threat intelligence

---

# 4. Scope

## In Scope (MVP)

* Real-time telemetry collection
* Feature extraction pipeline
* AI anomaly detection
* ROCm-accelerated inference
* Live dashboard visualization
* Ransomware simulation for demo

## Out of Scope (MVP)

* Production-grade EDR
* Cloud multi-tenant support
* Kernel-level drivers
* Enterprise policy engine

---

# 5. Functional Requirements

## 5.1 Real-Time Behavior Monitoring

### Description

Continuously collect system and file activity signals.

### Required Signals

* Process creation rate
* File write frequency
* File rename bursts
* Entropy changes in modified files
* CPU usage spikes
* I/O activity bursts

### Requirements

* Poll interval: 1–2 seconds
* Rolling observation window: 30–60 seconds
* Monitoring overhead < 10% CPU

---

## 5.2 Feature Engineering Pipeline

### Description

Transform raw telemetry into ML-ready vectors.

### Required Features

* Writes/sec per process
* Renames/sec
* Entropy delta
* Unique extensions touched
* Process burst score
* Rolling statistical aggregates

### Output

* Fixed-size feature vector per window

---

## 5.3 AI Anomaly Detection Engine

### Description

Predict ransomware likelihood using behavioral patterns.

### Recommended MVP Model

* Autoencoder (PyTorch + ROCm)

### Alternative Models

* Isolation Forest (baseline)
* LSTM sequence model (advanced)

### Requirements

* Inference latency < 200 ms
* GPU acceleration via ROCm when available
* CPU fallback supported
* Output anomaly score (0–1)

---

## 5.4 Threat Scoring & Alerting

### Description

Convert anomaly scores into actionable alerts.

### Risk Levels

* **Safe**: score < low threshold
* **Suspicious**: score between thresholds
* **Ransomware Likely**: score ≥ critical threshold

### Requirements

* Configurable thresholds
* Sliding window smoothing
* Alert logging

---

## 5.5 Live Security Dashboard

### Description

Provide real-time visualization for demo and monitoring.

### Required Widgets

* System status indicator
* Anomaly score timeline
* Top suspicious processes
* File activity graph
* GPU utilization panel (AMD emphasis)

### Recommended Stack

* Streamlit (MVP)
* Plotly charts

---

## 5.6 Automated Response (Optional)

### Possible Actions

* Alert popup
* Process kill (manual trigger)
* Threat logging

### MVP Requirement

* Alert notification

---

# 6. System Architecture

## 6.1 High-Level Flow

```
System Monitor Agent
        ↓
Feature Extractor
        ↓
AI Inference Engine (ROCm GPU)
        ↓
Threat Scoring Engine
        ↓
Dashboard + Alerts
```

## 6.2 AMD Technology Integration

### Required

* AMD Ryzen/EPYC for host execution
* AMD Radeon GPU for inference
* ROCm + PyTorch acceleration

### Bonus

* ONNX Runtime with ROCm
* Model quantization
* GPU telemetry display

---

# 7. Data Requirements

## 7.1 Training Data

### Sources

* Synthetic ransomware simulator
* Benign workload traces
* Public ransomware datasets (optional)

## 7.2 Estimated Volume (MVP)

* 5k–20k behavior windows
* Balanced benign vs attack samples

---

# 8. Prototype Demo Plan

## Demo Flow

### Phase 1 — Normal Activity

* User performs normal file operations
* Dashboard shows SAFE

### Phase 2 — Attack Simulation

* Run ransomware simulator
* Generate rapid file writes and renames
* Entropy increases

### Phase 3 — Detection

* Anomaly score spikes
* Alert triggered
* Suspicious process highlighted
* GPU usage visible

---

# 9. Non-Functional Requirements

## Performance

* Detection delay < 5 seconds
* Monitoring overhead < 10% CPU
* GPU inference preferred

## Reliability

* Graceful CPU fallback
* No crashes under moderate load

## Security & Privacy

* No raw file content stored
* Local processing by default

---

# 10. Risks & Mitigations

| Risk                  | Mitigation                     |
| --------------------- | ------------------------------ |
| High false positives  | Threshold tuning + smoothing   |
| ROCm setup issues     | Provide CPU fallback           |
| Limited training data | Synthetic augmentation         |
| Demo instability      | Provide recorded fallback data |

---

# 11. Success Metrics

The prototype is successful if:

* Ransomware simulator reliably triggers alerts
* Normal workload remains mostly safe
* Inference runs on AMD GPU
* Dashboard updates in real time
* End-to-end demo completes within 5 seconds detection delay

---

# 12. Future Enhancements

* Federated learning across endpoints
* Explainable AI module
* Kernel-level telemetry
* Cloud SOC integration
* Cross-platform agent support

---

**End of PRD**
