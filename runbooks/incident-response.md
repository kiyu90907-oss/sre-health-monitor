# Incident Response Runbook

## Service is unavailable

1. Check whether the API responds:

   ```bash
   curl http://127.0.0.1:8000/health
   ```

2. Check the process or container:

   ```bash
   ps aux | grep uvicorn
   docker ps -a
   ```

3. Review logs:

   ```bash
   tail -n 50 app.log
   tail -n 50 monitor.log
   docker logs sre-monitor-container
   ```

4. Restart the service:

   ```bash
   docker start sre-monitor-container
   ```

## High resource usage

1. Confirm metrics:

   ```bash
   curl http://127.0.0.1:8000/metrics
   ```

2. Find active processes:

   ```bash
   top
   df -h
   free -m
   ```

3. Record the symptom, timeline, cause, and recovery action in the incident notes.
