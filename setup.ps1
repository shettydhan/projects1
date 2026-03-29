# Setup Script for Workflow Automation Dashboard
Write-Host "🔧 Setting up Workflow Automation Dashboard..." -ForegroundColor Green
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Cyan
python --version

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python not found. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Create virtual environment
if (Test-Path "venv") {
    Write-Host "✅ Virtual environment already exists" -ForegroundColor Green
} else {
    Write-Host "Creating virtual environment..." -ForegroundColor Cyan
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& .\venv\Scripts\Activate.ps1

Write-Host "✅ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Create .env file if not exists
if (Test-Path ".env") {
    Write-Host "✅ .env file already exists" -ForegroundColor Green
} else {
    Write-Host "Creating .env file from template..." -ForegroundColor Cyan
    Copy-Item .env.example .env
    Write-Host "✅ .env file created (please configure SMTP settings)" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Make sure Redis is running" -ForegroundColor White
Write-Host "2. Open 3 terminals and run:" -ForegroundColor White
Write-Host "   Terminal 1: .\start_backend.ps1" -ForegroundColor Yellow
Write-Host "   Terminal 2: .\start_worker.ps1" -ForegroundColor Yellow
Write-Host "   Terminal 3: .\start_dashboard.ps1" -ForegroundColor Yellow
Write-Host ""
Write-Host "3. Open browser: http://localhost:8501" -ForegroundColor White
Write-Host ""
