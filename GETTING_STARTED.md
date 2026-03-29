# 🚀 Getting Started - Quick Guide

## Prerequisites Checklist

- [ ] Python 3.11+ installed
- [ ] Redis installed and running
- [ ] Git (optional, for version control)

---

## ⚡ Quick Start (5 Minutes)

### Step 1: Setup (One-time)

```powershell
# Run setup script
.\setup.ps1
```

This will:
- Create virtual environment
- Install all dependencies
- Create .env file

### Step 2: Start Redis

**Option A - Using Redis Service:**
```powershell
redis-server
```

**Option B - Using Docker:**
```powershell
docker run -d -p 6379:6379 redis:alpine
```

### Step 3: Start the Application

Open **3 separate PowerShell terminals** in the project directory:

**Terminal 1 - Backend:**
```powershell
.\start_backend.ps1
```
Wait for: "✅ Workflow Automation Dashboard started successfully!"

**Terminal 2 - Worker:**
```powershell
.\start_worker.ps1
```
Wait for: "celery@... ready"

**Terminal 3 - Dashboard:**
```powershell
.\start_dashboard.ps1
```
Browser will auto-open to http://localhost:8501

---

## 🎯 First Test Run

1. **Open Dashboard**: http://localhost:8501
2. **Upload Sample File**: Use `sample_data.csv` from project root
3. **Configure Job**:
   - Job Name: "My First Test"
   - Leave email disabled for now
4. **Click "Start Processing"**
5. **Watch Progress**: Real-time updates
6. **Download Reports**: Both CSV and PDF

---

## 🔧 Configuration (Optional)

### Enable Email Notifications

Edit `.env`:
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
```

**Get Gmail App Password:**
1. Enable 2FA: https://myaccount.google.com/security
2. Create App Password: https://myaccount.google.com/apppasswords
3. Use generated password in .env

---

## 📝 Common Tasks

### View API Documentation
http://localhost:8000/docs

### Check Backend Health
http://localhost:8000/health

### Run Tests
```powershell
pytest tests/ -v
```

### Stop Everything
Press `Ctrl+C` in each terminal

---

## 🐛 Troubleshooting

### Redis Not Running
```
Error: Error 10061 connecting to localhost:6379
```
**Solution:** Start Redis with `redis-server`

### Port Already in Use
```
Error: [Errno 10048] error while attempting to bind on address
```
**Solution:** Kill process using the port or change port in `.env`

### Import Errors
```
ModuleNotFoundError: No module named 'X'
```
**Solution:** 
```powershell
pip install -r requirements.txt
```

### Celery Won't Start (Windows)
```
Error: Pool not implemented for Windows
```
**Solution:** Already handled in `start_worker.ps1` with `--pool=solo`

---

## 📚 Next Steps

1. ✅ Complete first test run
2. 📧 Configure email (optional)
3. 🎨 Customize data processing logic
4. 🐳 Try Docker deployment
5. 🚀 Deploy to production

---

## 🎓 Learning Path

### Day 1: Setup & Test
- Complete setup
- Upload sample data
- Understand the flow

### Day 2: Customize
- Modify data cleaning logic
- Customize email templates
- Add custom validations

### Day 3: Extend
- Add new endpoints
- Create custom reports
- Integrate with other APIs

### Day 4: Deploy
- Docker deployment
- Production configuration
- Security hardening

---

## 💡 Pro Tips

1. **Use Multiple Browser Tabs**:
   - Tab 1: Dashboard
   - Tab 2: API Docs
   - Tab 3: Job Status

2. **Monitor Logs**:
   - Backend terminal shows API requests
   - Worker terminal shows processing details

3. **Test with Small Files First**:
   - Use sample_data.csv (12 rows)
   - Then try larger files

4. **Save Job IDs**:
   - Copy job ID for API testing
   - Use in Postman/curl

---

## 📞 Need Help?

- 📖 Read full README.md
- 🐛 Check troubleshooting section
- 💬 Open GitHub issue
- 📧 Contact: your-email@example.com

---

**Happy Automating! 🎉**
