# 🚀 Production Deployment Guide

## Quick Start Commands

### Start All Services
```bash
./start_all.sh
```

### Check Status
```bash
./status.sh
```

### Stop All Services
```bash
./stop_all.sh
```

### View Logs
```bash
# Backend logs
tail -f logs/backend.log

# Worker logs
tail -f logs/worker.log

# Dashboard logs
tail -f logs/dashboard.log

# All logs (in separate terminals)
tail -f logs/*.log
```

---

## Setup (First Time Only)

### 1. Create Required Directories
```bash
mkdir -p logs .pids
```

### 2. Make Scripts Executable
```bash
chmod +x start_all.sh stop_all.sh status.sh
```

### 3. Configure Environment
```bash
# Copy and edit .env file
cp .env.example .env
nano .env
```

### 4. Start Services
```bash
./start_all.sh
```

---

## Docker Deployment (Easier Alternative)

### Start
```bash
docker-compose up -d --build
```

### Check Status
```bash
docker-compose ps
```

### View Logs
```bash
docker-compose logs -f
```

### Stop
```bash
docker-compose down
```

---

## Systemd Service (Auto-start on Boot)

Create systemd service for automatic startup:

### 1. Create Service File
```bash
sudo nano /etc/systemd/system/workflow-automation.service
```

### 2. Add Configuration
```ini
[Unit]
Description=Workflow Automation Dashboard
After=network.target redis.service

[Service]
Type=forking
User=dhanush
WorkingDirectory=/home/dhanush/projects/workflow-automation-dashboard
ExecStart=/home/dhanush/projects/workflow-automation-dashboard/start_all.sh
ExecStop=/home/dhanush/projects/workflow-automation-dashboard/stop_all.sh
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 3. Enable and Start
```bash
sudo systemctl enable workflow-automation
sudo systemctl start workflow-automation
sudo systemctl status workflow-automation
```

---

## Monitoring & Maintenance

### Check Service Health
```bash
# Check all services
./status.sh

# Check specific service
ps aux | grep uvicorn
ps aux | grep celery
ps aux | grep streamlit
```

### Monitor Resource Usage
```bash
# CPU and Memory
top -p $(cat .pids/*.pid | tr '\n' ',' | sed 's/,$//')

# Disk usage
du -sh storage/*
```

### Database Management
```bash
# Backup database
cp workflow_automation.db backups/workflow_automation_$(date +%Y%m%d).db

# Check database size
ls -lh workflow_automation.db
```

### Clean Old Files
```bash
# Remove old reports (older than 30 days)
find storage/reports -type f -mtime +30 -delete
find storage/uploads -type f -mtime +30 -delete
```

---

## Troubleshooting

### Services Won't Start
```bash
# Check if ports are in use
lsof -i :8000  # Backend
lsof -i :8501  # Dashboard
lsof -i :6379  # Redis

# Kill processes on ports
kill $(lsof -t -i:8000)
kill $(lsof -t -i:8501)
```

### Redis Not Running
```bash
# Start Redis
sudo service redis-server start

# Check Redis
redis-cli ping
```

### View Error Logs
```bash
# Check logs for errors
grep -i error logs/*.log
```

### Restart Specific Service
```bash
# Stop service
kill $(cat .pids/backend.pid)

# Start service
cd ~/projects/workflow-automation-dashboard
source venv/bin/activate
nohup python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 > logs/backend.log 2>&1 &
echo $! > .pids/backend.pid
```

---

## Performance Optimization

### Increase Worker Concurrency
Edit `start_all.sh`:
```bash
# Change this line:
celery -A workers.celery_app worker --loglevel=info --concurrency=4
```

### Use Production WSGI Server
For better performance, use Gunicorn:
```bash
pip install gunicorn
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### Enable Log Rotation
```bash
# Install logrotate config
sudo nano /etc/logrotate.d/workflow-automation
```

Add:
```
/home/dhanush/projects/workflow-automation-dashboard/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 dhanush dhanush
}
```

---

## Security Checklist

- [ ] Change default passwords in .env
- [ ] Use strong SMTP passwords
- [ ] Restrict API access (add authentication)
- [ ] Enable HTTPS (use nginx reverse proxy)
- [ ] Configure firewall rules
- [ ] Regular backups
- [ ] Update dependencies regularly

---

## Access Points

- **Dashboard**: http://localhost:8501
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## Support

For issues:
1. Check logs: `tail -f logs/*.log`
2. Check status: `./status.sh`
3. Restart services: `./stop_all.sh && ./start_all.sh`
