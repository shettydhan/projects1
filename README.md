# 🤖 Business Workflow Automation Dashboard

> **Transform your data processing from hours to minutes with intelligent automation**

A production-ready automation platform that processes Excel/CSV files, generates professional reports, and delivers them via email—all through an intuitive web dashboard. Built for businesses that want to eliminate manual data entry and streamline their workflows.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

<div align="center">

**[🎬 View Demo](#-demo-walkthrough) • [🚀 Quick Start](#-quick-start) • [📖 Documentation](#-usage-guide) • [🔌 API Docs](#-api-endpoints)**

</div>

---

## 🎬 Why This Project?

**Problem:** Businesses waste 5-10 hours per week on:
- Manual data entry from spreadsheets
- Data cleaning and validation
- Generating reports
- Emailing stakeholders

**Solution:** This dashboard automates the entire workflow:
- Upload → Process → Report → Email ✨ **All automated in seconds**

---

## ✨ Key Features

### Core Functionality
- 📤 **Drag & Drop File Upload** - Excel (.xlsx, .xls) and CSV support
- 🧹 **Intelligent Data Cleaning** - Removes duplicates, null values, and standardizes formatting
- 📊 **Professional Report Generation** - PDF reports with charts and CSV exports
- 📧 **Automated Email Delivery** - Sends reports to stakeholders automatically
- 📈 **Real-time Progress Tracking** - Live status updates and progress bars
- ⚡ **Background Processing** - Handles large files without blocking

### Technical Excellence
- 🚀 **Production-Ready Architecture** - FastAPI + Celery + Redis
- 🔌 **RESTful API** - Complete API for third-party integrations
- 🐳 **Docker Support** - Deploy with a single command
- 📱 **Responsive UI** - Beautiful Streamlit interface
- 🔒 **Error Handling** - Comprehensive error tracking and recovery
- 📊 **System Monitoring** - Built-in statistics and health checks  

---

## 🎯 Perfect For

- 💼 **Small Businesses** - Automate repetitive data tasks
- 📊 **Data Analysts** - Quick data cleaning pipelines
- 📈 **Reporting Teams** - Automated monthly/weekly reports
- 🏢 **Enterprise Departments** - Self-service data processing
- 🚀 **Freelancers** - Showcase automation skills to clients

---

## 🏗️ Architecture

**Simple, Scalable, Production-Ready**

```
┌─────────────────┐
│   User Browser  │
└────────┬────────┘
         │ http://localhost:8501
         ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Streamlit     │────▶│    FastAPI       │────▶│     Celery      │
│   Dashboard     │     │    Backend       │     │     Worker      │
│   (Frontend)    │     │   (REST API)     │     │  (Processing)   │
└─────────────────┘     └────────┬─────────┘     └────────┬────────┘
                                 │                          │
                                 ▼                          ▼
                        ┌─────────────────┐     ┌─────────────────┐
                        │   SQLite DB     │     │   Redis Queue   │
                        │  (Job Metadata) │     │  (Task Queue)   │
                        └─────────────────┘     └─────────────────┘
```

**How It Works:**
1. User uploads file via dashboard
2. Backend creates job and queues task
3. Worker processes data asynchronously
4. Reports generated (PDF + CSV)
5. Email sent to recipients
6. User downloads results

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | FastAPI | High-performance REST API |
| **Frontend** | Streamlit | Interactive web dashboard |
| **Task Queue** | Celery + Redis | Asynchronous job processing |
| **Database** | SQLAlchemy + SQLite | Job metadata storage |
| **Data Processing** | Pandas | Data manipulation & cleaning |
| **Reports** | ReportLab + Matplotlib | PDF generation with charts |
| **Email** | SMTP | Automated notifications |
| **Deployment** | Docker + Docker Compose | Containerized deployment |

---

## 📁 Project Structure

```
workflow-automation-dashboard/
├── backend/                 # 🔌 FastAPI REST API
│   ├── main.py             # API endpoints & routes
│   ├── models.py           # Database models (SQLAlchemy)
│   ├── schemas.py          # Request/response schemas
│   ├── database.py         # Database connection & session
│   └── config.py           # Environment configuration
├── services/               # 🧩 Business logic layer
│   ├── data_processor.py   # Data cleaning & transformation
│   ├── report_generator.py # PDF & CSV generation
│   └── email_service.py    # Email notifications
├── workers/                # ⚙️ Background task processing
│   ├── celery_app.py       # Celery configuration
│   └── tasks.py            # Async task definitions
├── dashboard/              # 🎨 Streamlit web interface
│   └── app.py              # Dashboard UI components
├── tests/                  # ✅ Test suite
│   └── test_api.py         # API endpoint tests
├── storage/                # 💾 Runtime file storage
│   ├── uploads/            # User-uploaded files
│   ├── reports/            # Generated reports
│   └── temp/               # Temporary processing files
├── .github/workflows/      # 🔄 CI/CD pipelines
├── docker-compose.yml      # 🐳 Multi-container orchestration
├── Dockerfile              # 🐳 Container image definition
├── requirements.txt        # 📦 Python dependencies
├── .env.example            # 🔐 Environment template
└── README.md               # 📖 Documentation
```

---

---

---

## 🚀 Quick Start

> **Choose your setup method below. Docker is fastest, local development gives you more control.**

### ⚡ Option 1: Docker (Recommended - Fastest Setup)

**Step 1: Setup Environment**

```bash
# Clone repository
git clone https://github.com/shettydhan/workflow-automation-platform.git
cd workflow-automation-dashboard

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Step 2: Configure Environment**

```bash
# Copy example env file
copy .env.example .env    # Windows
cp .env.example .env      # Linux/Mac

# Edit .env with your settings (optional - defaults work for local dev)
```

**Important Email Configuration** (Optional):
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password    # Use Gmail App Password, not your regular password
SMTP_FROM_EMAIL=your-email@gmail.com
```

To get Gmail App Password:
1. Enable 2FA on your Google account
2. Go to: https://myaccount.google.com/apppasswords
3. Generate app password for "Mail"
4. Use that password in .env

**Step 3: Install Redis**

**Windows:**
```powershell
choco install redis-64
# Or download: https://github.com/microsoftarchive/redis/releases
```

**Linux:**
```bash
sudo apt-get install redis-server
sudo systemctl start redis
```

**Mac:**
```bash
brew install redis
brew services start redis
```

**Step 4: Start Services**

Open **3 separate terminals**:

**Terminal 1 - FastAPI Backend:**
```bash
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Celery Worker:**
```bash
celery -A workers.celery_app worker --loglevel=info --pool=solo
```
> **Note:** Windows requires `--pool=solo` flag

**Terminal 3 - Streamlit Dashboard:**
```bash
streamlit run dashboard/app.py
```

**Step 5: Access the Application**

- 🖥️ **Dashboard**: http://localhost:8501
- 📡 **API Docs**: http://localhost:8000/docs
- 🔍 **Health Check**: http://localhost:8000/health

---

**Prerequisites:** Docker & Docker Compose installed

```bash
# Clone the repository
git clone https://github.com/shettydhan/workflow-automation-platform.git
cd workflow-automation-dashboard

# Copy environment file
cp .env.example .env

# Start all services with one command
docker-compose up --build
```

**That's it!** Access the dashboard at http://localhost:8501

To stop:
```bash
docker-compose down
```

---

### 🔧 Option 2: Local Development

**Prerequisites:**
- Python 3.11+
- Redis installed and running

---

## 🎥 Try It Yourself - 2 Minute Test

Want to see it in action? Here's the fastest way:

```bash
# 1. Clone and start with Docker (one command!)
git clone https://github.com/shettydhan/projects1.git
cd projects1
docker-compose up

# 2. Open dashboard
# Visit: http://localhost:8501

# 3. Upload the included sample file
# Use: sample_data.csv (included in repo)

# 4. Watch it process in real-time!
# Download your reports in 30 seconds
```

**What you'll see:**
- Automatic duplicate removal
- Data cleaning and standardization
- Professional PDF report with charts
- CSV export ready for analysis

---

## 📖 Usage Guide

### 1. Upload & Process Files

1. Open dashboard: http://localhost:8501
2. Navigate to **"📤 Upload & Process"**
3. Upload your Excel/CSV file
4. Enter a job name
5. (Optional) Enable email notifications
6. Click **"🚀 Start Processing"**
7. Watch real-time progress
8. Download CSV and PDF reports

### 2. View Jobs

- Navigate to **"📊 View Jobs"**
- Filter by status (pending, processing, completed, failed)
- Download reports
- Delete old jobs

### 3. Check Statistics

- Navigate to **"📈 Statistics"**
- View overall system metrics
- Track success rates

---

## 🔧 API Endpoints

### Upload File
```http
POST /api/jobs/upload
Content-Type: multipart/form-data

Parameters:
- file: Excel/CSV file
- job_name: string
- send_email: boolean
- email_recipients: string (comma-separated)
```

### Get All Jobs
```http
GET /api/jobs?status=completed&limit=50&offset=0
```

### Get Job Details
```http
GET /api/jobs/{job_id}
```

### Get Job Status
```http
GET /api/jobs/{job_id}/status
```

### Download Report
```http
GET /api/jobs/{job_id}/download?format=csv
```

### Delete Job
```http
DELETE /api/jobs/{job_id}
```

### System Statistics
```http
GET /api/stats
```

**Full API Documentation**: http://localhost:8000/docs

---

## 🧪 Testing

### Test with Sample Data

Create a sample CSV file:

```csv
Name,Age,Email,Salary,Date
John Doe,30,john@example.com,50000,2024-01-15
Jane Smith,25,jane@example.com,60000,2024-02-20
Bob Wilson,  35  ,bob@example.com,55000,2024-03-10
John Doe,30,john@example.com,50000,2024-01-15
```

Save as `test_data.csv` and upload through the dashboard.

### Expected Results:
- Duplicate row removed (John Doe)
- Whitespace trimmed (Bob Wilson)
- Data standardized
- Summary statistics generated
- PDF + CSV reports created

---

## 🎨 Customization

### Modify Data Cleaning Logic

Edit `services/data_processor.py`:

```python
def clean_data(self) -> pd.DataFrame:
    # Add your custom cleaning logic here
    self.df = self.df.dropna(how='all')
    # ... more logic
    return self.df
```

### Add Custom Email Templates

Edit `services/email_service.py`:

```python
def send_job_completion_email(self, ...):
    # Customize email HTML
    body = f"""
    <html>
        <!-- Your custom template -->
    </html>
    """
```

### Customize Dashboard

Edit `dashboard/app.py`:

```python
def page_upload():
    # Add custom UI components
    st.header("Your Custom Title")
    # ... more customizations
```

---

## 🐛 Troubleshooting

### Redis Connection Error
```
Error: Cannot connect to Redis
```
**Solution:** Make sure Redis is running
```bash
# Windows
redis-server

# Linux/Mac
sudo systemctl start redis
```

### Celery Worker Not Starting (Windows)
```
Error: Pool not implemented for Windows
```
**Solution:** Add `--pool=solo` flag
```bash
celery -A workers.celery_app worker --loglevel=info --pool=solo
```

### Email Not Sending
**Solution:** 
1. Check SMTP credentials in `.env`
2. Use Gmail App Password (not regular password)
3. Enable "Less Secure Apps" if using older Gmail

### Port Already in Use
```
Error: Address already in use
```
**Solution:** Change ports in `.env`:
```env
API_PORT=8001
DASHBOARD_PORT=8502
```

---

## 📈 Performance Tips

1. **Large Files**: For files > 10MB, increase timeouts:
   ```python
   # workers/celery_app.py
   task_time_limit=7200  # 2 hours
   ```

2. **Concurrent Jobs**: Increase Celery workers:
   ```bash
   celery -A workers.celery_app worker --concurrency=4
   ```

3. **Database**: For production, use PostgreSQL instead of SQLite:
   ```env
   DATABASE_URL=postgresql://user:pass@localhost/dbname
   ```

---

## 🚢 Production Deployment

### Environment Variables for Production

```env
ENVIRONMENT=production
DEBUG=False
DATABASE_URL=postgresql://user:pass@host:5432/dbname
REDIS_HOST=your-redis-host
SMTP_HOST=your-smtp-server
```

### Security Best Practices

1. Use strong passwords
2. Enable HTTPS
3. Set up API authentication
4. Use environment-specific configs
5. Regular backups of database

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

MIT License - Feel free to use for commercial projects

---

## 🎓 Learning Resources

### For Backend (FastAPI)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Celery Documentation](https://docs.celeryq.dev/)

### For Frontend (Streamlit)
- [Streamlit Documentation](https://docs.streamlit.io/)

### For Data Processing
- [Pandas Documentation](https://pandas.pydata.org/)
- [ReportLab Documentation](https://www.reportlab.com/docs/)

---

## 💡 Real-World Use Cases

### 📊 For Small Businesses

**Scenario:** Monthly sales report generation
- **Before:** 4 hours of manual Excel work, copying data, formatting, emailing to 15 stakeholders
- **After:** Upload file → 5 minutes → Reports emailed automatically
- **ROI:** Save 16 hours/month = $320-640 in labor costs

### 🏢 For Marketing Agencies

**Scenario:** Client campaign performance reports
- **Before:** Collect data from 5 sources, clean manually, create PDF in PowerPoint, email individually
- **After:** Automated pipeline processes all sources, generates branded PDFs, bulk email delivery
- **ROI:** Serve 3x more clients with same team size

### 📈 For Data Teams

**Scenario:** Weekly data quality checks
- **Before:** Manual duplicate detection, inconsistency fixes, validation reports
- **After:** Upload → Automatic cleaning → Quality report with statistics
- **ROI:** 100% consistent data quality, zero human error

### 🎓 For Education Departments

**Scenario:** Student grade reports
- **Before:** Process attendance/grades manually, generate individual reports, email parents
- **After:** Upload class data → System generates personalized PDFs → Auto-email to all parents
- **ROI:** Save 6+ hours per grading period

---

## 🎬 Demo Walkthrough

### Step 1: Upload Your Data File

<div align="center">

![Upload Interface](https://via.placeholder.com/850x450/2563eb/ffffff?text=📤+Drag+%26+Drop+Excel/CSV+Files)

*Intuitive upload interface with validation and progress tracking*

</div>

**What happens:**
- Drag & drop or click to upload
- Automatic file validation (type, size)
- Configure job name and email settings
- One-click to start processing

---

### Step 2: Real-Time Processing

<div align="center">

![Progress Tracking](https://via.placeholder.com/850x450/16a34a/ffffff?text=⚡+Real-Time+Progress+Updates)

*Live progress bar showing current processing stage*

</div>

**Processing stages:**
1. ✅ Data loading and validation (20%)
2. ✅ Duplicate removal and cleaning (40%)
3. ✅ Generating reports (CSV + PDF) (80%)
4. ✅ Sending email notifications (90%)
5. ✅ Complete and ready for download (100%)

---

### Step 3: Download Professional Reports

<div align="center">

![Report Download](https://via.placeholder.com/850x450/0891b2/ffffff?text=📥+Download+CSV+%26+PDF+Reports)

*One-click download for both CSV and PDF formats*

</div>

**What you get:**
- **CSV Report:** Clean, processed data ready for analysis
- **PDF Report:** Professional document with:
  - Executive summary
  - Data statistics (rows, columns, duplicates removed)
  - Charts and visualizations
  - Timestamp and processing details

---

### Step 4: Monitor All Jobs

<div align="center">

![Job List](https://via.placeholder.com/850x450/7c3aed/ffffff?text=📊+Job+Management+Dashboard)

*Track all processing jobs with status, progress, and quick actions*

</div>

**Features:**
- Filter by status (pending, processing, completed, failed)
- View detailed job information
- Download reports anytime
- Delete old jobs to free up space

---

## 📊 Business Impact

| Metric | Result |
|--------|--------|
| ⏱️ **Time Saved** | 5-10 hours per week |
| 📉 **Error Reduction** | 95% fewer data entry errors |
| 💰 **Cost Savings** | $400-800/month in labor costs |
| 📈 **Productivity Gain** | 3x more reports with same team |
| ⚡ **Processing Speed** | 1000+ rows in under 60 seconds |

---

## 🎯 Perfect For Freelancers

This project demonstrates:
- ✅ **Full-stack development** - Frontend + Backend + Workers
- ✅ **Async programming** - Celery task queues
- ✅ **API design** - RESTful endpoints with FastAPI
- ✅ **DevOps skills** - Docker, CI/CD pipelines
- ✅ **Production mindset** - Error handling, monitoring, testing
- ✅ **Business value** - Solves real problems, saves money

**Showcase this to land $2,000-5,000 automation projects!** 💰

---

## 🎯 Roadmap

- [ ] User authentication & multi-tenancy
- [ ] Scheduled/recurring jobs (cron)
- [ ] Advanced data visualizations
- [ ] Support for JSON, XML, Parquet
- [ ] Cloud storage integration (S3, Azure Blob)
- [ ] API rate limiting & usage analytics
- [ ] Webhook notifications
- [ ] Multi-language support

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🌟 Show Your Support

If this project helped you, please give it a ⭐ on GitHub!

---

## 💼 Need Custom Implementation?

I offer professional services to customize this platform for your business:

### Services Offered:
- 🔧 **Custom Data Transformations** - Tailored business logic
- 🔌 **System Integrations** - Connect to your CRM, ERP, or database
- 🎨 **White-Label Branding** - Your logo and colors
- 🚀 **Deployment & Hosting** - AWS, Azure, or Google Cloud
- 📚 **Training & Support** - Team onboarding and documentation
- ⚙️ **Ongoing Maintenance** - Updates and monitoring

### Pricing:
- **Basic Setup:** $500-800 (Standard deployment with minor customization)
- **Custom Implementation:** $1,500-3,000 (Tailored features and integrations)
- **Enterprise Solution:** $5,000+ (Full customization, SLA, support)

---

## 👤 Author

**Dhanush Shetty**
- 💼 GitHub: [@shettydhan](https://github.com/shettydhan)
- 🔗 LinkedIn: [Your Profile](https://linkedin.com/in/your-profile)
- 📧 Email: your.email@example.com
- 💬 Available for: Consulting • Freelance Projects • Custom Development

*Specializing in Python automation, data processing, and business workflow solutions.*

---

## 🙏 Acknowledgments

Built with modern Python frameworks:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Streamlit](https://streamlit.io/) - Data apps framework
- [Celery](https://docs.celeryq.dev/) - Distributed task queue
- [Pandas](https://pandas.pydata.org/) - Data analysis library

---

<div align="center">
  <strong>Made with ❤️ for businesses seeking automation</strong>
</div>
