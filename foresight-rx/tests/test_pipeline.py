import sys
import os
import torch

# Add root project dir to path to find src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.features.entropy_calculator import EntropyCalculator
from src.ai.autoencoder import RansomwareAutoencoder
from src.features.feature_extractor import FeatureExtractor

def test_entropy_calculator():
    # Byte arrays of varying entropy
    low_entropy = b"AAAAAAAAAAAAAAAAA" 
    high_entropy = os.urandom(100) # Pure random noise is close to max entropy
    
    low_score = EntropyCalculator.calculate_shannon_entropy(low_entropy)
    high_score = EntropyCalculator.calculate_shannon_entropy(high_entropy)
    
    assert low_score < 1.0, f"Expected low entropy < 1.0, got {low_score}"
    assert high_score > 6.0, f"Expected high entropy > 6.0, got {high_score}"

def test_feature_extractor():
    extractor = FeatureExtractor(vector_size=6)
    mock_metrics = {
        "writes_per_sec": 10.0,
        "renames_per_sec": 2.0,
        "entropy_delta": 0.5,
        "unique_exts": 1,
        "burst_score": 0.1,
        "cpu_spike": 50.0
    }
    vec = extractor.process_telemetry(mock_metrics)
    assert len(vec) == 6
    assert vec[0] == 10.0 # writes check
    
def test_model_forward_pass():
    model = RansomwareAutoencoder(input_dim=6, hidden_dim=16)
    model.eval()
    dummy_input = torch.randn(1, 6)
    output = model(dummy_input)
    assert output.shape == (1, 6) # Ensures reconstruction shape matches input shape
    
if __name__ == "__main__":
    # Standard pytest structure
    test_entropy_calculator()
    test_feature_extractor()
    test_model_forward_pass()
    print("All pipeline tests passed successfully.")
