"""
Streamlit Dashboard for Workflow Automation
"""
import streamlit as st
import requests
import pandas as pd
import time
import os
from datetime import datetime
from pathlib import Path

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Page config
st.set_page_config(
    page_title="Workflow Automation Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stat-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .stat-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #666;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 0.3rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 1rem;
        border-radius: 0.3rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


def check_api_health():
    """Check if API is reachable"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def get_stats():
    """Get system statistics"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/stats")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None


def get_jobs(status=None, limit=50):
    """Get list of jobs"""
    try:
        params = {"limit": limit}
        if status:
            params["status"] = status
        
        response = requests.get(f"{API_BASE_URL}/api/jobs", params=params)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error fetching jobs: {str(e)}")
        return None


def get_job_status(job_id):
    """Get job status"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/jobs/{job_id}/status")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None


def upload_file(file, job_name, send_email, email_recipients):
    """Upload file and create job"""
    try:
        files = {"file": (file.name, file, file.type)}
        data = {
            "job_name": job_name,
            "send_email": send_email,
            "email_recipients": email_recipients if send_email else ""
        }
        
        response = requests.post(
            f"{API_BASE_URL}/api/jobs/upload",
            files=files,
            data=data
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Upload failed: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error uploading file: {str(e)}")
        return None


def download_report(job_id, format="csv"):
    """Download report"""
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/jobs/{job_id}/download",
            params={"format": format}
        )
        
        if response.status_code == 200:
            return response.content
        return None
    except:
        return None


def delete_job(job_id):
    """Delete a job"""
    try:
        response = requests.delete(f"{API_BASE_URL}/api/jobs/{job_id}")
        return response.status_code == 200
    except:
        return False


def main():
    """Main dashboard application"""
    
    # Header
    st.markdown('<div class="main-header">🤖 Workflow Automation Dashboard</div>', unsafe_allow_html=True)
    
    # Check API health
    if not check_api_health():
        st.error("❌ API is not reachable. Please make sure the backend server is running.")
        st.code("python -m uvicorn backend.main:app --reload")
        return
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["📤 Upload & Process", "📊 View Jobs", "📈 Statistics", "⚙️ Settings"]
    )
    
    # Page routing
    if page == "📤 Upload & Process":
        page_upload()
    elif page == "📊 View Jobs":
        page_view_jobs()
    elif page == "📈 Statistics":
        page_statistics()
    elif page == "⚙️ Settings":
        page_settings()


def page_upload():
    """Upload and process page"""
    st.header("📤 Upload & Process Data")
    
    st.markdown("""
    Upload your Excel or CSV file to start automated processing. The system will:
    - Clean and standardize your data
    - Remove duplicates and empty rows
    - Generate comprehensive reports (CSV + PDF)
    - Optionally email the results to you
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # File upload
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['csv', 'xlsx', 'xls'],
            help="Upload Excel (.xlsx, .xls) or CSV files. Max size: 50MB"
        )
        
        # Job configuration
        job_name = st.text_input(
            "Job Name",
            value=f"Processing_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            help="Give this job a descriptive name"
        )
        
        # Email configuration
        send_email = st.checkbox("📧 Send email when complete", value=False)
        
        email_recipients = ""
        if send_email:
            email_recipients = st.text_input(
                "Email Recipients",
                placeholder="email1@example.com, email2@example.com",
                help="Comma-separated email addresses"
            )
        
        # Submit button
        if st.button("🚀 Start Processing", type="primary", use_container_width=True):
            if not uploaded_file:
                st.error("Please upload a file first")
            elif not job_name:
                st.error("Please provide a job name")
            elif send_email and not email_recipients:
                st.error("Please provide email recipients")
            else:
                with st.spinner("Uploading and creating job..."):
                    result = upload_file(uploaded_file, job_name, send_email, email_recipients)
                    
                    if result:
                        st.markdown(f'<div class="success-box">✅ Job created successfully!<br/>Job ID: <code>{result["job_id"]}</code></div>', unsafe_allow_html=True)
                        
                        # Track job progress
                        st.subheader("📊 Processing Progress")
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        job_id = result["job_id"]
                        max_attempts = 120  # 2 minutes
                        attempt = 0
                        
                        while attempt < max_attempts:
                            status = get_job_status(job_id)
                            if status:
                                progress = status['progress'] / 100.0
                                progress_bar.progress(progress)
                                status_text.text(f"Status: {status['status'].upper()} - {status['progress']:.1f}%")
                                
                                if status['status'] == 'completed':
                                    st.success("✅ Processing completed successfully!")
                                    
                                    # Download buttons
                                    col_csv, col_pdf = st.columns(2)
                                    
                                    with col_csv:
                                        csv_data = download_report(job_id, "csv")
                                        if csv_data:
                                            st.download_button(
                                                label="📥 Download CSV Report",
                                                data=csv_data,
                                                file_name=f"{job_name}.csv",
                                                mime="text/csv",
                                                use_container_width=True
                                            )
                                    
                                    with col_pdf:
                                        pdf_data = download_report(job_id, "pdf")
                                        if pdf_data:
                                            st.download_button(
                                                label="📥 Download PDF Report",
                                                data=pdf_data,
                                                file_name=f"{job_name}.pdf",
                                                mime="application/pdf",
                                                use_container_width=True
                                            )
                                    
                                    break
                                
                                elif status['status'] == 'failed':
                                    st.error(f"❌ Processing failed: {status.get('message', 'Unknown error')}")
                                    break
                            
                            time.sleep(1)
                            attempt += 1
                        
                        if attempt >= max_attempts:
                            st.warning("⏱️ Status check timed out. Please check the 'View Jobs' page for updates.")
    
    with col2:
        st.info("💡 **Tips:**\n\n"
                "- Ensure your file has column headers\n"
                "- Remove any merged cells\n"
                "- Data will be automatically cleaned\n"
                "- Duplicates will be removed\n"
                "- You'll get both CSV and PDF reports")


def page_view_jobs():
    """View jobs page"""
    st.header("📊 View Jobs")
    
    # Filters
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        status_filter = st.selectbox(
            "Filter by status",
            ["All", "pending", "processing", "completed", "failed"]
        )
    
    with col2:
        limit = st.number_input("Jobs per page", min_value=10, max_value=100, value=50)
    
    with col3:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    # Fetch jobs
    status_param = None if status_filter == "All" else status_filter
    jobs_data = get_jobs(status=status_param, limit=limit)
    
    if jobs_data and jobs_data.get('jobs'):
        jobs = jobs_data['jobs']
        st.write(f"**Total jobs:** {jobs_data['total']}")
        
        # Display jobs
        for job in jobs:
            with st.expander(f"🔹 {job['name']} - {job['status'].upper()}", expanded=False):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.write(f"**Job ID:** `{job['job_id']}`")
                    st.write(f"**Status:** {job['status']}")
                    st.write(f"**Progress:** {job['progress']:.1f}%")
                
                with col2:
                    st.write(f"**Created:** {job['created_at'][:19] if job['created_at'] else 'N/A'}")
                    st.write(f"**Rows:** {job['processed_rows']} / {job['total_rows']}")
                    if job['error_rows'] > 0:
                        st.write(f"**Errors:** {job['error_rows']}")
                
                with col3:
                    if job['status'] == 'completed':
                        # Download buttons
                        csv_data = download_report(job['job_id'], "csv")
                        if csv_data:
                            st.download_button(
                                label="📥 CSV",
                                data=csv_data,
                                file_name=f"{job['name']}.csv",
                                mime="text/csv",
                                use_container_width=True,
                                key=f"csv_{job['job_id']}"
                            )
                        
                        pdf_data = download_report(job['job_id'], "pdf")
                        if pdf_data:
                            st.download_button(
                                label="📥 PDF",
                                data=pdf_data,
                                file_name=f"{job['name']}.pdf",
                                mime="application/pdf",
                                use_container_width=True,
                                key=f"pdf_{job['job_id']}"
                            )
                    
                    # Delete button
                    if st.button("🗑️ Delete", key=f"delete_{job['job_id']}", use_container_width=True):
                        if delete_job(job['job_id']):
                            st.success("Job deleted!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Failed to delete job")
                
                # Show error message if failed
                if job['status'] == 'failed' and job.get('error_message'):
                    st.error(f"Error: {job['error_message']}")
    else:
        st.info("No jobs found")


def page_statistics():
    """Statistics page"""
    st.header("📈 System Statistics")
    
    stats = get_stats()
    
    if stats:
        # Display stats in columns
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown(
                f'<div class="stat-box"><div class="stat-value">{stats["total_jobs"]}</div><div class="stat-label">Total Jobs</div></div>',
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                f'<div class="stat-box"><div class="stat-value">{stats["pending"]}</div><div class="stat-label">Pending</div></div>',
                unsafe_allow_html=True
            )
        
        with col3:
            st.markdown(
                f'<div class="stat-box"><div class="stat-value">{stats["processing"]}</div><div class="stat-label">Processing</div></div>',
                unsafe_allow_html=True
            )
        
        with col4:
            st.markdown(
                f'<div class="stat-box"><div class="stat-value">{stats["completed"]}</div><div class="stat-label">Completed</div></div>',
                unsafe_allow_html=True
            )
        
        with col5:
            st.markdown(
                f'<div class="stat-box"><div class="stat-value">{stats["failed"]}</div><div class="stat-label">Failed</div></div>',
                unsafe_allow_html=True
            )
        
        # Success rate
        if stats["total_jobs"] > 0:
            success_rate = (stats["completed"] / stats["total_jobs"]) * 100
            st.metric("Success Rate", f"{success_rate:.1f}%")
    else:
        st.error("Could not fetch statistics")


def page_settings():
    """Settings page"""
    st.header("⚙️ Settings")
    
    st.subheader("API Configuration")
    st.info(f"API URL: {API_BASE_URL}")
    
    st.subheader("About")
    st.markdown("""
    **Workflow Automation Dashboard v1.0.0**
    
    This system automates data processing workflows:
    - 📤 Upload Excel/CSV files
    - 🧹 Automatic data cleaning
    - 📊 Report generation (CSV + PDF)
    - 📧 Email notifications
    - 🔄 Background processing
    
    ---
    
    **Tech Stack:**
    - Backend: FastAPI + Python
    - Dashboard: Streamlit
    - Queue: Celery + Redis
    - Database: SQLite
    
    ---
    
    **Documentation:**
    - API Docs: http://localhost:8000/docs
    - GitHub: [Your Repo]
    """)
    
    st.subheader("System Health")
    if check_api_health():
        st.success("✅ API is healthy")
    else:
        st.error("❌ API is not reachable")


if __name__ == "__main__":
    main()
