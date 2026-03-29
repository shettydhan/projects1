"""
Email automation service
"""
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from pathlib import Path
from typing import List, Optional
from backend.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending automated emails"""
    
    def __init__(self):
        self.smtp_host = settings.smtp_host
        self.smtp_port = settings.smtp_port
        self.smtp_username = settings.smtp_username
        self.smtp_password = settings.smtp_password
        self.from_email = settings.smtp_from_email
        self.from_name = settings.smtp_from_name
    
    def send_email(
        self,
        to_emails: List[str],
        subject: str,
        body: str,
        attachments: Optional[List[str]] = None,
        html: bool = True
    ) -> bool:
        """
        Send email with optional attachments
        
        Args:
            to_emails: List of recipient email addresses
            subject: Email subject
            body: Email body (can be HTML if html=True)
            attachments: List of file paths to attach
            html: Whether body is HTML (default: True)
        
        Returns:
            bool: True if sent successfully
        """
        try:
            # Validate configuration
            if not self.smtp_username or not self.smtp_password:
                logger.warning("Email credentials not configured. Skipping email.")
                return False
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = ', '.join(to_emails)
            msg['Subject'] = subject
            
            # Attach body
            if html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            # Attach files
            if attachments:
                for file_path in attachments:
                    file_path = Path(file_path)
                    if file_path.exists():
                        with open(file_path, 'rb') as f:
                            part = MIMEApplication(f.read(), Name=file_path.name)
                            part['Content-Disposition'] = f'attachment; filename="{file_path.name}"'
                            msg.attach(part)
                    else:
                        logger.warning(f"Attachment not found: {file_path}")
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to: {', '.join(to_emails)}")
            return True
        
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False
    
    def send_job_completion_email(
        self,
        to_emails: List[str],
        job_name: str,
        stats: dict,
        report_files: List[str]
    ) -> bool:
        """
        Send job completion notification with reports attached
        
        Args:
            to_emails: List of recipient emails
            job_name: Name of the completed job
            stats: Processing statistics
            report_files: List of report file paths
        
        Returns:
            bool: True if sent successfully
        """
        subject = f"✅ Workflow Automation Complete: {job_name}"
        
        # Create HTML body
        body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #1f77b4; color: white; padding: 20px; text-align: center; border-radius: 5px; }}
                .content {{ background-color: #f9f9f9; padding: 20px; margin-top: 20px; border-radius: 5px; }}
                .stats {{ background-color: white; padding: 15px; margin: 15px 0; border-left: 4px solid #1f77b4; }}
                .stat-item {{ margin: 8px 0; }}
                .stat-label {{ font-weight: bold; color: #555; }}
                .footer {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #777; }}
                .success {{ color: #28a745; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 Job Completed Successfully!</h1>
                </div>
                
                <div class="content">
                    <p>Hello,</p>
                    <p>Your workflow automation job "<strong>{job_name}</strong>" has been processed successfully.</p>
                    
                    <div class="stats">
                        <h3>📊 Processing Summary:</h3>
        """
        
        # Add statistics
        for key, value in stats.items():
            formatted_key = key.replace('_', ' ').title()
            body += f'<div class="stat-item"><span class="stat-label">{formatted_key}:</span> {value}</div>'
        
        body += """
                    </div>
                    
                    <p>The processed data and reports are attached to this email.</p>
                    
                    <h3>📎 Attached Files:</h3>
                    <ul>
        """
        
        # List attachments
        for file_path in report_files:
            filename = Path(file_path).name
            body += f"<li>{filename}</li>"
        
        body += f"""
                    </ul>
                    
                    <p class="success">✅ All processing completed successfully!</p>
                </div>
                
                <div class="footer">
                    <p>This is an automated message from Workflow Automation Dashboard.</p>
                    <p>Generated at: {stats.get('completed_at', 'N/A')}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(
            to_emails=to_emails,
            subject=subject,
            body=body,
            attachments=report_files,
            html=True
        )
    
    def send_job_failure_email(
        self,
        to_emails: List[str],
        job_name: str,
        error_message: str
    ) -> bool:
        """
        Send job failure notification
        """
        subject = f"❌ Workflow Automation Failed: {job_name}"
        
        body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #dc3545; color: white; padding: 20px; text-align: center; border-radius: 5px; }}
                .content {{ background-color: #f9f9f9; padding: 20px; margin-top: 20px; border-radius: 5px; }}
                .error {{ background-color: #fff3cd; padding: 15px; margin: 15px 0; border-left: 4px solid #dc3545; }}
                .footer {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #777; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>❌ Job Failed</h1>
                </div>
                
                <div class="content">
                    <p>Hello,</p>
                    <p>Your workflow automation job "<strong>{job_name}</strong>" encountered an error during processing.</p>
                    
                    <div class="error">
                        <h3>Error Details:</h3>
                        <p>{error_message}</p>
                    </div>
                    
                    <p>Please check your input file and try again. If the issue persists, contact support.</p>
                </div>
                
                <div class="footer">
                    <p>This is an automated message from Workflow Automation Dashboard.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(
            to_emails=to_emails,
            subject=subject,
            body=body,
            html=True
        )


# Example usage
if __name__ == "__main__":
    email_service = EmailService()
    
    # Test job completion email
    stats = {
        'total_rows': 100,
        'processed_rows': 95,
        'error_rows': 5,
        'processing_time': '3.2 seconds',
        'completed_at': '2024-03-28 10:30:00'
    }
    
    # Uncomment to test (requires valid email configuration)
    # email_service.send_job_completion_email(
    #     to_emails=['test@example.com'],
    #     job_name='Sample Data Processing',
    #     stats=stats,
    #     report_files=['./storage/reports/sample_report.pdf']
    # )
    
    print("Email service initialized. Configure .env file with SMTP settings to enable email functionality.")
