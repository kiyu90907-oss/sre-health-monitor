from __future__ import annotations

import argparse
import datetime as dt
import os
import sys
from dataclasses import dataclass
from typing import Any

import requests


@dataclass(frozen=True)
class Thresholds:
    cpu: float = 80.0
    memory: float = 80.0
    disk: float = 80.0


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def log(level: str, message: str) -> str:
    return f"{now()} {level}: {message}"


def fetch_json(base_url: str, path: str, timeout: float) -> dict[str, Any]:
    response = requests.get(f"{base_url.rstrip('/')}{path}", timeout=timeout)
    response.raise_for_status()
    return response.json()


def check_health(base_url: str, timeout: float) -> list[str]:
    try:
        data = fetch_json(base_url, "/health", timeout)
    except requests.RequestException as exc:
        return [log("ALERT", f"health check request failed: {exc}")]

    if data.get("status") != "ok":
        return [log("ALERT", f"health status is not ok: {data!r}")]

    return [log("HEALTH OK", "service is running")]


def check_metric_thresholds(metrics: dict[str, Any], thresholds: Thresholds) -> list[str]:
    alerts: list[str] = []
    cpu_percent = float(metrics.get("cpu_percent", 0))
    memory_percent = float(metrics.get("memory", {}).get("percent", 0))
    disk_percent = float(metrics.get("disk", {}).get("percent", 0))

    if cpu_percent >= thresholds.cpu:
        alerts.append(log("ALERT", f"cpu usage high: {cpu_percent}% >= {thresholds.cpu}%"))
    if memory_percent >= thresholds.memory:
        alerts.append(log("ALERT", f"memory usage high: {memory_percent}% >= {thresholds.memory}%"))
    if disk_percent >= thresholds.disk:
        alerts.append(log("ALERT", f"disk usage high: {disk_percent}% >= {thresholds.disk}%"))

    if alerts:
        return alerts

    return [
        log(
            "METRICS OK",
            f"cpu={cpu_percent}% memory={memory_percent}% disk={disk_percent}%",
        )
    ]


def check_metrics(base_url: str, timeout: float, thresholds: Thresholds) -> list[str]:
    try:
        metrics = fetch_json(base_url, "/metrics", timeout)
    except requests.RequestException as exc:
        return [log("ALERT", f"failed to check metrics: {exc}")]
    except ValueError as exc:
        return [log("ALERT", f"invalid metrics response: {exc}")]

    return check_metric_thresholds(metrics, thresholds)


def run_checks(base_url: str, timeout: float, thresholds: Thresholds) -> tuple[int, list[str]]:
    lines = check_health(base_url, timeout)
    lines.extend(check_metrics(base_url, timeout, thresholds))
    exit_code = 1 if any("ALERT" in line for line in lines) else 0
    return exit_code, lines


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check SRE health monitor endpoints.")
    parser.add_argument(
        "--base-url",
        default=os.getenv("SRE_MONITOR_BASE_URL", "http://127.0.0.1:8000"),
        help="Base URL for the FastAPI service.",
    )
    parser.add_argument("--timeout", type=float, default=5.0, help="Request timeout in seconds.")
    parser.add_argument("--cpu-threshold", type=float, default=float(os.getenv("SRE_CPU_THRESHOLD", 80.0)))
    parser.add_argument(
        "--memory-threshold",
        type=float,
        default=float(os.getenv("SRE_MEMORY_THRESHOLD", 80.0)),
    )
    parser.add_argument("--disk-threshold", type=float, default=float(os.getenv("SRE_DISK_THRESHOLD", 80.0)))
    return parser


def main() -> int:
    args = build_parser().parse_args()
    thresholds = Thresholds(
        cpu=args.cpu_threshold,
        memory=args.memory_threshold,
        disk=args.disk_threshold,
    )
    exit_code, lines = run_checks(args.base_url, args.timeout, thresholds)
    for line in lines:
        print(line)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
