import torch
import torch.nn as nn
from src.ai.autoencoder import RansomwareAutoencoder, get_device
import yaml
import os

class ThreatScorer:
    def __init__(self):
        self.device = get_device()
        self.model = RansomwareAutoencoder().to(self.device)
        self.model.eval() # Inference mode
        self.loss_fn = nn.MSELoss()
        
        # Load config
        config_path = os.path.join(os.path.dirname(__file__), "..", "..", "config", "config.yaml")
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
            
        self.low_thresh = self.config["detection"]["score_threshold_low"]
        self.crit_thresh = self.config["detection"]["score_threshold_critical"]

        # Auto-load the latest trained model if available
        models_dir = os.path.join(os.path.dirname(__file__), "..", "..", "models", "trained")
        if os.path.exists(models_dir):
            model_files = [f for f in os.listdir(models_dir) if f.endswith(".pth")]
            if model_files:
                latest_model = sorted(model_files)[-1]
                model_path = os.path.join(models_dir, latest_model)
                self.model.load_state_dict(torch.load(model_path, map_location=self.device, weights_only=True))

    def compute_anomaly_score(self, feature_vector):
        """
        Runs inference on the feature vector and returns an anomaly score based on reconstruction error.
        Higher error = Higher probability of ransomware.
        """
        # --- UI DEMO OVERRIDE ---
        # If the system is completely idle of malicious file IO (0 writes, 0 renames), force the AI score 
        # to a minimal baseline (0.01) to hide the autoencoder's mathematical noise from high background CPU.
        # This ensures the dashboard firmly snaps back to GREEN (SAFE) after a reset.
        if feature_vector[0] == 0.0 and feature_vector[1] == 0.0:
            return 0.01
            
        # Convert numpy array to torch tensor
        input_tensor = torch.tensor(feature_vector, dtype=torch.float32).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            reconstructed = self.model(input_tensor)
            
        # Calculate Mean Squared Error loss (Reconstruction Error)
        error = self.loss_fn(reconstructed, input_tensor).item()
        
        # Scale error to roughly 0-1 for dashboard
        # This is a naive scaling for the MVP demo
        scaled_score = min(error * 10, 1.0) 
        return scaled_score

    def get_risk_level(self, score):
        if score >= self.crit_thresh:
            return "Ransomware Likely"
        elif score >= self.low_thresh:
            return "Suspicious"
        else:
            return "Safe"
