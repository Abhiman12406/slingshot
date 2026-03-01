import os
import subprocess
import sys

def setup_demo():
    print("Setting up Foresight-RX Demo Environment...")

    # Create dummy data directory
    dummy_dir = os.path.join(os.path.dirname(__file__), "..", "data", "samples", "dummy_files")
    if not os.path.exists(dummy_dir):
        os.makedirs(dummy_dir)
        print(f"Created directory: {dummy_dir}")
        
    print("Setup complete. Starting the React + FastAPI Server...")
    
    # Launch FastAPI Server
    api_path = os.path.join(os.path.dirname(__file__), "..", "dashboard", "api.py")
    subprocess.run([sys.executable, api_path])

if __name__ == "__main__":
    setup_demo()
