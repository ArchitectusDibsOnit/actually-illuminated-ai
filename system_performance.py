# system_performance.py

import psutil
import platform
import time

def recommend_max_frame():
    """
    Recommend max frame slice size based on system RAM and CPU.
    Returns recommended duration in seconds.
    """
    total_memory_gb = psutil.virtual_memory().total / (1024 ** 3)
    cpu_count = psutil.cpu_count(logical=True)

    if total_memory_gb < 8 or cpu_count <= 4:
        return 6  # Low-end machines
    elif total_memory_gb < 16 or cpu_count <= 8:
        return 10  # Mid-tier
    else:
        return 15  # High-end machines

def estimate_eta(total_duration, slice_size):
    """
    Estimate total generation time based on slice size and system class.
    """
    slices = total_duration // slice_size + (1 if total_duration % slice_size else 0)

    # Per-slice generation speed estimated based on system class
    if slice_size <= 6:
        per_slice_time = 30  # low-end (longer processing)
    elif slice_size <= 10:
        per_slice_time = 20  # mid-tier
    else:
        per_slice_time = 12  # high-end

    estimated_time = slices * per_slice_time
    return estimated_time

def system_summary():
    """
    Returns a quick summary of system resources.
    """
    total_memory_gb = psutil.virtual_memory().total / (1024 ** 3)
    cpu_count = psutil.cpu_count(logical=True)
    return f"Detected System: {platform.system()} | RAM: {total_memory_gb:.1f} GB | CPU Cores: {cpu_count}"

def benchmark_system_speed():
    """
    Runs a quick CPU stress test to estimate how fast the system handles a simple loop.
    """
    start = time.time()
    _ = [x ** 2 for x in range(10_000_000)]
    end = time.time()
    duration = end - start

    if duration > 6:
        return "Performance Rating: 🚧 Low-End (Expect longer generation times)"
    elif duration > 3:
        return "Performance Rating: ⚙️ Mid-Tier (Decent generation speed)"
    else:
        return "Performance Rating: 🚀 High-End (Fast generation expected)"
