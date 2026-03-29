"""
FastAPI main application
"""
import uuid
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, List
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Form, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from backend.database import get_db, init_db
from backend.models import Job, JobStatus
from backend.schemas import (
    JobCreate, JobResponse, JobListResponse, 
    JobStatusResponse, HealthCheckResponse
)
from backend.config import settings
from workers.tasks import process_data_job

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="Business Workflow Automation Dashboard API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print(f"✅ {settings.app_name} started successfully!")
    print(f"📡 API running on http://{settings.api_host}:{settings.api_port}")


@app.get("/", response_model=HealthCheckResponse)
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "1.0.0"
    }


@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "1.0.0"
    }


@app.post("/api/jobs/upload", response_model=JobResponse)
async def upload_file(
    file: UploadFile = File(...),
    job_name: str = Form(...),
    send_email: bool = Form(False),
    email_recipients: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Upload a file and create a new processing job
    
    - **file**: Excel or CSV file to process
    - **job_name**: Name for this job
    - **send_email**: Whether to send email on completion
    - **email_recipients**: Comma-separated email addresses
    """
    try:
        # Validate file extension
        file_ext = Path(file.filename).suffix.lower().replace('.', '')
        if file_ext not in settings.allowed_extensions_list:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed: {', '.join(settings.allowed_extensions_list)}"
            )
        
        # Validate file size (read in chunks to avoid memory issues)
        file_size = 0
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset to beginning
        
        max_size = settings.max_file_size_mb * 1024 * 1024
        if file_size > max_size:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {settings.max_file_size_mb}MB"
            )
        
        # Generate unique job ID
        job_id = str(uuid.uuid4())
        
        # Save uploaded file
        file_path = settings.upload_dir / f"{job_id}_{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Create job record
        job = Job(
            job_id=job_id,
            name=job_name,
            input_file=str(file_path),
            input_file_name=file.filename,
            status=JobStatus.PENDING,
            send_email=1 if send_email else 0,
            email_recipients=email_recipients if email_recipients else None
        )
        
        db.add(job)
        db.commit()
        db.refresh(job)
        
        # Queue background task
        task = process_data_job.delay(job_id)
        
        # Update with task ID
        job.celery_task_id = task.id
        db.commit()
        
        return job.to_dict()
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/jobs", response_model=JobListResponse)
async def list_jobs(
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(50, ge=1, le=100, description="Number of jobs to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    db: Session = Depends(get_db)
):
    """
    List all jobs with optional filtering
    
    - **status**: Filter by status (pending, processing, completed, failed)
    - **limit**: Maximum number of jobs to return (default: 50)
    - **offset**: Number of jobs to skip (for pagination)
    """
    try:
        query = db.query(Job)
        
        # Filter by status if provided
        if status:
            try:
                status_enum = JobStatus(status.lower())
                query = query.filter(Job.status == status_enum)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid status. Must be one of: {', '.join([s.value for s in JobStatus])}"
                )
        
        # Get total count
        total = query.count()
        
        # Apply pagination and ordering
        jobs = query.order_by(Job.created_at.desc()).offset(offset).limit(limit).all()
        
        return {
            "total": total,
            "jobs": [job.to_dict() for job in jobs]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/jobs/{job_id}", response_model=JobResponse)
async def get_job(job_id: str, db: Session = Depends(get_db)):
    """
    Get details of a specific job
    
    - **job_id**: Unique job identifier
    """
    try:
        job = db.query(Job).filter(Job.job_id == job_id).first()
        
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return job.to_dict()
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/jobs/{job_id}/status", response_model=JobStatusResponse)
async def get_job_status(job_id: str, db: Session = Depends(get_db)):
    """
    Get current status of a job (lightweight endpoint for polling)
    
    - **job_id**: Unique job identifier
    """
    try:
        job = db.query(Job).filter(Job.job_id == job_id).first()
        
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        message = None
        if job.status == JobStatus.FAILED:
            message = job.error_message
        elif job.status == JobStatus.COMPLETED:
            message = "Job completed successfully"
        
        return {
            "job_id": job.job_id,
            "status": job.status.value,
            "progress": job.progress,
            "message": message
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/jobs/{job_id}/download")
async def download_report(
    job_id: str,
    format: str = Query("csv", description="Report format (csv or pdf)"),
    db: Session = Depends(get_db)
):
    """
    Download the generated report
    
    - **job_id**: Unique job identifier
    - **format**: Report format (csv or pdf)
    """
    try:
        job = db.query(Job).filter(Job.job_id == job_id).first()
        
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        if job.status != JobStatus.COMPLETED:
            raise HTTPException(
                status_code=400,
                detail=f"Job not completed. Current status: {job.status.value}"
            )
        
        if not job.output_file:
            raise HTTPException(status_code=404, detail="Report file not found")
        
        # Determine file path based on format
        if format.lower() == "csv":
            file_path = Path(job.output_file)
        elif format.lower() == "pdf":
            file_path = Path(job.output_file).with_suffix('.pdf')
        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid format. Must be 'csv' or 'pdf'"
            )
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail=f"{format.upper()} file not found")
        
        return FileResponse(
            path=str(file_path),
            filename=file_path.name,
            media_type='application/octet-stream'
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/jobs/{job_id}")
async def delete_job(job_id: str, db: Session = Depends(get_db)):
    """
    Delete a job and its associated files
    
    - **job_id**: Unique job identifier
    """
    try:
        job = db.query(Job).filter(Job.job_id == job_id).first()
        
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Delete associated files
        try:
            if job.input_file and Path(job.input_file).exists():
                Path(job.input_file).unlink()
            
            if job.output_file:
                csv_path = Path(job.output_file)
                pdf_path = csv_path.with_suffix('.pdf')
                
                if csv_path.exists():
                    csv_path.unlink()
                if pdf_path.exists():
                    pdf_path.unlink()
        except Exception as e:
            print(f"Warning: Could not delete files: {str(e)}")
        
        # Delete job record
        db.delete(job)
        db.commit()
        
        return {"message": f"Job {job_id} deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get overall system statistics"""
    try:
        total_jobs = db.query(Job).count()
        pending_jobs = db.query(Job).filter(Job.status == JobStatus.PENDING).count()
        processing_jobs = db.query(Job).filter(Job.status == JobStatus.PROCESSING).count()
        completed_jobs = db.query(Job).filter(Job.status == JobStatus.COMPLETED).count()
        failed_jobs = db.query(Job).filter(Job.status == JobStatus.FAILED).count()
        
        return {
            "total_jobs": total_jobs,
            "pending": pending_jobs,
            "processing": processing_jobs,
            "completed": completed_jobs,
            "failed": failed_jobs
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
