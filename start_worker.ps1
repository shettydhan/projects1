# Start Celery Worker
Write-Host "⚙️  Starting Celery Worker..." -ForegroundColor Green
Write-Host "Make sure Redis is running first!" -ForegroundColor Yellow
Write-Host ""

celery -A workers.celery_app worker --loglevel=info --pool=solo
