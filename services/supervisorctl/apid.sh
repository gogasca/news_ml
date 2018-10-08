#!/bin/bash
cd /usr/local/src/news_ml/api/version1_0/
GUNICORN_LOGFILE=/usr/local/src/news_ml/log/gunicorn.log
API_PORT=8081
NUM_WORKERS=1
TIMEOUT=60
WORKER_CONNECTIONS=1000
BACKLOG=500
LOG_LEVEL=DEBUG

# Execute Gunicorn and call Flask API.
exec gunicorn news_ml:api_app --bind 0.0.0.0:$API_PORT --log-level=$LOG_LEVEL --log-file=$GUNICORN_LOGFILE --workers $NUM_WORKERS --worker-connections=$WORKER_CONNECTIONS --backlog=$BACKLOG --timeout $TIMEOUT