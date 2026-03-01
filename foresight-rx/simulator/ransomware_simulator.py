import os
import shutil
import time
import random

class RansomwareSimulator:
    """
    Creates real dummy files in the output directory to simulate real file 
    encryption and massive renaming patterns characteristics of an attack.
    """
    def __init__(self, target_dir="data/samples/dummy_files", num_files=50):
        # Create base path relative to this script
        base_expected_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "samples", "dummy_files"))
        requested_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", target_dir))
        
        # Sandbox validation against path traversal
        if not os.path.commonpath([base_expected_dir]) == os.path.commonpath([base_expected_dir, requested_dir]):
            raise ValueError(f"[Security] Path traversal detected or invalid directory. Must be within {base_expected_dir}")
            
        self.target_dir = requested_dir
        self.num_files = num_files
        self.active_attack = False

    def check_and_create_target_dir(self):
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)
            
    def _create_dummy_data(self):
        """Generates random benign-looking human readable dummy data."""
        return "This is a legitimate company file containing important text data. " * random.randint(10, 100)
            
    def setup_normal_state(self):
        """Spawns standard txt files."""
        print(f"[Simulator] Initializing {self.num_files} benign sample files...")
        self.check_and_create_target_dir()
        
        # Clean up old state
        self._cleanup()
        self.check_and_create_target_dir()

        for i in range(self.num_files):
            file_path = os.path.join(self.target_dir, f"document_important_{i}.txt")
            with open(file_path, "w") as f:
                f.write(self._create_dummy_data())

    def _encrypt_file(self, filepath):
        """Simulates high entropy encryption by writing purely random byte data over the file and appending an extension."""
        # Read Original (Pretend we encrypt it)
        with open(filepath, "rb") as f:
            original_data = f.read()

        # Generate "encrypted" random noise (High entropy) 
        encrypted_data = os.urandom(len(original_data))
        
        # Write back encrypted data
        with open(filepath, "wb") as f:
            f.write(encrypted_data)
            
        # Ransomware typical rename action
        new_filepath = filepath + ".locked"
        os.rename(filepath, new_filepath)

    def trigger_attack(self):
        """Creates the file system burst characteristic of ransomware."""
        print("[Simulator] ALARM: Commencing file encryption attack...")
        self.active_attack = True
        
        files_to_attack = [f for f in os.listdir(self.target_dir) if f.endswith(".txt")]
        if not files_to_attack:
            print("[Simulator] No files found to encrypt. Please run setup_normal_state() first.")
            return

        for filename in files_to_attack:
            if not self.active_attack:
                break # abort if needed
                
            filepath = os.path.join(self.target_dir, filename)
            self._encrypt_file(filepath)
            print(f"Encrypted -> {filename}.locked")
            
            # Simulate rapid iteration by a thread
            time.sleep(random.uniform(0.01, 0.05))

    def _cleanup(self):
        if os.path.exists(self.target_dir):
            for filename in os.listdir(self.target_dir):
                filepath = os.path.join(self.target_dir, filename)
                try:
                    if os.path.isfile(filepath):
                        os.remove(filepath)
                except Exception:
                    pass
            
    def reset(self):
        self.active_attack = False
        print("[Simulator] Resetting file system to normal state...")
        self.setup_normal_state()

if __name__ == "__main__":
    sim = RansomwareSimulator()
    sim.setup_normal_state()
    time.sleep(2)
    sim.trigger_attack()
    print("[Simulator] Attack execution finished.")
