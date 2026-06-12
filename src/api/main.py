from __future__ import annotations

from fastapi import FastAPI

from src.collector.system_metrics import get_health, get_info, get_metrics

app = FastAPI(
    title="SRE Health Monitor",
    description="Health, system metrics, and host information endpoints for SRE practice.",
    version="1.0.0",
)


@app.get("/health")
def health() -> dict:
    return get_health()


@app.get("/metrics")
def metrics() -> dict:
    return get_metrics()


@app.get("/info")
def info() -> dict:
    return get_info()
