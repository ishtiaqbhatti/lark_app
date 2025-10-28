#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Cleanup Logic ---
echo "Attempting to free up ports 3000 and 8000..."
lsof -ti:3000 | xargs kill -9 || true
lsof -ti:8000 | xargs kill -9 || true
echo "Ports have been cleared."
# --- End Cleanup ---

# Function to clean up all child processes on exit
cleanup() {
    echo "Shutting down servers..."
    # The pkill command is more reliable for finding and killing all child processes.
    pkill -P $$
}
trap cleanup EXIT

# 1. Create a logs directory and start the backend in the background
echo "Starting FastAPI backend..."
mkdir -p logs
LOG_FILE="logs/backend-$(date +'%Y-%m-%d_%H-%M-%S').log"
(uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload) > "$LOG_FILE" 2>&1 &
echo "Backend logs are being written to: $LOG_FILE"

# 2. Wait for the backend to be ready
echo "Waiting for backend to start on port 8000..."
while ! nc -z localhost 8000; do
  sleep 0.1 # wait for a moment before checking again
done
echo "Backend is ready."

# 3. Start the frontend in the foreground
echo "Starting React frontend..."
(cd /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app && npm run dev)

# When the user presses Ctrl+C, the trap will run the cleanup function.
