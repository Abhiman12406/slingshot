import math
import collections
import os

class EntropyCalculator:
    """Calculates Shannon entropy to detect encryption sequences."""
    
    @staticmethod
    def calculate_shannon_entropy(data: bytes) -> float:
        """
        Calculates the Shannon entropy of a byte sequence.
        Returns a value between 0.0 and 8.0.
        Scores > 7.5 usually indicate compressed or encrypted data.
        """
        if not data:
            return 0.0
            
        entropy = 0.0
        length = len(data)
        
        # Count byte frequencies
        frequencies = collections.Counter(data)
        
        for count in frequencies.values():
            probability = count / length
            entropy -= probability * math.log2(probability)
            
        return entropy

    @staticmethod
    def measure_file_entropy(filepath: str, sample_size: int = 1024) -> float:
        """Reads a chunk of a file to estimate its entropy efficiently."""
        try:
            if not os.path.exists(filepath):
                return 0.0
            with open(filepath, 'rb') as f:
                data = f.read(sample_size)
                return EntropyCalculator.calculate_shannon_entropy(data)
        except (FileNotFoundError, PermissionError):
            return 0.0
