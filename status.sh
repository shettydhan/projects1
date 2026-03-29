#!/bin/bash
# Check status of all services

PROJECT_DIR="$HOME/projects/workflow-automation-dashboard"
cd "$PROJECT_DIR"

echo "📊 Workflow Automation Dashboard - Status"
echo "=========================================="
echo ""

# Function to check service status
check_service() {
    SERVICE_NAME=$1
    PID_FILE=".pids/$2.pid"
    PORT=$3
    
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 $PID 2>/dev/null; then
            echo "✅ $SERVICE_NAME: Running (PID: $PID)"
            if [ ! -z "$PORT" ]; then
                if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
                    echo "   Port $PORT: Active"
                else
                    echo "   ⚠️  Port $PORT: Not listening"
                fi
            fi
        else
            echo "❌ $SERVICE_NAME: Not running (stale PID file)"
        fi
    else
        echo "❌ $SERVICE_NAME: Not running (no PID file)"
    fi
}

# Check Redis
echo "🔍 Checking Redis..."
if redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis: Running"
else
    echo "❌ Redis: Not running"
fi
echo ""

# Check services
echo "🔍 Checking Services..."
check_service "Backend API" "backend" "8000"
check_service "Celery Worker" "worker"
check_service "Streamlit Dashboard" "dashboard" "8501"

echo ""
echo "=========================================="
echo ""
echo "📍 Access Points:"
echo "   Dashboard:  http://localhost:8501"
echo "   API:        http://localhost:8000"
echo "   API Docs:   http://localhost:8000/docs"
echo ""
