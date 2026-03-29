"""
Celery background tasks
"""
import logging
from datetime import datetime
from pathlib import Path
from workers.celery_app import celery_app
from services.data_processor import DataProcessor
from services.report_generator import ReportGenerator
from services.email_service import EmailService
from backend.database import SessionLocal
from backend.models import Job, JobStatus
from backend.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name='workers.tasks.process_data_job')
def process_data_job(self, job_id: str):
    """
    Main background task to process data
    
    Steps:
    1. Load and clean data
    2. Generate summary
    3. Create reports (CSV + PDF)
    4. Send email (if configured)
    5. Update job status
    """
    db = SessionLocal()
    
    try:
        # Get job from database
        job = db.query(Job).filter(Job.job_id == job_id).first()
        if not job:
            raise ValueError(f"Job {job_id} not found")
        
        logger.info(f"Starting processing for job: {job_id}")
        
        # Update job status
        job.status = JobStatus.PROCESSING
        job.started_at = datetime.utcnow()
        job.celery_task_id = self.request.id
        job.progress = 5.0
        db.commit()
        
        # Step 1: Load and clean data
        logger.info(f"Step 1: Loading file {job.input_file}")
        processor = DataProcessor()
        processor.load_file(job.input_file)
        
        job.total_rows = len(processor.df)
        job.progress = 20.0
        db.commit()
        
        # Step 2: Clean data
        logger.info("Step 2: Cleaning data")
        processor.clean_data()
        
        job.processed_rows = len(processor.df)
        job.error_rows = job.total_rows - job.processed_rows
        job.progress = 40.0
        db.commit()
        
        # Step 3: Generate summary
        logger.info("Step 3: Generating summary")
        summary = processor.generate_summary()
        stats = processor.get_stats()
        
        job.progress = 60.0
        db.commit()
        
        # Step 4: Generate reports
        logger.info("Step 4: Generating reports")
        report_generator = ReportGenerator()
        
        # Add completion timestamp to stats
        stats['completed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        stats['job_name'] = job.name
        
        reports = report_generator.generate_complete_report(
            df=processor.df,
            output_dir=str(settings.report_dir),
            job_name=job.name.replace(' ', '_'),
            stats=stats,
            summary=summary
        )
        
        # Store output file path (CSV)
        job.output_file = reports['csv']
        job.progress = 80.0
        db.commit()
        
        logger.info(f"Reports generated: {reports}")
        
        # Step 5: Send email (if configured)
        if job.send_email and job.email_recipients:
            logger.info("Step 5: Sending email")
            
            email_service = EmailService()
            recipient_list = [email.strip() for email in job.email_recipients.split(',')]
            
            # Send both CSV and PDF
            attachments = [reports['csv'], reports['pdf']]
            
            email_sent = email_service.send_job_completion_email(
                to_emails=recipient_list,
                job_name=job.name,
                stats=stats,
                report_files=attachments
            )
            
            job.email_sent = 1 if email_sent else 0
            
            if email_sent:
                logger.info(f"Email sent to: {job.email_recipients}")
            else:
                logger.warning("Email sending failed or not configured")
        
        # Step 6: Mark as completed
        job.status = JobStatus.COMPLETED
        job.completed_at = datetime.utcnow()
        job.progress = 100.0
        db.commit()
        
        logger.info(f"Job {job_id} completed successfully")
        
        return {
            'status': 'completed',
            'job_id': job_id,
            'output_file': job.output_file,
            'stats': stats
        }
    
    except Exception as e:
        logger.error(f"Error processing job {job_id}: {str(e)}")
        
        # Update job status to failed
        try:
            job = db.query(Job).filter(Job.job_id == job_id).first()
            if job:
                job.status = JobStatus.FAILED
                job.error_message = str(e)
                job.completed_at = datetime.utcnow()
                db.commit()
                
                # Send failure email if configured
                if job.send_email and job.email_recipients:
                    email_service = EmailService()
                    recipient_list = [email.strip() for email in job.email_recipients.split(',')]
                    email_service.send_job_failure_email(
                        to_emails=recipient_list,
                        job_name=job.name,
                        error_message=str(e)
                    )
        except Exception as db_error:
            logger.error(f"Error updating job status: {str(db_error)}")
        
        raise
    
    finally:
        db.close()


@celery_app.task(name='workers.tasks.cleanup_old_files')
def cleanup_old_files(days_old: int = 7):
    """
    Cleanup task to remove old files
    Can be scheduled with Celery Beat
    """
    try:
        from datetime import timedelta
        import os
        
        now = datetime.now()
        cutoff_date = now - timedelta(days=days_old)
        
        # Cleanup directories
        directories = [settings.upload_dir, settings.report_dir, settings.temp_dir]
        
        total_deleted = 0
        for directory in directories:
            if directory.exists():
                for file_path in directory.iterdir():
                    if file_path.is_file():
                        file_modified = datetime.fromtimestamp(file_path.stat().st_mtime)
                        if file_modified < cutoff_date:
                            file_path.unlink()
                            total_deleted += 1
                            logger.info(f"Deleted old file: {file_path}")
        
        logger.info(f"Cleanup completed. Deleted {total_deleted} files older than {days_old} days")
        return {'deleted_files': total_deleted}
    
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")
        raise
