import numpy as np

class FeatureExtractor:
    """Transforms raw telemetry into fixed-size ML vectors."""
    
    def __init__(self, vector_size=6):
        self.vector_size = vector_size
        self.history = []
        self.window_size = 30 # Store last 30 samples

    def process_telemetry(self, raw_metrics):
        """
        Converts a raw metrics dictionary into an ML-ready numpy array.
        Expected keys: writes_per_sec, renames_per_sec, entropy_delta, unique_exts, burst_score, cpu_spike
        """
        self.history.append(raw_metrics)
        if len(self.history) > self.window_size:
            self.history.pop(0)

        # Feature Vector map
        feature_vector = np.array([
            raw_metrics.get("writes_per_sec", 0.0),
            raw_metrics.get("renames_per_sec", 0.0),
            raw_metrics.get("entropy_delta", 0.0),
            raw_metrics.get("unique_exts", 0.0),
            raw_metrics.get("burst_score", 0.0),
            raw_metrics.get("cpu_spike", 0.0)
        ], dtype=np.float32)

        # Optional: Apply scaling/normalization here if needed (e.g., Min-Max over history)
        return feature_vector

    def get_summary_stats(self):
        """Returns moving averages for dashboard display."""
        if not self.history:
            return {}
        
        avg_cpu = sum(m["cpu_spike"] for m in self.history) / len(self.history)
        avg_writes = sum(m["writes_per_sec"] for m in self.history) / len(self.history)
        return {"avg_cpu": avg_cpu, "avg_writes": avg_writes}
