# 导入 requests，用于发送 HTTP 请求
import requests

# 导入 datetime，用于记录当前检查时间
from datetime import datetime


# FastAPI 服务的健康检查接口
HEALTH_URL = "http://127.0.0.1:8000/health"

# FastAPI 服务的资源指标接口
METRICS_URL = "http://127.0.0.1:8000/metrics"

# 告警阈值：超过 80% 就认为有风险
THRESHOLD = 80


def now():
    """
    返回当前时间字符串，方便写入日志。
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def check_health():
    """
    检查服务是否存活。
    如果 /health 能返回 200，说明服务基本可用。
    """
    try:
        response = requests.get(HEALTH_URL, timeout=3)

        if response.status_code == 200:
            print(f"[{now()}] HEALTH OK: service is running")
            return True
        else:
            print(f"[{now()}] ALERT: health check failed, status_code={response.status_code}")
            return False

    except Exception as e:
        print(f"[{now()}] ALERT: health check request failed: {e}")
        return False


def check_metrics():
    """
    检查 CPU、内存、磁盘指标是否超过阈值。
    """
    try:
        response = requests.get(METRICS_URL, timeout=3)
        data = response.json()

        # 当前结构是 cpu_percent / memory_percent / disk_percent
        if "memory_percent" in data:
            cpu = data["cpu_percent"]
            memory = data["memory_percent"]
            disk = data["disk_percent"]

        # 兼容 /metrics 返回结构
        # 新版结构是 memory.percent / disk.percent
        else:
            cpu = data["cpu_percent"]
            memory = data["memory"]["percent"]
            disk = data["disk"]["percent"]

        print(f"[{now()}] CPU: {cpu}%")
        print(f"[{now()}] Memory: {memory}%")
        print(f"[{now()}] Disk: {disk}%")

        if cpu > THRESHOLD:
            print(f"[{now()}] ALERT: CPU usage is too high!")

        if memory > THRESHOLD:
            print(f"[{now()}] ALERT: Memory usage is too high!")

        if disk > THRESHOLD:
            print(f"[{now()}] ALERT: Disk usage is too high!")

        if cpu <= THRESHOLD and memory <= THRESHOLD and disk <= THRESHOLD:
            print(f"[{now()}] METRICS OK: all metrics are normal")

    except Exception as e:
        print(f"[{now()}] ALERT: failed to check metrics: {e}")


def main():
    """
    主函数：先检查服务健康状态，再检查资源指标。
    """
    check_health()
    check_metrics()


# Python 程序入口
if __name__ == "__main__":
    main()
