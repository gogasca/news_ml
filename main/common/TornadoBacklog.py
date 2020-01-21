"""Collect News via HTTP client.


This module connects to News API
News API module supports 2 endpoints:
1. Get articles
2. Get sources

We pass the source type and other parameters to client request in order to
get top news
We will support a limited list of providers for tech, but API Calls can
support and process any of them.

curl 'https://newsapi.org/v2/top-headlines?sources=bbc&apiKey=<API_KEY>'
    | python -m json.tool
"""

import collections
import logging
import os

from urllib.parse import urlencode
from functools import partial
from tornado import gen, httpclient, ioloop
from tornado.log import gen_log

from conf import logger
from conf import settings
from main.lib.news_api import top_news_handler as news_handler
from main.lib.news_api import top_news_processor as news_processor

CONNECTION_TIMEOUT = 15
REQUEST_TIMEOUT = 30
DEFAULT_LANGUAGE = 'en'

log = logger.LoggerManager().getLogger('__app__')
log.setLevel(level=logging.DEBUG)


def _get_auth_headers(api_key):
    """Builds up JSON object to authenticate via API.

    Args:
        api_key: (str) - A String defining API Key.

    Returns:
        A Dictionary with authentication information.
    """
    return {'Content-Type': 'Application/JSON', 'Authorization': api_key}


class BacklogClient(object):
    """Helper function to handle requests."""

    MAX_CONCURRENT_REQUESTS = settings.MAX_API_CLIENT_REQUESTS

    def __init__(self, ioloop_instance):
        self._ioloop = ioloop_instance
        self._client = httpclient.AsyncHTTPClient(
            max_clients=self.MAX_CONCURRENT_REQUESTS)
        self._client.configure(None, defaults=dict(connect_timeout=15,
                                                   request_timeout=30))
        self._backlog = collections.deque()
        self._concurrent_requests = 0

    def __get_callback(self, function):
        def wrapped(*args, **kwargs):
            self._concurrent_requests -= 1
            self.try_run_request()
            return function(*args, **kwargs)

        return wrapped

    def try_run_request(self):
        while self._backlog and self._concurrent_requests < \
                self.MAX_CONCURRENT_REQUESTS:
            request, callback = self._backlog.popleft()
            self._client.fetch(request, callback=callback)
            self._concurrent_requests += 1

    def fetch(self, request, callback=None):
        wrapped = self.__get_callback(callback)
        self._backlog.append((request, wrapped))
        self.try_run_request()


class TornadoBacklog:
    def __init__(self, campaign_instance):
        self.api_errors = 0
        self.debug = 1
        self.delay = 1.0
        self.queue = 0
        self.to_process = []
        self.campaign = campaign_instance
        # Create HTTP Async - Non blocking client.
        self.ioloop = ioloop.IOLoop.current()
        self.backlog = BacklogClient(self.ioloop)
        log.info('TornadoBacklog() Initialized')
        if self.campaign:
            body = dict()
            body['campaign'] = campaign_instance.reference
        # Handles Search queries.
        if self.campaign.query:
            self.to_process = self.campaign.query.split(',')
        else:
            self.to_process = settings.NEWS_API_SOURCES

    @gen.coroutine
    def crawl(self):
        """

        :return:
        """
        log.info('Sending API requests...')
        while True:
            try:
                yield gen.sleep(self.delay)
                gen_log.info('Items in queue: %d' % len(self.to_process))
                if len(self.to_process) < 1:
                    gen_log.info('Campaign requests completed. API Errors: %s'
                                 % self.api_errors)
                    break
                # Read News providers from Queue.
                source = self.to_process.pop()
                gen_log.info(
                    'Provider: %s Source: %s' % (settings.NEWS_API, source))
                if self.campaign.query:
                    # Build News API URL for search query.
                    url_params = {
                        'q': source,
                        'language': DEFAULT_LANGUAGE,
                        'sortBy': settings.NEWS_API_SORT_ORDER,
                        'pageSize': settings.NEWS_PAGE_SIZE}
                    news_url = '%s%s?%s' % (
                        settings.NEWS_API_URL, 'everything',
                        urlencode(url_params))
                else:
                    url_params = {
                        'sources': source,
                        'sortBy': settings.NEWS_API_SORT_ORDER,
                        'pageSize': settings.NEWS_PAGE_SIZE}
                    if source == 'recode':
                        del url_params['sortBy']
                    news_url = '%s%s?%s' % (
                        settings.NEWS_API_URL, 'top-headlines',
                        urlencode(url_params))
                request = httpclient.HTTPRequest(url=news_url,
                                                 headers=_get_auth_headers(
                                                     settings.NEWS_API_KEY),
                                                 connect_timeout=CONNECTION_TIMEOUT,
                                                 request_timeout=REQUEST_TIMEOUT)
                self.backlog.fetch(request, callback=partial(self.handle_request,
                                                             source))

            except httpclient.HTTPError as exception:
                gen_log.exception('crawl() %r' % exception)
                self.api_errors += 1
                if self.handle_errors(self.api_errors):
                    break
            except IndexError:
                break
        gen_log.info('Waiting for active Provider requests to complete...')
        yield gen.sleep(settings.CAMPAIGN_LIMIT)

    def handle_request(self, news_provider, response):
        """

        :param news_provider:
        :param response:
        :return:
        """
        gen_log.info('API Response: [%s] %d %r' % (
            news_provider, response.code, response.body))
        if response.code != 200:
            gen_log.error('Response code: %d' % response.code)
            return
        articles = news_handler.handle_http_response(response.body,
                                                     self.campaign.limit)
        gen_log.info('Provider: %s Number of articles: %d ' % (
            news_provider, len(articles)))
        news_processor.process_articles(articles, news_provider, self.campaign)

    @staticmethod
    def handle_errors(api_errors):
        """

        :param
        api_errors:
        :return:
        """
        if api_errors >= settings.API_ERROR_LIMIT:
            gen_log.error('API Exceed Error limit: %d Hostname: %s' % (
                settings.API_ERROR_LIMIT,
                os.uname()[1]))
            return True
