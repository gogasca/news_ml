""" Starts API via Flask.

Flask Main Application and configuration settings.
Defines API endpoints.
"""


import logging
import flask_restful

from conf import logger
from conf import settings

from api.version1_0.database import Model
from api_main import ApiBase
from api_main import ApiUser
from api_main import ApiUserList
from api_main import Campaign
from api_main import CampaignList
from api_main import GetToken
from api_main import NewsList
from api_main import Person
from api_main import PersonList
from api_main import Status

from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

from utils import banner

log = logger.LoggerManager().getLogger("__app__",
                                       logging_file=settings.api_logfile)
log.setLevel(level=logging.DEBUG)

# Flask Main Application.
api_app = Flask(__name__)
# Flask configuration.
api_app.config.from_pyfile("../../../conf/settings.py")
# Define API.
news_api = flask_restful.Api(api_app)
# Initialize database.
db = Model.db.init_app(api_app)

# API Endpoint definition.
news_api.add_resource(ApiBase, settings.api_base_url)
news_api.add_resource(ApiUser, '/api/1.0/users/<int:id>')
news_api.add_resource(ApiUserList, '/api/1.0/users')
news_api.add_resource(Campaign, '/api/1.0/campaign/<string:ref>')
news_api.add_resource(CampaignList, '/api/1.0/campaign')
news_api.add_resource(GetToken, '/api/1.0/token')
news_api.add_resource(Person, '/api/1.0/person/<int:id>')
news_api.add_resource(PersonList, '/api/1.0/person')
news_api.add_resource(NewsList, '/api/1.0/news')
news_api.add_resource(Status, '/api/1.0/status')

# API Proxy WSGi for gunicorn.
api_app.wsgi_app = ProxyFix(api_app.wsgi_app)

# API Logs.
log.info('Initializing News API >>>')
banner.horizontal('News ML v0.1')
log.info('News API Started... >>>')
