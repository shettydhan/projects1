"""
Database models
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Enum as SQLEnum
from backend.database import Base
import enum


class JobStatus(str, enum.Enum):
    """Job status enumeration"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Job(Base):
    """Job model to track processing tasks"""
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Job identification
    job_id = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    
    # File information
    input_file = Column(String(500), nullable=False)
    input_file_name = Column(String(255), nullable=False)
    output_file = Column(String(500), nullable=True)
    
    # Status tracking
    status = Column(SQLEnum(JobStatus), default=JobStatus.PENDING, nullable=False)
    progress = Column(Float, default=0.0)  # 0-100
    
    # Processing details
    total_rows = Column(Integer, default=0)
    processed_rows = Column(Integer, default=0)
    error_rows = Column(Integer, default=0)
    
    # Metadata
    celery_task_id = Column(String(100), nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Email configuration
    email_recipients = Column(String(500), nullable=True)  # Comma-separated
    send_email = Column(Integer, default=0)  # 0=No, 1=Yes
    email_sent = Column(Integer, default=0)  # 0=No, 1=Yes
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<Job {self.job_id} - {self.status}>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "job_id": self.job_id,
            "name": self.name,
            "status": self.status.value,
            "progress": self.progress,
            "total_rows": self.total_rows,
            "processed_rows": self.processed_rows,
            "error_rows": self.error_rows,
            "input_file_name": self.input_file_name,
            "output_file": self.output_file,
            "error_message": self.error_message,
            "send_email": bool(self.send_email),
            "email_sent": bool(self.email_sent),
            "email_recipients": self.email_recipients,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
