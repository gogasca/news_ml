"""Process News response."""

import json
import logging

from conf import settings
from conf import logger
from main.common import NewsArticle

log = logger.LoggerManager().getLogger("__app__",
                                       logging_file=settings.APP_LOGFILE)
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


def handle_http_response(response, limit=-1):
    """
    This function handles HTTP responde body in JSON format.
    It receives and JSON object with the following fields:
    -status: str. Example: ok
    -source: str. Example: ars-technica
    -sortBy: str. Example: top
    -articles: list

    :param response:
    :param limit:

    :return: dict(). Articles response
    """
    try:
        articles_processed = {}
        json_response = json.loads(response)
        status = json_response.get('status')
        if status == 'ok':
            articles = json_response.get('articles')
            for article_index, article in enumerate(articles, start=1):
                # Create a News Article instance.
                source_name = article[SOURCE][SOURCE_NAME]
                log.info('Article: [%s] %s' % (source_name, article[TITLE]))
                article_instance = NewsArticle.Article(settings.NEWS_API)
                article_instance.source_id = article.get(SOURCE).get(ID)
                article_instance.source = source_name.upper()
                article_instance.author = article.get(AUTHOR)
                article_instance.title = article.get(TITLE)
                article_instance.description = article.get(DESCRIPTION)
                article_instance.content = article.get(CONTENT)
                article_instance.url = article.get(URL)
                article_instance.url_to_image = article.get(URL_TO_IMAGE)
                article_instance.published_at = article.get(PUBLISHED_AT)
                articles_processed[article_instance.url] = article_instance
                log.info('%r %r', article_instance.author,
                         article_instance.url)
                if article_index == limit:
                    logging.warning('Limit is defined. Skipping other news')
                    break
        else:
            log.error('Request failed. Status: %s' % status)
        return articles_processed
    except ValueError as exception:
        log.exception(exception)
