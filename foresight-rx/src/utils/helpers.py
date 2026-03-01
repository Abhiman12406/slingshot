import os

def resolve_project_root() -> str:
    """Returns the absolute path to the foresight-rx root directory."""
    # Assuming helpers.py is at `foresight-rx/src/utils/helpers.py`
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    
def get_data_dir(subfolder: str) -> str:
    """Helper to get standardized data paths (e.g. 'raw', 'processed', 'samples')"""
    root = resolve_project_root()
    path = os.path.join(root, "data", subfolder)
    os.makedirs(path, exist_ok=True)
    return path
