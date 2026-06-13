from fastapi import FastAPI
import psutil
import socket
import platform
import time

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "SRE Monitor API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "timestamp": int(time.time())
    }

@app.get("/metrics")
def metrics():
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory": {
            "total_mb": round(memory.total / 1024 / 1024, 2),
            "used_mb": round(memory.used / 1024 / 1024, 2),
            "available_mb": round(memory.available / 1024 / 1024, 2),
            "percent": memory.percent
        },
        "disk": {
            "total_gb": round(disk.total / 1024 / 1024 / 1024, 2),
            "used_gb": round(disk.used / 1024 / 1024 / 1024, 2),
            "free_gb": round(disk.free / 1024 / 1024 / 1024, 2),
            "percent": disk.percent
        }
    }


@app.get("/info")
def info():
    return {
        "hostname": socket.gethostname(),
        "system": platform.system(),
        "platform": platform.platform(),
        "python_version": platform.python_version()
    }
