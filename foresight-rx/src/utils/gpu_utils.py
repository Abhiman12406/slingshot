import torch
import psutil

def check_amd_rocm_status():
    """Checks for an active AMD ROCm GPU environment."""
    status = {
        "is_rocm_available": False,
        "is_cuda_available": torch.cuda.is_available(),
        "device_count": 0,
        "device_name": "CPU"
    }

    if torch.cuda.is_available():
        status["device_count"] = torch.cuda.device_count()
        status["device_name"] = torch.cuda.get_device_name(0)
        
        # PyTorch on ROCm identifies itself through version tags or HIP bindings
        version = torch.__version__
        if "rocm" in version.lower():
            status["is_rocm_available"] = True
            
    return status

def get_system_memory():
    """Returns general host memory stats."""
    mem = psutil.virtual_memory()
    return {
        "total_gb": round(mem.total / (1024.**3), 2),
        "available_gb": round(mem.available / (1024.**3), 2),
        "used_percent": mem.percent
    }
    
if __name__ == "__main__":
    print("GPU Status:", check_amd_rocm_status())
    print("Host RAM:", get_system_memory())
