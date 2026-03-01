import psutil
import time
from collections import defaultdict

class ProcessMonitor:
    """Uses psutil to track real-time OS process creation events and CPU spikes."""
    
    def __init__(self, history_window=30):
        self.history_window = history_window
        self.known_pids = set()
        self.process_creation_history = []  # List of timestamps
        self.cpu_history = []
        # Add root path processes to whitelist (e.g. the dashboard itself)
        
    def poll(self):
        """Called every second to analyze the system."""
        current_time = time.time()
        current_pids = set(psutil.pids())
        
        # Calculate new processes created since last poll
        new_pids = current_pids - self.known_pids
        self.known_pids = current_pids
        
        # Record creations
        for _ in new_pids:
            self.process_creation_history.append(current_time)
            
        # Clean old history (sliding window)
        cutoff_time = current_time - self.history_window
        self.process_creation_history = [t for t in self.process_creation_history if t > cutoff_time]
        
        # Calculate burst score (e.g. ransomware spawning many workers)
        burst_score = min(len(self.process_creation_history) / 10.0, 1.0) # naive scale 0-1
        
        # Global CPU
        cpu_spike = psutil.cpu_percent(interval=0.1)
        self.cpu_history.append(cpu_spike)
        if len(self.cpu_history) > self.history_window:
            self.cpu_history.pop(0)
            
        return {
            "burst_score": burst_score,
            "cpu_spike": cpu_spike
        }
        
    def reset(self):
        """Clears the sliding history window when the app resets."""
        self.known_pids = set()
        self.process_creation_history = []
        self.cpu_history = []
