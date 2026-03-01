import torch
import torch.nn as nn
import yaml
import os

class RansomwareAutoencoder(nn.Module):
    """
    A lightweight autoencoder to learn benign system behavior.
    High reconstruction error indicates anomalous (ransomware) activity.
    """
    def __init__(self, input_dim=6, hidden_dim=16):
        super(RansomwareAutoencoder, self).__init__()
        
        # Encoder
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU()
        )
        
        # Decoder
        self.decoder = nn.Sequential(
            nn.Linear(hidden_dim // 2, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, input_dim),
            nn.Sigmoid() # Bound outputs if normalized 0-1 initially, else remove
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

def get_device():
    """Determines whether to use AMD ROCm/CUDA GPU or fallback to CPU based on config."""
    config_path = os.path.join(os.path.dirname(__file__), "..", "..", "config", "config.yaml")
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            if config.get("model", {}).get("force_cpu", False):
                return torch.device("cpu")
    except Exception:
        pass # Default to hardware checks if config fails
        
    if torch.cuda.is_available():
        # Maps to ROCm if PyTorch is compiled for ROCm, else CUDA
        return torch.device("cuda")
    
    return torch.device("cpu")

if __name__ == "__main__":
    device = get_device()
    model = RansomwareAutoencoder().to(device)
    print(f"Model initialized on: {device}")
    
    # Test pass
    dummy_input = torch.randn(1, 6).to(device)
    output = model(dummy_input)
    print(f"Test inference output shape: {output.shape}")
