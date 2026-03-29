# Start FastAPI Backend
Write-Host "🚀 Starting FastAPI Backend..." -ForegroundColor Green
Write-Host "API will be available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "" 

python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
