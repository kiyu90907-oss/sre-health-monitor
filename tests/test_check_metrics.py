from src.alerting.check_metrics import Thresholds, check_metric_thresholds


def test_check_metric_thresholds_ok() -> None:
    metrics = {
        "cpu_percent": 10,
        "memory": {"percent": 20},
        "disk": {"percent": 30},
    }

    lines = check_metric_thresholds(metrics, Thresholds())

    assert len(lines) == 1
    assert "METRICS OK" in lines[0]


def test_check_metric_thresholds_alerts() -> None:
    metrics = {
        "cpu_percent": 90,
        "memory": {"percent": 85},
        "disk": {"percent": 95},
    }

    lines = check_metric_thresholds(metrics, Thresholds())

    assert len(lines) == 3
    assert all("ALERT" in line for line in lines)
