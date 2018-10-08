import json
import logging

from conf import settings
from conf import logger
from main.common import NewsArticle

log = logger.LoggerManager().getLogger("__app__",
                                       logging_file=settings.app_logfile)
log.setLevel(level=logging.DEBUG)

AUTHOR = 'author'
CONTENT = 'content'
DESCRIPTION = 'description'
ID = 'id'
PUBLISHED_AT = 'publishedAt'
TITLE = 'title'
URL = 'url'
URL_TO_IMAGE = 'urlToImage'
SOURCE = 'source'
SOURCE_NAME = 'name'
STATUS = 'status'


def handle_http_response(response):
    """
    This function handles HTTP responde body in JSON format.
    It receives and JSON object with the following fields:
    -status: str. Example: ok
    -source: str. Example: ars-technica
    -sortBy: str. Example: top
    -articles: list

    :param response:
    :return: dict(). Articles response
    """
    try:
        articles_processed = {}
        json_response = json.loads(response)
        status = json_response.get('status')
        if status == 'ok':
            articles = json_response['articles']
            for article in articles:
                # Create a News Article instance.
                source_name = article[SOURCE][SOURCE_NAME]
                log.info('New Article: %s %s' % (source_name, article[TITLE]))
                article_instance = NewsArticle.Article(settings.news_api)
                article_instance.source_id = article[SOURCE][ID]
                article_instance.source = source_name.upper()
                article_instance.author = article[AUTHOR]
                article_instance.title = article[TITLE]
                article_instance.description = article[DESCRIPTION]
                article_instance.content = article[CONTENT]
                article_instance.url = article[URL]
                article_instance.url_to_image = article[URL_TO_IMAGE]
                article_instance.published_at = article[PUBLISHED_AT]
                articles_processed[article_instance.url] = article_instance
                log.info('%r %r', article_instance.author,
                         article_instance.url)
        else:
            log.error('Request failed. Status: %s' % status)
        return articles_processed
    except ValueError as exception:
        log.exception(exception)
