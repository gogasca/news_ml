"""Main instance to sort Articles based on source."""

import logging
import ranker

from conf import settings


class RankerD(object):
    """Reads posts from DB and rank them based on: score, provider, keywords."""

    def __init__(self, reference):
        """

        :return:
        """
        self._articles = []
        self._sorted_articles = []
        self._limit = settings.ranking_limit
        self._num_of_articles = 0
        self._provider = None
        self._reference = reference

    @property
    def articles(self):
        return self._articles

    @articles.setter
    def articles(self, articles):
        self._articles = articles

    @property
    def sorted_articles(self):
        return self._sorted_articles

    @sorted_articles.setter
    def sorted_articles(self, sorted_articles):
        self._sorted_articles = sorted_articles

    @property
    def num_of_articles(self):
        return self._num_of_articles

    @num_of_articles.setter
    def num_of_articles(self, num_of_articles):
        self._num_of_articles = num_of_articles

    @property
    def provider(self):
        return self._provider

    @provider.setter
    def provider(self, provider):
        self._provider = provider

    @property
    def reference(self):
        return self._reference

    @reference.setter
    def reference(self, reference):
        self._reference = reference

    def get_articles(self):
        """Gets latest news already inserted in database.

        :return:
        """
        logging.info('Reading news from Database...')
        self.articles = ranker.get_and_rank_news_articles(
            campaign=self.reference)
        self.num_of_articles = len(self.articles)
        logging.info('News found: %d.', self._num_of_articles)
        return self.articles

    def rank_articles(self):
        """Reads posts from DB. Filters unwanted providers. Then rank them.

        :return:
        """
        self.articles = self.get_articles()
        logging.info('Sorting %d articles by score.', len(self.articles))
        if self.articles:
            self.sorted_articles = ranker.sort_articles(self.articles)
        logging.info('Completed Ranking of %d articles(s).',
                     len(self._sorted_articles))
        if settings.update_rank_articles_db:
            logging.info('Updating database')
            ranker.update_articles(self.sorted_articles)
        return self.sorted_articles