"""System configuration settings."""

import os

# Parameters
FILEPATH = os.environ.get('NEWSML_ENV', '')

DATE_LATEST = u'latest'
DEFAULT_PROVIDER = u'GOOGLEBLOG.COM'
NEWS_FIELDS = ['title', 'content', 'url', 'published_at', 'source']
EMPTY_TEXT = ''
EMAIL_SEPARATOR = ';'

# =========================================================
# Logging
# =========================================================

APP_LOGFILE = FILEPATH + 'log/app.log'
LOG_SALIENCE = False

# =========================================================
# NLP settings
# =========================================================

CREDENTIALS = FILEPATH + 'conf/credentials/key.json'
SALIENCE_SCORE = 0.01
CONTENT_SIZE = 16384
INVALID_WORDS = FILEPATH + 'conf/dictionary/es_blacklist'
ENTITY_FILTER = FILEPATH + 'conf/entity_blacklist'

# =========================================================
# NLP
# =========================================================
PROCESS_ENTITIES = True
REMOVE_STOP_WORDS = True
DEFAULT_LANGUAGE = 'en'
TRANSLATION_SERVICE = True
TRANSLATION_LIMIT = 10000
TRANSLATION_DEFAULT_LANGUAGE = 'es'
TRANSLATION_LANGUAGES = ('es', 'fr', 'zh-CN', 'pt', 'de')

# Valid News providers.
VALID_PROVIDERS = ('NEWS_API')

# =========================================================
# Google News API
# =========================================================

NEWS_API = 'NEWS_API'
NEWS_API_KEY = os.environ['NEWS_API_KEY']
NEWS_API_URL = 'https://newsapi.org/v2/'
NEWS_API_SOURCES = ['ars-technica',
                    'engadget',
                    'hacker-news',
                    'recode',
                    'techcrunch',
                    'techradar',
                    'the-next-web',
                    'the-verge']

# *Recode do not support sortBy=latest: CL Correct recode invalid sorting
# algorithm.
NEWS_API_SORT_ORDER = 'latest'
NEWS_PAGE_SIZE = 100
CAMPAIGN_LIMIT = 120

# List of News API supported providers.
ARS_TECHNICA = 'ARS_TECHNICA'
ENGADGET = 'ENGADGET'
HACKER_NEWS = 'HACKER_NEWS'
RECODE = 'RECODE'
TECHRADAR = 'TECHRADAR'
THE_NEXT_WEB = 'THE_NEXT_WEB'

# =========================================================
# Alexa Skill
# =========================================================

DEFAULT_CURRENCY = 'USD'
ALEXA_PORT = 8082

# =========================================================
# Ranking
# =========================================================
RANK_ARTICLES = True
UPDATE_RANK_ARTICLES_DB = True
RANKING_SOURCES = ['amazon.com',
                   'fb.com',
                   'facebook.com',
                   'ibm.com',
                   'microsoft.com',
                   'googleblog.com',
                   'anaconda.com',
                   'databricks.com',
                   'fastcompany.com',
                   'techcrunch',
                   'towardsdatascience.com',
                   'the next web',
                   'hackernoon.com']

UNKNOWN_SOURCE_SCORE = 5
RANKING_LIMIT = 1000
RANKING_QUERY_DATE = """SELECT to_char(published_at,'YYYY-MM-DD') AS date
    FROM news WHERE inserted_at IS NOT NULL GROUP BY 1 ORDER BY date DESC LIMIT 1;"""
RANKING_QUERY_GET_NEWS = """SELECT news_id, title, content, LOWER(source) AS
    source, url FROM news WHERE campaign = '%s' GROUP BY 1,2,3,4,5;"""
RANKING_QUERY_GET_NEWS_BY_DATE = """SELECT news_id, title, content,
    LOWER(source) AS source, url FROM news WHERE TO_CHAR(inserted_at,
    'YYYY-MM-DD') = '%s' AND inserted_at IS NOT NULL GROUP BY 1,2,3,4,5;"""
RANKING_QUERY_GET_NEWS_FILTERED = """SELECT post_id, title, text,
    LOWER(source), url FROM news WHERE to_char(published_at,'YYYY-MM-DD') = '%s'
    AND LOWER(source) != ANY('{%s}'::text[]) GROUP BY 1,2,3,4,5;"""

# =========================================================
# Clustering configuration parameters. Queries Ranked posts
# =========================================================

NUM_OF_CLUSTERS = 8
PROCESS_COSINE_SIMILARITY = False
UPDATE_CLUSTERING_ARTICLES_DB = True
api_num_of_clusters = 'clusters'
CLUSTERING_PROVIDER = 'CLUSTERING'
CLUSTERING_LIMIT = 1000
CLUSTERING_QUERY_DATE = """SELECT to_char(inserted_at,'YYYY-MM-DD') AS date
    FROM news WHERE inserted_at IS NOT NULL GROUP BY 1 ORDER BY date DESC LIMIT 1;"""
CLUSTERING_QUERY_GET_NEWS = """SELECT news_id, title, content, LOWER(source) AS
    source, url FROM news WHERE TO_CHAR(inserted_at,'YYYY-MM-DD') = '%s' AND inserted_at IS NOT NULL GROUP
    BY 1,2,3,4,5;"""
CLUSTERING_QUERY_GET_NEWS_FILTERED = """SELECT news_id, title, content,
    LOWER(source) AS source, url FROM news WHERE TO_CHAR(inserted_at,
    'YYYY-MM-DD') = '%s' AND LOWER(source) != ALL('{%s}'::text[]) GROUP BY 1,
    2,3,4,5;"""

# =========================================================
# Authentication
# =========================================================

API_KEY = os.environ['SECRET_FERNET_KEY']
TOKEN_EXPIRATION_SECS = 600

# =========================================================
# API configuration parameters
# =========================================================

API_VERSION = '0.4'
API_ACCOUNT = os.environ['API_USERNAME']
API_PASSWORD = os.environ['API_PASSWORD']
API_LOGFILE = FILEPATH + '/log/apid.log'
API_BASE_URL = '/api/1.0/'
API_SCHEME = 'http'
API_FRONTEND = 'api.newsml.io'
API_IP_ADDRESS = '0.0.0.0'
API_EXTERNAL_PORT = 8080
API_PORT = 8081
API_URL = '%s://%s:%d/api/1.0' % (API_SCHEME, API_FRONTEND, API_EXTERNAL_PORT)
API_REALM = 'Basic realm="newsml"'
API_LIMITS_ENABLED = True
API_GLOBAL_LIMITS = '1000/second'
ITEMS_PER_PAGE = 10
API_ERROR_LIMIT = 50
API_OK = 'News API version %s is active' % API_VERSION
API_MIME_TYPE = 'application/json'
MAX_API_CLIENT_REQUESTS = 1000
MAX_NEWS = 8

# =========================================================
# News processor
# =========================================================
MAX_CRAWLER_PROCESSING = 3600  # Max time processing news task.
MAX_TASK_PROCESSING = 3600  # Max time processing news task.
MAX_RANK_PROCESSING = 1800  # Max time ranking posts.
MAX_API_PROCESSING = 600

# =========================================================
# Email SMTP
# =========================================================

EMAIL_SERVER = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_ADDRESS = os.environ.get('EMAIL_USERNAME')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_NAME = 'News ML Reporter'
EMAIL_SUBJECT = 'News ML Daily summary'
EMAIL_REPORT = True
EMAIL_TO = ['admin@newsml.io']
EMAIL_CHECK_MX = False
EMAIL_VERIFY = False

# =========================================================
# Email Mailgun
# =========================================================
MAILGUN_SENDER = 'news-ml@newsml.io'
MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN')
MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')

# =========================================================
# Twilio configuration parameters
# =========================================================

SMS_ALERTS = False
TWILIO_FROM = os.environ.get('TWILIO_FROM')
TWILIO_ACCOUNTID = os.environ.get('TWILIO_ACCOUNTID')
TWILIO_TOKENID = os.environ.get('TWILIO_TOKENID')
PHONE_NUMBERS = ['+1408XXXXXXX']

# =========================================================
# Report configuration parameters
# =========================================================
REPORT_ALL_DATES_ARTICLES = False

# =========================================================
# Database
# =========================================================
# psql -h 127.0.0.1 -d postgres -U newsml -W #dbhost = '127.0.0.1'

DBHOST = os.environ.get('DBHOST')
DBPORT = int(os.environ.get('DBPORT'))
DBUSERNAME = os.environ.get('DBUSERNAME')
DBPASSWORD = os.environ.get('DBPASSWORD')
DBNAME = os.environ.get('DBNAME')
DBPASSWORD_ALLOW_EMPTY_PASSWORD = False
DBNOW = 'now()'

# =========================================================
# SQLALCHEMY parameter
# =========================================================

SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@%s/%s' % (
    DBUSERNAME, DBPASSWORD, DBHOST, DBNAME)
SQLALCHEMY_DSN = 'dbname=%s host=%s port=%d user=%s password=%s' % (
    DBNAME, DBHOST, DBPORT, DBUSERNAME, DBPASSWORD)
SQLALCHEMY_ECHO = False
SQLALCHEMY_POOL_SIZE = 1024
SQLALCHEMY_POOL_TIMEOUT = 5
SQLALCHEMY_MAX_OVERFLOW = 0
SQLALCHEMY_POOL_RECYCLE = 60
SQLALCHEMY_TRACK_MODIFICATIONS = True
DATABASE_CONNECT_OPTIONS = None
SQLALCHEMY_COMMIT_ON_TEARDOWN = True

