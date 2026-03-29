"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class JobCreate(BaseModel):
    """Schema for creating a new job"""
    name: str = Field(..., min_length=1, max_length=255, description="Job name")
    email_recipients: Optional[str] = Field(None, description="Comma-separated email addresses")
    send_email: bool = Field(default=False, description="Whether to send email on completion")


class JobResponse(BaseModel):
    """Schema for job response"""
    id: int
    job_id: str
    name: str
    status: str
    progress: float
    total_rows: int
    processed_rows: int
    error_rows: int
    input_file_name: str
    output_file: Optional[str]
    error_message: Optional[str]
    send_email: bool
    email_sent: bool
    email_recipients: Optional[str]
    created_at: Optional[str]
    started_at: Optional[str]
    completed_at: Optional[str]
    
    class Config:
        from_attributes = True


class JobListResponse(BaseModel):
    """Schema for listing jobs"""
    total: int
    jobs: List[JobResponse]


class JobStatusResponse(BaseModel):
    """Schema for job status check"""
    job_id: str
    status: str
    progress: float
    message: Optional[str] = None


class HealthCheckResponse(BaseModel):
    """Schema for health check"""
    status: str
    timestamp: datetime
    version: str = "1.0.0"
