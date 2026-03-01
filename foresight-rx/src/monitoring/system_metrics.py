import time
import random
import yaml

class MockTelemetryGenerator:
    """Generates synthetic telemetry data as a placeholder for real OS monitoring."""
    
    def __init__(self, config_path="config/config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
            
        self.poll_interval = self.config["monitoring"]["poll_interval_sec"]
        self.is_attack_active = False

    def trigger_attack(self):
        """Simulates an attack starting by spiking metrics."""
        self.is_attack_active = True

    def reset_state(self):
        """Returns to normal benign state."""
        self.is_attack_active = False

    def get_latest_metrics(self):
        """Returns a snapshot of current system and file metrics."""
        if not self.is_attack_active:
            # Benign baseline: low I/O, low CPU, low entropy
            metrics = {
                "timestamp": time.time(),
                "writes_per_sec": random.uniform(0.1, 5.0),
                "renames_per_sec": random.uniform(0.0, 0.5),
                "entropy_delta": random.uniform(0.001, 0.05),
                "unique_exts": random.randint(1, 3),
                "burst_score": random.uniform(0.0, 0.2),
                "cpu_spike": random.uniform(5.0, 15.0)
            }
        else:
            # Ransomware behavior: High write/rename burst, huge entropy spike, CPU load
            metrics = {
                "timestamp": time.time(),
                "writes_per_sec": random.uniform(50.0, 200.0),
                "renames_per_sec": random.uniform(20.0, 100.0),
                "entropy_delta": random.uniform(0.5, 0.95),  # High entropy = encryption
                "unique_exts": random.randint(1, 2), # Focuses on .encrypted etc
                "burst_score": random.uniform(0.8, 1.0),
                "cpu_spike": random.uniform(70.0, 95.0)
            }
        
        return metrics

if __name__ == "__main__":
    generator = MockTelemetryGenerator()
    print("Normal Metrics:", generator.get_latest_metrics())
    generator.trigger_attack()
    print("Attack Metrics:", generator.get_latest_metrics())
