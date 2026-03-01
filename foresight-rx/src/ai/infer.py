import torch
import sys
import os
import argparse
import yaml

# Add root project dir to path to find src
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from src.ai.autoencoder import RansomwareAutoencoder, get_device
from src.features.feature_extractor import FeatureExtractor

def run_inference(vector_args):
    """Standalone CLI script to test specific ransomware feature vectors."""
    try:
        config_path = os.path.join(os.path.dirname(__file__), "..", "..", "config", "config.yaml")
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            
        device = get_device()
        model = RansomwareAutoencoder(
            input_dim=config["model"]["input_dim"], 
            hidden_dim=config["model"]["hidden_dim"]
        ).to(device)
        
        # Load latest trained weights if they exist
        checkpoint = os.path.join(os.path.dirname(__file__), "..", "..", config["model"]["checkpoint_path"])
        if os.path.exists(checkpoint):
            model.load_state_dict(torch.load(checkpoint, map_location=device, weights_only=True))
        
        model.eval()
        
        extractor = FeatureExtractor(config["features"]["vector_size"])
        # Mocking the raw telemetry from CLI arguments
        raw_metrics = {
            "writes_per_sec": vector_args[0],
            "renames_per_sec": vector_args[1],
            "entropy_delta": vector_args[2],
            "unique_exts": vector_args[3],
            "burst_score": vector_args[4],
            "cpu_spike": vector_args[5]
        }
        
        feature_vec = extractor.process_telemetry(raw_metrics)
        input_tensor = torch.tensor(feature_vec, dtype=torch.float32).unsqueeze(0).to(device)
        
        with torch.no_grad():
            reconstructed = model(input_tensor)
            
        loss_fn = torch.nn.MSELoss()
        anomaly_score = loss_fn(reconstructed, input_tensor).item() * 10
        
        print("\n=== Foresight-RX GPU Inference CLI ===")
        print(f"Device: {device}")
        print(f"Input Vector: {feature_vec}")
        print(f"Calculated Anomaly Score: {anomaly_score:.4f}")
        
        if anomaly_score > config["detection"]["score_threshold_critical"]:
            print("Verdict: [CRITICAL] Ransomware Pattern Detected!")
        elif anomaly_score > config["detection"]["score_threshold_low"]:
            print("Verdict: [WARNING] Suspicious Behavior.")
        else:
            print("Verdict: [OK] Normal System State.")
            
    except Exception as e:
        print(f"Inference failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Foresight-RX Model Inference.")
    parser.add_argument('--vector', nargs=6, type=float, required=True, 
                        help='Provide 6 feature values: writes, renames, entropy, exts, burst, cpu')
    args = parser.parse_args()
    run_inference(args.vector)
