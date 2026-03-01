from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

class RansomwareEventHandler(FileSystemEventHandler):
    def __init__(self):
        self.recent_writes = 0
        self.recent_renames = 0
        self.touched_extensions = set()
        self.ignore_events = False
        
    def on_modified(self, event):
        if self.ignore_events or event.is_directory:
            return
        self.recent_writes += 1
        _, ext = os.path.splitext(event.src_path)
        self.touched_extensions.add(ext)

    def on_moved(self, event):
        if self.ignore_events or event.is_directory:
            return
        self.recent_renames += 1
        _, ext = os.path.splitext(event.dest_path)
        self.touched_extensions.add(ext)
            
    def get_and_reset_metrics(self):
        """Returns the counts for the current polling interval and resets them for the next."""
        metrics = {
            "writes": self.recent_writes,
            "renames": self.recent_renames,
            "unique_exts_count": len(self.touched_extensions)
        }
        self.recent_writes = 0
        self.recent_renames = 0
        self.touched_extensions.clear()
        return metrics

class FileMonitor:
    """Uses watchdog to track file modifications on disk."""
    def __init__(self, target_dir):
        self.target_dir = target_dir
        self.handler = RansomwareEventHandler()
        self.observer = Observer()
        
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)
            
        self.observer.schedule(self.handler, path=self.target_dir, recursive=True)
        
    def start(self):
        self.observer.start()
        
    def stop(self):
        self.observer.stop()
        self.observer.join()
        
    def poll(self):
        """Extracts the accumulated metrics over the last interval."""
        return self.handler.get_and_reset_metrics()
        
    def reset(self):
        """Forces a hard reset of all accumulating metrics when the app resets."""
        self.handler.recent_writes = 0
        self.handler.recent_renames = 0
        self.handler.touched_extensions.clear()
        
    def pause(self):
        self.handler.ignore_events = True
        
    def resume(self):
        self.handler.ignore_events = False
