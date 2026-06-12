# SRE 服务器监控与自动巡检系统

这是一个面向 SRE 入门场景的服务器监控与自动巡检项目。项目基于 Python + FastAPI 开发，提供健康检查、资源指标采集和主机信息查看接口，并配套自动巡检脚本、Docker 容器化部署示例、crontab 定时任务示例和故障处理 Runbook。

## 功能

- `/health`：服务健康检查
- `/metrics`：CPU、内存、磁盘资源指标
- `/info`：主机名、操作系统、Python 版本等运行环境信息
- `check_metrics.py`：自动请求 `/health` 和 `/metrics`，超过阈值时输出 `ALERT`
- `Dockerfile`：容器化运行 FastAPI 服务
- `deploy/crontab.example`：每分钟自动巡检示例
- `runbooks/incident-response.md`：基础故障排查流程

## 技术栈

- Python
- FastAPI
- psutil
- requests
- Docker
- crontab
- Linux / Windows 本地开发

## 项目结构

```text
sre-health-monitor/
  main.py
  check_metrics.py
  Dockerfile
  requirements.txt
  config/
  deploy/
  runbooks/
  src/
    api/
    alerting/
    collector/
  tests/
```

## 本地启动

创建虚拟环境并安装依赖：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell：

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

启动服务：

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

访问接口：

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/metrics
curl http://127.0.0.1:8000/info
```

## 接口说明

### 健康检查

```bash
curl http://127.0.0.1:8000/health
```

示例返回：

```json
{
  "status": "ok",
  "timestamp": 1780906842,
  "uptime_seconds": 12.34
}
```

### 资源指标

```bash
curl http://127.0.0.1:8000/metrics
```

示例返回：

```json
{
  "cpu_percent": 1.0,
  "memory": {
    "total_mb": 908.72,
    "used_mb": 436.35,
    "available_mb": 472.37,
    "percent": 48.0
  },
  "disk": {
    "total_gb": 6.61,
    "used_gb": 3.48,
    "free_gb": 3.11,
    "percent": 52.8
  }
}
```

### 主机信息

```bash
curl http://127.0.0.1:8000/info
```

示例返回：

```json
{
  "hostname": "server-01",
  "system": "Linux",
  "platform": "Linux-6.8.0-x86_64-with-glibc2.39",
  "python_version": "3.11.15"
}
```

## 自动巡检

手动执行：

```bash
python check_metrics.py
```

将结果写入日志：

```bash
python check_metrics.py >> monitor.log 2>&1
tail -n 20 monitor.log
```

脚本默认检查 `http://127.0.0.1:8000`，也可以指定地址：

```bash
python check_metrics.py --base-url http://127.0.0.1:8000
```

默认阈值为 80%。超过 CPU、内存或磁盘阈值时，脚本会输出 `ALERT` 并返回非 0 退出码。

## crontab 示例

```bash
* * * * * cd /home/ubuntu/sre-health-monitor && /home/ubuntu/sre-health-monitor/.venv/bin/python check_metrics.py >> /home/ubuntu/sre-health-monitor/monitor.log 2>&1
```

这个配置表示每分钟执行一次巡检脚本，并将正常输出和错误输出追加到 `monitor.log`。

## Docker 部署

构建镜像：

```bash
docker build -t sre-health-monitor .
```

运行容器：

```bash
docker run -d -p 8000:8000 --name sre-monitor-container sre-health-monitor
```

查看容器状态和日志：

```bash
docker ps
docker logs -f sre-monitor-container
```

## 故障模拟与恢复

模拟服务故障：

```bash
docker stop sre-monitor-container
python check_metrics.py
```

预期输出包含：

```text
ALERT: health check request failed
ALERT: failed to check metrics
```

恢复服务：

```bash
docker start sre-monitor-container
python check_metrics.py
```

预期输出包含：

```text
HEALTH OK: service is running
METRICS OK: cpu=... memory=... disk=...
```

## 常见问题

### 端口被占用

现象：

```text
address already in use
```

排查：

```bash
ss -tunlp | grep 8000
```

Windows PowerShell：

```powershell
netstat -ano | findstr :8000
```

### 容器名称冲突

现象：

```text
container name is already in use
```

解决：

```bash
docker rm sre-monitor-container
```

### 缺少依赖

现象：

```text
ModuleNotFoundError
```

解决：

```bash
pip install -r requirements.txt
```

## 测试

```bash
pytest
```

## 项目收获

通过这个项目可以实践 SRE 入门阶段常见的完整闭环：服务部署、健康检查、指标采集、自动巡检、阈值告警、日志记录、容器化部署、故障模拟、恢复验证和基础排障。
