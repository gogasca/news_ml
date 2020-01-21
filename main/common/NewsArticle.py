"""Main Article class"""

import logging

from conf import logger
from conf import settings

log = logger.LoggerManager().getLogger("__app__",
                                       logging_file=settings.APP_LOGFILE)
log.setLevel(level=logging.DEBUG)


class Article(object):
    """A class representing an Article from News.
    Each Article shares common properties.
    """
    def __init__(self, provider):
        self._provider = provider
        self._author = ''
        self._content = ''
        self._description = ''
        self._published_at = ''
        self._source_id = ''
        self._source = ''
        self._title = ''
        self._url_to_image = ''
        self._url = ''
        self._twitter_image = ''

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, author):
        if author:
            self._author = author.replace('\'', '')
        else:
            log.warning('No author defined')

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        if content:
            self._content = content.replace('\'', '')
        else:
            log.warning('No content defined')

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        if description:
            self._description = description.replace('\'', '')

    @property
    def provider(self):
        return self._provider

    @provider.setter
    def provider(self, provider):
        self._provider = provider

    @property
    def source_id(self):
        return self._source_id

    @source_id.setter
    def source_id(self, source_id):
        self._source_id = source_id

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, source):
        self._source = source

    @property
    def published_at(self):
        return self._published_at

    @published_at.setter
    def published_at(self, published_at):
        self._published_at = published_at

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    @property
    def url_to_image(self):
        return self._url_to_image

    @url_to_image.setter
    def url_to_image(self, url_to_image):
        if url_to_image:
            self._url_to_image = url_to_image
        else:
            log.warning('No image url defined')

    @property
    def twitter_image(self):
        return self._twitter_image

    @twitter_image.setter
    def twitter_image(self, twitter_image):
        self._twitter_image = twitter_image

    def __repr__(self):
        return 'Article: <{}> Title: <{}>'.format(self._url, self._title)

    def __str__(self):
        return 'Article: <{}> Title: <{}>'.format(self._url, self._title)
