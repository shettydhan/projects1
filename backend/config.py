"""
Configuration management for the application
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings"""
    
    def __init__(self):
        # Application
        self.app_name = os.getenv("APP_NAME", "Workflow Automation Dashboard")
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.debug = os.getenv("DEBUG", "True").lower() == "true"
        
        # API Configuration
        self.api_host = os.getenv("API_HOST", "0.0.0.0")
        self.api_port = int(os.getenv("API_PORT", "8000"))
        
        # Database
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///./workflow_automation.db")
        
        # Redis & Celery
        self.redis_host = os.getenv("REDIS_HOST", "localhost")
        self.redis_port = int(os.getenv("REDIS_PORT", "6379"))
        self.redis_db = int(os.getenv("REDIS_DB", "0"))
        self.celery_broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
        self.celery_result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
        
        # Email Configuration
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.smtp_from_email = os.getenv("SMTP_FROM_EMAIL", "")
        self.smtp_from_name = os.getenv("SMTP_FROM_NAME", "Automation System")
        
        # Storage Paths
        self.upload_dir = Path(os.getenv("UPLOAD_DIR", "./storage/uploads"))
        self.report_dir = Path(os.getenv("REPORT_DIR", "./storage/reports"))
        self.temp_dir = Path(os.getenv("TEMP_DIR", "./storage/temp"))
        
        # File Upload Limits
        self.max_file_size_mb = int(os.getenv("MAX_FILE_SIZE_MB", "50"))
        self.allowed_extensions = os.getenv("ALLOWED_EXTENSIONS", "csv,xlsx,xls")
        
        # Create directories if they don't exist
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.report_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    @property
    def allowed_extensions_list(self):
        """Get allowed extensions as a list"""
        return [ext.strip() for ext in self.allowed_extensions.split(",")]


# Global settings instance
settings = Settings()
