from __future__ import annotations

import platform
import socket
import time
from typing import Any

import psutil

START_TIME = time.time()


def round_float(value: float, digits: int = 2) -> float:
    return round(float(value), digits)


def get_health() -> dict[str, Any]:
    return {
        "status": "ok",
        "timestamp": int(time.time()),
        "uptime_seconds": round_float(time.time() - START_TIME),
    }


def get_metrics() -> dict[str, Any]:
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return {
        "cpu_percent": round_float(psutil.cpu_percent(interval=0.1)),
        "memory": {
            "total_mb": round_float(memory.total / 1024 / 1024),
            "used_mb": round_float(memory.used / 1024 / 1024),
            "available_mb": round_float(memory.available / 1024 / 1024),
            "percent": round_float(memory.percent),
        },
        "disk": {
            "total_gb": round_float(disk.total / 1024 / 1024 / 1024),
            "used_gb": round_float(disk.used / 1024 / 1024 / 1024),
            "free_gb": round_float(disk.free / 1024 / 1024 / 1024),
            "percent": round_float(disk.percent),
        },
    }


def get_info() -> dict[str, str]:
    return {
        "hostname": socket.gethostname(),
        "system": platform.system(),
        "platform": platform.platform(),
        "python_version": platform.python_version(),
    }
