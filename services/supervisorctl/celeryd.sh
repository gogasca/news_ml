#!/bin/bash
# Program: Celery start script for Supervisor
# Use celeryd.conf to launch this script.

. ~root/.profile
DEBUG_MODE="INFO"
CELERY_LOGFILE=/usr/local/src/newsml/log/%n.log
# If you change CELERY_PROCESSES verify you change CELERYD_PREFETCH_MULTIPLIER in conf/celeryconfig.py.
CELERY_PROCESSES=10
CELERY_PID_FILE=/usr/local/src/newsml/log/%n.pid
CELERYD_SERVER_OPTS="-P processes -c $CELERY_PROCESSES --loglevel=$DEBUG_MODE --pidfile=$CELERY_PID_FILE -Ofair"

echo "Starting Celery..."
cd /usr/local/src/newsml/conf
exec celery worker -n celeryd$1@%h -f $CELERY_LOGFILE $CELERYD_SERVER_OPTS