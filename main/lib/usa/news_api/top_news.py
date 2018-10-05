"""Collect News information.

This module connects to Google News API.
News API module supports 2 endpoints:
1. Get articles
2. Get sources

We pass the source type and other parameters to client request in order to get top news
We will support a limited list of providers for tech, but API Calls can support and process any of them.

https://newsapi.org/v1/articles?source=<PROVIDER>&sortBy=<SORT_OPTION>&apiKey=<API_KEY>
https://newsapi.org/v1/articles?source=ars-technica&sortBy=top&apiKey=1369bd55461b40e0987191f4ebe094d4

"""
import time

from tornado import ioloop
from tornado.log import gen_log
from main.common import TornadoBacklog


def launch(campaign_instance):
    """

    :param self:
    :param campaign_instance:
    :return:
    """
    start_time = time.time()
    gen_log.info('launch() Initializing...')
    crawler = TornadoBacklog.TornadoBacklog(campaign_instance)
    ioloop.IOLoop.current().run_sync(lambda: crawler.crawl())
    elapsed_time = time.time() - start_time
    gen_log.info('Process took %f seconds processed ' % elapsed_time)
