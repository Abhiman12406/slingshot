import torch
import torch.nn as nn
import torch.optim as optim
import os
import yaml
import sys
from datetime import datetime

# Add root project dir to path to find src
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from src.ai.autoencoder import RansomwareAutoencoder, get_device
from src.utils.logger import get_logger

logger = get_logger("TrainPipeline")

def generate_synthetic_benign_data(num_samples=10000, vector_size=6):
    """Generates synthetic benign telemetry for initial MVP training if no real data exists."""
    # Data distribution for normal behavior (low writes, zero/low entropy, etc.)
    data = torch.randn(num_samples, vector_size)
    data[:, 0] = torch.abs(torch.normal(1.0, 0.5, (num_samples,)))  # writes
    data[:, 1] = torch.abs(torch.normal(0.1, 0.1, (num_samples,)))  # renames
    data[:, 2] = torch.abs(torch.normal(0.01, 0.05, (num_samples,))) # entropy
    data[:, 3] = torch.randint(1, 4, (num_samples,)).float()         # exts
    data[:, 4] = torch.abs(torch.normal(0.1, 0.1, (num_samples,)))  # burst
    data[:, 5] = torch.abs(torch.normal(5.0, 2.0, (num_samples,)))  # cpu
    return data

def train_model():
    # 1. Setup
    config_path = os.path.join(os.path.dirname(__file__), "..", "..", "config", "config.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
        
    device = get_device()
    model = RansomwareAutoencoder(
        input_dim=config["model"]["input_dim"], 
        hidden_dim=config["model"]["hidden_dim"]
    ).to(device)
    
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()
    
    logger.info(f"Starting autoencoder training on device: {device}")
    
    # 2. Data Preparation (Synthetic fallback for hackathon MVP)
    # In a production system, we load pandas DataFrames from data/processed
    train_data = generate_synthetic_benign_data(vector_size=config["model"]["input_dim"]).to(device)
    dataset = torch.utils.data.TensorDataset(train_data)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=64, shuffle=True)
    
    # 3. Training Loop
    epochs = 20
    model.train()
    for epoch in range(epochs):
        epoch_loss = 0.0
        for batch in dataloader:
            inputs = batch[0]
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, inputs)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
            
        avg_loss = epoch_loss / len(dataloader)
        if (epoch + 1) % 5 == 0:
            logger.info(f"Epoch [{epoch+1}/{epochs}], Loss: {avg_loss:.6f}")
            
    # 4. Save Artifacts
    save_dir = os.path.join(os.path.dirname(__file__), "..", "..", "models", "trained")
    os.makedirs(save_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = os.path.join(save_dir, f"autoencoder_{timestamp}.pth")
    torch.save(model.state_dict(), model_path)
    logger.info(f"Training complete. Weights saved to {model_path}")
    
    # Update latest checkpoint path (Symlink equivalent for windows/simple path update)
    latest_path = os.path.join(os.path.dirname(__file__), "..", "..", config["model"]["checkpoint_path"])
    os.makedirs(os.path.dirname(latest_path), exist_ok=True)
    torch.save(model.state_dict(), latest_path)

if __name__ == "__main__":
    train_model()
