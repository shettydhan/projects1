"""
Basic API tests
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data


def test_stats():
    """Test statistics endpoint"""
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_jobs" in data


def test_list_jobs():
    """Test list jobs endpoint"""
    response = client.get("/api/jobs")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "jobs" in data


def test_invalid_job_id():
    """Test getting non-existent job"""
    response = client.get("/api/jobs/invalid-job-id")
    assert response.status_code == 404


# To run tests:
# pip install pytest
# pytest tests/test_api.py -v
