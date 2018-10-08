"""Initial application that call the API via flask.

 Gunicorn calls the Flask API. Example:
   gunicorn news_ml:api_app
       --bind 0.0.0.0:8081
       --log-level=CRITICAL
       --log-file=$GUNICORN_LOGFILE
       --workers $NUM_WORKERS
       --worker-connections=$WORKER_CONNECTIONS
       --backlog=$BACKLOG
       --timeout $TIMEOUT
"""
from application.app import api_app

if __name__ == "__main__":
    api_app.run(debug=True, threaded=True)
