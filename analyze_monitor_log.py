# analyze_monitor_log.py
# 作用：分析 monitor.log 巡检日志，统计正常次数和告警次数

# 日志文件名
LOG_FILE = "monitor.log"


def analyze_log():
    """
    读取 monitor.log 文件，
    统计 HEALTH OK、METRICS OK、ALERT 出现的次数。
    """

    # 记录健康检查成功次数
    health_ok_count = 0

    # 记录指标检查成功次数
    metrics_ok_count = 0

    # 记录告警次数
    alert_count = 0

    try:
        # 打开 monitor.log 文件
        # encoding="utf-8" 表示用 UTF-8 编码读取文件
        with open(LOG_FILE, "r", encoding="utf-8") as file:

            # 一行一行读取日志内容
            for line in file:

                # 如果这一行包含 HEALTH OK，说明服务健康检查正常
                if "HEALTH OK" in line:
                    health_ok_count += 1

                # 如果这一行包含 METRICS OK，说明资源指标检查正常
                if "METRICS OK" in line:
                    metrics_ok_count += 1

                # 如果这一行包含 ALERT，说明出现过告警
                if "ALERT" in line:
                    alert_count += 1

        # 输出分析结果
        print("Monitor Log Analysis Result")
        print("---------------------------")
        print(f"HEALTH OK count: {health_ok_count}")
        print(f"METRICS OK count: {metrics_ok_count}")
        print(f"ALERT count: {alert_count}")

        # 根据告警次数输出简单结论
        if alert_count > 0:
            print("Result: Some alerts were found. Please check service or resource status.")
        else:
            print("Result: No alerts found. Service looks healthy.")

    except FileNotFoundError:
        # monitor.log 不存在时，输出错误提示
        print(f"ERROR: {LOG_FILE} not found.")

    except Exception as e:
        # 捕获其他未知错误，避免程序直接崩溃
        print(f"ERROR: failed to analyze log: {e}")


# Python 程序入口
# 只有直接运行这个文件时，才会执行 analyze_log()
if __name__ == "__main__":
    analyze_log()
