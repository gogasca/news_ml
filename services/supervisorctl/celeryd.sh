#!/bin/bash
# Google 2018
# Gonzalo Gasca Meza gogasca@google.com
# Program: Celery start script for Supervisor
# Use celeryd.conf|celerydclient.conf to launch this script.
#
source ~/.profile
DEBUG_MODE="INFO"
CELERY_LOGFILE=/usr/local/src/news_ml/log/%n.log
# If you change CELERY_PROCESSES verify you change CELERYD_PREFETCH_MULTIPLIER in conf/celeryconfig.py
CELERY_PROCESSES=10
CELERY_PID_FILE=/usr/local/src/news_ml/log/%n.pid
CELERYD_SERVER_OPTS="-P processes -c $CELERY_PROCESSES --loglevel=$DEBUG_MODE --pidfile=$CELERY_PID_FILE -Ofair"
cd /usr/local/src/news_ml/conf
echo "Server mode"
exec celery worker -n celeryd$1@%h -f $CELERY_LOGFILE $CELERYD_SERVER_OPTS