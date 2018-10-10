"""Implements clustering algorithm."""


class ClusteredNews(object):
    """ Initialize news_id, title, text, source, url"""
    def __init__(self, news_id, title, content, source, url):
        self._news_id = news_id
        self._title = title
        self._content = content
        self._source = source
        self._url = url
        self._cluster = -1

    @property
    def cluster(self):
        return self._cluster

    @cluster.setter
    def cluster(self, cluster):
        self._cluster = cluster

    @property
    def bag_of_words(self):
        return self._content.split()

    @property
    def news_id(self):
        return self._news_id

    @news_id.setter
    def news_id(self, news_id):
        self._news_id = news_id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        self._content = content

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, source):
        self._source = source

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    def __str__(self):
        return "Clustered Post: %r %r %r %s." % (
            self._url,
            self._title.encode('utf-8'),
            self._source,
            self._cluster)

    def __repr__(self):
        return "Clustered Post: %r %r %r %s." % (
            self._url,
            self._title.encode('utf-8'),
            self._source,
            self._cluster)
