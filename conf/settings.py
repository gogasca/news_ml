"""System configuration settings."""

import os
import platform
import sys

if platform.system() == 'Linux':
    filepath = '/usr/local/src/news_ml/'
else:
    filepath = '/Users/gogasca/Documents/Development/dpe/news/'

sys.path.append(filepath)

DATE_LATEST = u'latest'
DEFAULT_PROVIDER = 'NEWS_API'
NEWS_FIELDS = ['title', 'content', 'url', 'published_at', 'provider']
EMPTY_TEXT = ''
_EMAIL_SEPARATOR = ';'

# =========================================================
# Logging
# =========================================================

app_logfile = filepath + 'log/app.log'
log_salience = False

# =========================================================
# NLP settings
# =========================================================

credentials = filepath + 'conf/credentials/key.json'
salience_score = 0.01
content_size = 16384
invalid_words = filepath + 'conf/dictionary/es_blacklist'
entity_filter = filepath + 'conf/entity_blacklist'

# =========================================================
# NLP
# =========================================================
remove_stop_words = True
default_language = 'en'
translation_service = True
translation_limit = 10000
translation_default_language = 'es'
translation_languages = ('es', 'fr', 'zh-CN', 'pt', 'de')

# Valid News providers.
valid_providers = ('NEWS_API')

# =========================================================
# Google News API
# =========================================================

news_api = 'NEWS_API'
news_api_key = os.environ['NEWS_API_KEY']
# news_api_url = 'https://newsapi.org/v1/articles?source=%s&apiKey=%s&sortBy=%s'
# news_api_url = 'https://newsapi.org/v2/top-headlines?sources=%s&apiKey=%s' \
#               '&sortBy=%s'
news_api_url = 'https://newsapi.org/v2/'
news_api_sources = ['ars-technica',
                    'engadget',
                    'hacker-news',
                    'recode',
                    'techcrunch',
                    'techradar',
                    'the-next-web',
                    'the-verge']

# *Recode do not support sortBy=latest: CL Correct recode invalid sorting
# algorithm.
news_api_sort_order = 'latest'
news_page_size = 100

# List of Google News API supported providers.
ars_technica = 'ARS_TECHNICA'
engadget = 'ENGADGET'
hacker_news = 'HACKER_NEWS'
recode = 'RECODE'
techradar = 'TECHRADAR'
the_next_web = 'THE_NEXT_WEB'

campaign_limit = 120

# =========================================================
# Alexa Skill
# =========================================================

default_currency = 'USD'
alexa_port = 8082

# =========================================================
# Ranking
# =========================================================
rank_articles = True
ranking_sources = ['techcrunch',
                   'towardsdatascience.com',
                   'the next web',
                   'hackernoon.com',
                   'databricks.com',
                   'anaconda.com',
                   'googleblog.com',
                   'ibm.com',
                   'fb.com',
                   'amazon.com']

unknown_source_score = 10
ranking_limit = 1000
ranking_query_date = """SELECT to_char(published_at,'YYYY-MM-DD') AS date
    FROM news GROUP BY 1 ORDER BY date DESC LIMIT 1;"""
ranking_query_get_news = """SELECT news_id, title, content, lower(source), url
    FROM news WHERE campaign = '%s' GROUP BY 1,2,3,4,5;"""
ranking_query_get_news_filtered = """SELECT post_id, title, text,
lower(source), url, lower(tld)
    FROM news WHERE to_char(published_at,'YYYY-MM-DD') = '%s'
    AND LOWER(source) != ANY('{%s}'::text[]) GROUP BY 1,2,3,4,5,6;"""

# =========================================================
# Twilio configuration parameters
# =========================================================

sms_alerts = False
twilio_from = '+14088053951'
twilio_accountId = 'ACed0b00c221c2e58a3f6dd33308c84321'
twilio_tokenId = '68314e5765c801ba4e38bdb4c730f90e'
phone_numbers = ['+14082186575']

# =========================================================
# API configuration parameters
# =========================================================

api_account = os.environ['API_USERNAME']
api_password = os.environ['API_PASSWORD']
api_logfile = filepath + '/log/apid.log'
api_base_url = '/api/1.0/'
api_scheme = 'https'
api_frontend = 'api.googlecloud.io'
api_ip_address = '0.0.0.0'
api_external_port = 8080
api_port = 8081
api_url = '%s://%s:%d/api/1.0' % (api_scheme, api_frontend, api_external_port)
api_version = '0.1'
api_limits_enabled = True
api_global_limits = '1000/second'
max_news = 8
items_per_page = 10
api_error_limit = 50
api_ok = 'News API is active'
api_mime_type = 'application/json'
max_api_client_requests = 1000

# =========================================================
# News processor
# =========================================================

max_crawler_processing = 1800  # Max time processing news task
max_task_processing = 1800  # Max time processing news task
max_rank_processing = 1800  # Max time ranking posts
max_api_processing = 600

# =========================================================
# Email SMTP
# =========================================================

# =========================================================
# Email Mailgun
# =========================================================
mailgun_sender = '8bits@techie8.com'
mailgun_api_key = os.environ.get('MAILGUN_API_KEY')
email_server = 'smtp.gmail.com'
email_port = 587
email_address = os.environ.get('EMAIL_USERNAME')
email_password = os.environ.get('EMAIL_PASSWORD')
email_name = 'News ML Reporter'
email_subject = 'News ML Resumen diario'
email_report = True
email_to = ['gogasca@google.com']
email_check_mx = False
email_verify = False

# =========================================================
# Database
# =========================================================
# psql -h 127.0.0.1 -d postgres -U techie8db -W #dbhost = '127.0.0.1'

dbhost = os.environ['DBHOST']
dbport = int(os.environ['DBPORT'])
dbusername = os.environ['DBUSERNAME']
dbpassword = os.environ['DBPASSWORD']
dbname = os.environ['DBNAME']

dbPasswordAllowEmptyPassword = False
dbnow = 'now()'

# =========================================================
# SQLALCHEMY parameter
# =========================================================

SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@%s/%s' % (
    dbusername, dbpassword, dbhost, dbname)
SQLALCHEMY_DSN = 'dbname=%s host=%s port=%d user=%s password=%s' % (
    dbname, dbhost, dbport, dbusername, dbpassword)
SQLALCHEMY_ECHO = False
SQLALCHEMY_POOL_SIZE = 1024
SQLALCHEMY_POOL_TIMEOUT = 5
SQLALCHEMY_MAX_OVERFLOW = 0
SQLALCHEMY_POOL_RECYCLE = 60
SQLALCHEMY_TRACK_MODIFICATIONS = True
DATABASE_CONNECT_OPTIONS = None
SQLALCHEMY_COMMIT_ON_TEARDOWN = True

# =========================================================
# Authentication
# =========================================================

api_key = os.environ['SECRET_FERNET_KEY']
api_realm = 'Basic realm="newsml"'
token_expiration_secs = 600
