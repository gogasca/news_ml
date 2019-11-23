"""Celery configuration settings."""

from kombu import Exchange
from kombu import Queue

import os
import sys

filepath = os.environ.get('NEWSML_ENV')
sys.path.append(filepath)

CELERYD_CHDIR = filepath
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'US/Pacific'
CELERY_ACCEPT_CONTENT = ['json', 'pickle']
CELERY_IGNORE_RESULT = True
CELERY_RESULT_BACKEND = 'amqp'
CELERY_RESULT_PERSISTENT = True
RABBITMQ_USER = 'news_ml'
RABBITMQ_PASSWORD = 'news_ml'
RABBITMQ_HOSTNAME = 'rabbitmq'
RABBITMQ_PORT = '5672'
BROKER_URL = 'amqp://{}:{}@{}:{}'.format(RABBITMQ_USER, RABBITMQ_PASSWORD,
                                         RABBITMQ_HOSTNAME, RABBITMQ_PORT)
BROKER_CONNECTION_TIMEOUT = 15
BROKER_CONNECTION_MAX_RETRIES = 5
CELERY_DISABLE_RATE_LIMITS = True
CELERY_TASK_RESULT_EXPIRES = 7200
CELERY_IMPORTS = ('main.appD')
CELERY_DEFAULT_QUEUE = 'default'
CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('gold', Exchange('news_ml'), routing_key='news_ml.gold'),
    Queue('silver', Exchange('news_ml'), routing_key='news_ml.silver'),
    Queue('bronze', Exchange('news_ml'), routing_key='news_ml.bronze'),
)
CELERY_DEFAULT_EXCHANGE = 'news_ml'
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
CELERY_DEFAULT_ROUTING_KEY = 'default'
CELERY_TRACK_STARTED = True

CELERY_ROUTES = {
    'process_campaign': {'queue': 'gold', 'routing_key': 'news_ml.gold',
                         'exchange': 'news_ml', },
    'process_clustering': {'queue': 'gold', 'routing_key': 'news_ml.gold',
                           'exchange': 'news_ml', },
    'rank_news': {'queue': 'gold', 'routing_key': 'news_ml.gold',
                  'exchange': 'news_ml', },
}
