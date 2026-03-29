#!/bin/bash
# Stop all services

PROJECT_DIR="$HOME/projects/workflow-automation-dashboard"
cd "$PROJECT_DIR"

echo "🛑 Stopping Workflow Automation Dashboard..."
echo ""

# Function to stop service
stop_service() {
    SERVICE_NAME=$1
    PID_FILE=".pids/$2.pid"
    
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 $PID 2>/dev/null; then
            echo "🛑 Stopping $SERVICE_NAME (PID: $PID)..."
            kill $PID
            sleep 1
            # Force kill if still running
            if kill -0 $PID 2>/dev/null; then
                kill -9 $PID
            fi
            rm "$PID_FILE"
            echo "✅ $SERVICE_NAME stopped"
        else
            echo "⚠️  $SERVICE_NAME was not running"
            rm "$PID_FILE"
        fi
    else
        echo "⚠️  No PID file for $SERVICE_NAME"
    fi
}

# Stop all services
stop_service "Backend API" "backend"
stop_service "Celery Worker" "worker"
stop_service "Streamlit Dashboard" "dashboard"

echo ""
echo "=========================================="
echo "✅ All services stopped"
echo "=========================================="
