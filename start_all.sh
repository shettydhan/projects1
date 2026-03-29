#!/bin/bash
# Start all services for production

PROJECT_DIR="$HOME/projects/workflow-automation-dashboard"
cd "$PROJECT_DIR"

echo "🚀 Starting Workflow Automation Dashboard..."
echo ""

# Activate virtual environment
source venv/bin/activate

# Check if Redis is running
if ! redis-cli ping > /dev/null 2>&1; then
    echo "⚠️  Redis is not running. Starting Redis..."
    sudo service redis-server start
    sleep 2
fi

echo "✅ Redis is running"
echo ""

# Start Backend API in background
echo "🔧 Starting Backend API..."
nohup python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 > logs/backend.log 2>&1 &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID)"
echo ""

# Wait for backend to be ready
sleep 3

# Start Celery Worker in background
echo "⚙️  Starting Celery Worker..."
nohup celery -A workers.celery_app worker --loglevel=info > logs/worker.log 2>&1 &
WORKER_PID=$!
echo "✅ Worker started (PID: $WORKER_PID)"
echo ""

# Wait for worker to be ready
sleep 2

# Start Streamlit Dashboard in background
echo "🖥️  Starting Streamlit Dashboard..."
nohup streamlit run dashboard/app.py > logs/dashboard.log 2>&1 &
DASHBOARD_PID=$!
echo "✅ Dashboard started (PID: $DASHBOARD_PID)"
echo ""

# Save PIDs to file for easy stopping
echo "$BACKEND_PID" > .pids/backend.pid
echo "$WORKER_PID" > .pids/worker.pid
echo "$DASHBOARD_PID" > .pids/dashboard.pid

echo "=========================================="
echo "✅ All services started successfully!"
echo "=========================================="
echo ""
echo "📍 Access Points:"
echo "   Dashboard:  http://localhost:8501"
echo "   API:        http://localhost:8000"
echo "   API Docs:   http://localhost:8000/docs"
echo ""
echo "📋 Logs:"
echo "   Backend:    tail -f logs/backend.log"
echo "   Worker:     tail -f logs/worker.log"
echo "   Dashboard:  tail -f logs/dashboard.log"
echo ""
echo "🛑 To stop all services:"
echo "   ./stop_all.sh"
echo ""
