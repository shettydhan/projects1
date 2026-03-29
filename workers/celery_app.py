"""
Celery application configuration
"""
from celery import Celery
from backend.config import settings

# Create Celery app
celery_app = Celery(
    'workflow_automation',
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=['workers.tasks']
)

# Configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour max
    task_soft_time_limit=3000,  # 50 minutes soft limit
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=50,
)

if __name__ == '__main__':
    celery_app.start()
