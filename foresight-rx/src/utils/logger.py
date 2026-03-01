import logging
import os
import sys

def get_logger(name: str) -> logging.Logger:
    """Configures and returns a standard logger for the application."""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console Handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
        # File Handler
        log_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data")
        if os.path.exists(log_dir): # Only add if project structure is setup
            fh = logging.FileHandler(os.path.join(log_dir, "foresight.log"))
            fh.setFormatter(formatter)
            logger.addHandler(fh)
            
    return logger
