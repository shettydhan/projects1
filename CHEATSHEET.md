# 📋 Quick Reference Cheat Sheet

## 🚀 Quick Commands

### Setup (One-time)
```powershell
.\setup.ps1                    # Complete setup
```

### Run Application (3 terminals)
```powershell
# Terminal 1
.\start_backend.ps1            # FastAPI on port 8000

# Terminal 2  
.\start_worker.ps1             # Celery worker

# Terminal 3
.\start_dashboard.ps1          # Streamlit on port 8501
```

### Docker (Alternative)
```powershell
docker-compose up --build      # Start everything
docker-compose down            # Stop everything
```

---

## 🌐 Important URLs

| Service | URL |
|---------|-----|
| Dashboard | http://localhost:8501 |
| API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| Health Check | http://localhost:8000/health |

---

## 📁 Key Files to Edit

| Task | File |
|------|------|
| API Endpoints | `backend/main.py` |
| Data Cleaning | `services/data_processor.py` |
| Report Format | `services/report_generator.py` |
| Email Template | `services/email_service.py` |
| Dashboard UI | `dashboard/app.py` |
| Background Tasks | `workers/tasks.py` |
| Configuration | `.env` |

---

## 🔧 Configuration (.env)

### Essential Settings
```env
# API
API_PORT=8000

# Database
DATABASE_URL=sqlite:///./workflow_automation.db

# Redis
REDIS_HOST=localhost
CELERY_BROKER_URL=redis://localhost:6379/0
```

### Email Settings (Optional)
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
```

---

## 🔄 API Endpoints Quick Reference

### Upload & Create Job
```bash
curl -X POST http://localhost:8000/api/jobs/upload \
  -F "file=@data.csv" \
  -F "job_name=Test Job" \
  -F "send_email=false"
```

### List Jobs
```bash
curl http://localhost:8000/api/jobs
```

### Get Job Status
```bash
curl http://localhost:8000/api/jobs/{job_id}/status
```

### Download Report
```bash
curl http://localhost:8000/api/jobs/{job_id}/download?format=csv -o report.csv
```

### System Stats
```bash
curl http://localhost:8000/api/stats
```

---

## 🐛 Common Issues & Fixes

### Redis Not Running
```powershell
redis-server               # Start Redis
```

### Port Already in Use
```powershell
# Find process
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F
```

### Module Not Found
```powershell
pip install -r requirements.txt
```

### Celery Won't Start (Windows)
```powershell
# Use --pool=solo flag (already in start_worker.ps1)
celery -A workers.celery_app worker --loglevel=info --pool=solo
```

---

## 📊 Project Structure

```
workflow-automation-dashboard/
├── backend/              # FastAPI app
│   ├── main.py          # API endpoints ⭐
│   ├── models.py        # Database models
│   ├── schemas.py       # Request/response schemas
│   └── config.py        # Configuration
├── services/            # Business logic
│   ├── data_processor.py      # Data cleaning ⭐
│   ├── report_generator.py    # PDF/CSV reports ⭐
│   └── email_service.py       # Email automation ⭐
├── workers/             # Background tasks
│   ├── celery_app.py    # Celery config
│   └── tasks.py         # Task definitions ⭐
├── dashboard/           # UI
│   └── app.py          # Streamlit app ⭐
└── storage/            # Files
    ├── uploads/        # User uploads
    └── reports/        # Generated reports
```

⭐ = Most commonly edited files

---

## 🧪 Testing

### Run Tests
```powershell
pytest tests/ -v
```

### Test with Sample Data
```powershell
# Use included sample_data.csv
# Upload via dashboard
```

### Manual API Test (PowerShell)
```powershell
# Health check
Invoke-WebRequest http://localhost:8000/health

# Get stats
Invoke-WebRequest http://localhost:8000/api/stats | ConvertFrom-Json
```

---

## 📦 Dependencies

### Core
- FastAPI - Web framework
- Streamlit - Dashboard
- Celery - Background tasks
- Redis - Task queue
- Pandas - Data processing
- SQLAlchemy - Database ORM

### Install All
```powershell
pip install -r requirements.txt
```

---

## 🎨 Customization Examples

### Add Custom Data Transformation
```python
# services/data_processor.py
def clean_data(self):
    # Add your logic
    self.df['total'] = self.df['price'] * self.df['quantity']
    return self.df
```

### Add New API Endpoint
```python
# backend/main.py
@app.get("/api/custom")
async def custom_endpoint():
    return {"message": "Hello"}
```

### Change Email Template
```python
# services/email_service.py
def send_job_completion_email(self, ...):
    body = f"""<html>Your custom HTML</html>"""
```

---

## 📈 Monitoring

### Check Logs

**Backend:**
```
Terminal 1 output - Shows all API requests
```

**Worker:**
```
Terminal 2 output - Shows task processing
```

**Dashboard:**
```
Terminal 3 output - Shows Streamlit events
```

### Database
```powershell
# View jobs in database
sqlite3 workflow_automation.db
> SELECT * FROM jobs;
```

---

## 🚀 Deployment

### Development
```powershell
.\start_backend.ps1
.\start_worker.ps1
.\start_dashboard.ps1
```

### Docker (Production)
```powershell
docker-compose up -d
```

### Environment Variables
```env
ENVIRONMENT=production
DEBUG=False
```

---

## 💡 Pro Tips

1. **Use API Docs**: http://localhost:8000/docs for interactive testing
2. **Check Redis**: `redis-cli ping` should return PONG
3. **Monitor Jobs**: Use Statistics page in dashboard
4. **Test Email**: Start without email, add later
5. **Sample Data**: Included `sample_data.csv` for testing

---

## 📞 Help & Resources

- **README.md** - Full documentation
- **GETTING_STARTED.md** - Quick start guide
- **PROJECT_OVERVIEW.md** - Architecture deep dive
- **API Docs** - http://localhost:8000/docs

---

## 🎯 Freelancing Pitch Points

1. ✅ "Saves 5+ hours/week on manual data processing"
2. ✅ "Professional PDF reports with company branding"
3. ✅ "Automated email notifications to stakeholders"
4. ✅ "Scalable to handle thousands of rows"
5. ✅ "Production-ready with Docker"

---

**Keep this file open while working! 📌**
