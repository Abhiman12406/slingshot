import time
import csv
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.monitoring.process_monitor import ProcessMonitor
from src.monitoring.file_monitor import FileMonitor
from src.utils.helpers import get_data_dir

def collect_baseline_data(duration_seconds=60):
    """
    Runs the OS monitors for a specified duration to collect baseline
    telemetry of a normal system state. Saves to CSV for ML training.
    """
    print(f"Starting Data Collection for {duration_seconds} seconds...")
    dummy_dir = os.path.join(get_data_dir("samples"), "dummy_files")
    
    proc_mon = ProcessMonitor(30)
    file_mon = FileMonitor(dummy_dir)
    file_mon.start()
    
    output_file = os.path.join(get_data_dir("raw"), "baseline_telemetry.csv")
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "writes", "renames", "unique_exts", "burst_score", "cpu_percent"])
        
        try:
            for _ in range(duration_seconds):
                p_mets = proc_mon.poll()
                f_mets = file_mon.poll()
                
                writer.writerow([
                    time.time(),
                    f_mets["writes"],
                    f_mets["renames"],
                    f_mets["unique_exts_count"],
                    p_mets["burst_score"],
                    p_mets["cpu_spike"]
                ])
                print(".", end="", flush=True)
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nCollection aborted by user.")
        finally:
            file_mon.stop()
            
    print(f"\nSaved telemetry to {output_file}")

if __name__ == "__main__":
    collect_baseline_data(10) # 10 seconds default for quick testing
