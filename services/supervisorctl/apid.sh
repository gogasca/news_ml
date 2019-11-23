#!/bin/bash
# Program: Gunicorn start script for Supervisor
# Use apid.conf to launch this script.

cd /usr/local/src/news_ml/api/version1_0/

# Execute Gunicorn and call Flask API.
exec gunicorn news_ml:api_app --bind 0.0.0.0:"$API_PORT" --log-level="$LOG_LEVEL" --log-file="$GUNICORN_LOGFILE" --workers "$NUM_WORKERS" --worker-connections="$WORKER_CONNECTIONS" --backlog="$BACKLOG" --timeout "$TIMEOUT"