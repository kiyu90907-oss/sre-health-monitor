# SRE Health Monitor

基于 Python + FastAPI + Docker + AWS EC2 + crontab 的 SRE 服务器监控与自动巡检项目。

## 项目介绍

本项目是一个面向 SRE 入门场景的服务器监控与自动巡检系统。

项目提供 `/health`、`/metrics`、`/info` 三个接口，分别用于服务健康检查、服务器资源指标采集和主机信息查看。

同时，项目通过 `check_metrics.py` 自动巡检脚本定时请求 `/health` 和 `/metrics` 接口。当服务不可用，或 CPU、内存、磁盘使用率超过阈值时，会输出 `ALERT` 告警信息，并写入日志。

本项目实践了 SRE 基础流程：服务部署、Docker 容器化、健康检查、指标采集、自动巡检、日志记录、故障模拟和恢复验证。

## 技术栈

- Python
- FastAPI
- psutil
- requests
- Docker
- AWS EC2
- crontab
- Linux

## 项目结构

```text
sre-health-monitor
├── main.py
├── check_metrics.py
├── analyze_monitor_log.py
├── Dockerfile
├── requirements.txt
├── README.md
└── .gitignore
```

## 核心接口

### 健康检查接口

```bash
curl http://127.0.0.1:8000/health
```

用于判断服务是否存活。

### 资源指标接口

```bash
curl http://127.0.0.1:8000/metrics
```

用于查看 CPU、内存、磁盘使用率。

### 主机信息接口

```bash
curl http://127.0.0.1:8000/info
```

用于查看 hostname、系统信息和 Python 版本。

## Docker 部署

构建镜像：

```bash
docker build -t sre-monitor .
```

启动容器：

```bash
docker run -d -p 8000:8000 --name sre-monitor-container sre-monitor
```

查看容器状态：

```bash
docker ps
```

查看容器日志：

```bash
docker logs sre-monitor-container
```

配置容器自动重启策略：

```bash
docker update --restart unless-stopped sre-monitor-container
```

验证重启策略：

```bash
docker inspect -f '{{.HostConfig.RestartPolicy.Name}}' sre-monitor-container
```

如果输出 `unless-stopped`，说明容器已经具备基础自动恢复能力。只要不是手动停止容器，Docker 会在 Docker 服务重启或服务器重启后尽量自动恢复服务。

## 自动巡检

手动执行巡检脚本：

```bash
python3 check_metrics.py
```

将巡检结果写入日志：

```bash
python3 check_metrics.py >> monitor.log 2>&1
```

crontab 定时任务示例：

```bash
* * * * * cd /home/ubuntu && /home/ubuntu/myenv/bin/python check_metrics.py >> /home/ubuntu/monitor.log 2>&1
```

该配置表示每分钟自动执行一次巡检脚本，并将结果写入 `monitor.log`。

## 日志分析

执行日志分析脚本：

```bash
python3 analyze_monitor_log.py
```

该脚本用于统计巡检日志中 `HEALTH OK`、`METRICS OK` 和 `ALERT` 的出现次数，便于快速判断服务近期健康状态。

示例输出：

```text
Monitor Log Analysis Result
---------------------------
HEALTH OK count: 5891
METRICS OK count: 5891
ALERT count: 4
Result: Some alerts were found. Please check service or resource status.
```

其中 `ALERT count` 大于 0，通常说明服务曾经不可用或资源指标超过阈值。本项目中该结果来自故障模拟期间主动停止 Docker 容器产生的告警。

## 故障模拟

停止 Docker 容器：

```bash
docker stop sre-monitor-container
```

等待 crontab 自动巡检后，日志中会出现 `Connection refused` 或 `ALERT` 信息。

恢复服务：

```bash
docker start sre-monitor-container
```

服务恢复后，巡检日志会重新出现 `HEALTH OK` 和 `METRICS OK`。

## 实践中遇到的问题

### 1. 端口占用

现象：

```text
address already in use
```

原因：

旧的 uvicorn 进程占用了宿主机 8000 端口。

排查：

```bash
ss -tunlp | grep 8000
```

解决：

停止旧进程后重新启动 Docker 容器。

### 2. 容器名冲突

现象：

```text
container name is already in use
```

原因：

之前创建失败的容器虽然没有运行，但容器名仍然存在。

排查：

```bash
docker ps -a
```

解决：

```bash
docker rm sre-monitor-container
```

### 3. Python 依赖缺失

现象：

```text
ModuleNotFoundError: No module named 'requests'
```

解决：

```bash
pip install requests
```

### 4. JSON 字段不匹配

现象：

```text
ALERT: Failed to check metrics: 'memory'
```

原因：

巡检脚本读取的字段和 `/metrics` 接口实际返回结构不一致。

排查：

```bash
curl http://127.0.0.1:8000/metrics
```

解决：

根据接口真实返回结构修改 `check_metrics.py` 中的字段读取逻辑。

## 项目收获

通过该项目，我实践了 SRE 入门阶段的完整基础闭环：

- 云服务器部署
- FastAPI 服务开发
- Docker 容器化
- Docker 自动重启策略
- 健康检查接口
- 资源指标采集
- 自动巡检脚本
- 日志分析脚本
- crontab 定时任务
- 日志记录
- 故障模拟
- 服务恢复验证
- 常见问题排查
