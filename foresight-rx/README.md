# Foresight-RX: AI-Driven Early Ransomware Prediction

A real-time AI-powered endpoint security system that predicts ransomware attacks before mass file encryption occurs, leveraging PyTorch Autoencoders and AMD ROCm architecture (with CPU fallback).

## Project Structure
* `config/`: System configuration and threshold settings.
* `src/monitoring/`: Captures system file system telemetry (mock MVP provided).
* `src/features/`: Transforms raw telemetry into PyTorch ready feature tensors.
* `src/ai/`: The Autoencoder neural network model.
* `src/detection/`: Threat scoring algorithm to classify behavior as Safe/Suspicious/Ransomware.
* `dashboard/`: A real-time React + Tailwind UI (`ui/`) connected to a FastAPI backend (`api.py`).
* `simulator/`: A ransomware simulator to test the detection pipeline.

## Installation Requirements
```bash
pip install -r requirements.txt
```

## Running the Demo

1. **Initialize the Environment & Start Server**
   ```bash
   python scripts/run_demo.py
   ```
2. **Access the Dashboard**
   Open your browser and navigate to:
   **http://localhost:8000**

*Use the buttons in the React application header to trigger the ransomware simulator.*
