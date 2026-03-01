import os
import sys
from datetime import datetime

# Add root project dir to path to find src
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from src.utils.logger import get_logger

logger = get_logger("AlertManager")

class AlertManager:
    """Handles dispatching of threat notifications."""
    
    def __init__(self):
        self.alert_log_file = os.path.join(os.path.dirname(__file__), "..", "..", "data", "alerts.log")
        
    def trigger_alert(self, risk_level: str, anomaly_score: float, context: dict):
        """Dispatches an alert based on severity."""
        timestamp = datetime.now().isoformat()
        
        alert_msg = f"[{timestamp}] ALERT: {risk_level} | Score: {anomaly_score:.2f} | Context: {context}"
        
        # Log to system logger
        if risk_level == "Ransomware Likely":
            logger.critical(alert_msg)
        elif risk_level == "Suspicious":
            logger.warning(alert_msg)
            
        # Write to dedicated audit log
        try:
            with open(self.alert_log_file, "a") as f:
                f.write(alert_msg + "\n")
        except Exception as e:
            logger.error(f"Failed to write to alert log: {e}")
            
        # Future enhancements: Webhooks, Email, Windows Toast Notifications, etc.
