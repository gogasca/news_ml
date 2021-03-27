"""Ranks articles from Database."""
import logging
import random
import re

from api.version1_0.database import DbHelper
from conf import settings


class RankedArticle(object):
    def __init__(self, news_id, title, content, source, url):
        self._news_id = news_id
        self._title = title
        self._content = content
        self._source = source
        self._url = url
        self._ranking = 0
        self._order = -1
        self._score = 1.0
        self._ranking_source = -1

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        self._score = score

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, source):
        self._source = source

    @property
    def news_id(self):
        return self._news_id

    @news_id.setter
    def news_id(self, news_id):
        self._news_id = news_id

    @property
    def bag_of_words(self):
        return self._content.split

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, source):
        self._source = source

    @property
    def ranking_source(self):
        return self._ranking_source

    @ranking_source.setter
    def ranking_source(self, ranking_source):
        self._ranking_source = ranking_source

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, order):
        self._order = order

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        self._score = score

    def rank(self):
        """Assigns score based on News source. Sources defined in settings file.

        First sources in settings.ranking_sources list get higher score.
        Articles which are generated first are prioritized.
        :return:
        """
        try:
            self.ranking_source = 1 + settings.RANKING_SOURCES.index(
                self.source)
        except ValueError:
            self.ranking_source = settings.UNKNOWN_SOURCE_SCORE

        try:
            self.score += 200 // self.ranking_source
            self.score += self.order + random.randrange(0, 10)
        except ZeroDivisionError as e:
            logging.exception(e)

    def __str__(self):
        return "RankedArticle: (%d) Source: [%r] Ranking: %d Score: (%f) %r,  " \
               "" \
               "" \
               "" \
               "<%r>." % (
                   self.order,
                   self.source,
                   self.ranking_source,
                   self.score,
                   self._title.encode('utf-8'),
                   self._url)

    def __repr__(self):
        return "RankedArticle: (%d) Source: [%r] Ranking: %d Score: (%f) %r,  " \
               "" \
               "" \
               "" \
               "<%r>." % (
                   self.order,
                   self.source,
                   self.ranking_source,
                   self.score,
                   self._title.encode('utf-8'),
                   self._url)


def get_and_rank_news_articles(date='latest'):
    """Get Articles in DB and assigns them a score.

    Args:
        date: (str)

    Returns:
        News information from Database.
    """
    if not date:
        raise ValueError('Invalid date')

    if date == 'latest':
        date = str(DbHelper.get_record(settings.RANKING_QUERY_DATE))
        logging.info('Using latest date. The latest date found was: %s', date)
        if not date:
            raise ValueError('Unable to extract date')

    logging.info('Using date: %s', date)
    if re.match('\d{4}-\d{1,2}-\d{2}', date):
        news = get_articles_by_date(date)
        if news:
            logging.info('Ranking started.')
            return rank_articles(news)
        else:
            raise ValueError('No news found')
    else:
        raise ValueError('Invalid date format')


def get_articles_by_date(date):
    """

    :param date:
    :return: list(List of RankedArticle)
    """
    logging.info('Looking news for %s', date)
    news = DbHelper.get_multiple_records(
        settings.RANKING_QUERY_GET_NEWS_BY_DATE % date)
    if news:
        logging.info('Total news found: %s', len(news))
        return news
    else:
        raise ValueError('No news found')


def rank_articles(news_articles):
    """

    :param news_articles:
    :return:
    """
    ranked_articles = []
    logging.info('Ranking %d posts and assign score.' % len(news_articles))
    for order, news_article in enumerate(news_articles, 1):
        ranked_article = RankedArticle(news_id=news_article[0],
                                       title=news_article[1],
                                       content=news_article[2],
                                       source=news_article[3],
                                       url=news_article[4])
        # Order in which the article was read.
        ranked_article.order = order
        # Rank article based on the source.
        ranked_article.rank()
        logging.info('Added Ranked Article %r', ranked_article)
        ranked_articles.append(ranked_article)
    return ranked_articles


def sort_articles(articles):
    """Sort articles based on score.

    :param articles:
    :return:
    """
    if len(articles) < 1:
        raise ValueError('No news')
    sorted_articles = sorted(articles, key=lambda x: x.score, reverse=True)
    return sorted_articles


def update_articles(articles):
    """

    :param articles:
    :return:
    """
    if not articles:
        raise ValueError('Invalid number of articles')
    for order, article in enumerate(articles, 1):
        logging.info(article)
        DbHelper.update_ranked_post(news_id=article.news_id,
                                    rank_score=article.score,
                                    rank_order=order)
    logging.info('Update %d articles', len(articles))


def process_articles(campaign, limit=100):
    """Test processing and DB insertion.

    :param campaign:
    :param limit:
    :return:
    """
    ranked_articles = get_and_rank_news_articles()
    sorted_articles = sort_articles(ranked_articles)
    if not isinstance(limit, int) and limit > 1:
        raise ValueError('Invalid limit')
    for order, article in enumerate(sorted_articles[:limit], 1):
        logging.info(article)
        DbHelper.update_ranked_post(news_id=article.news_id,
                                    rank_score=article.score,
                                    rank_order=order)
    logging.info('Process %d articles', order)


def print_articles(campaign):
    """Test processing

    :param campaign:
    :return:
    """
    articles = get_and_rank_news_articles()
    sorted_articles = sort_articles(articles)
    logging.info('Found %d articles. Printing results:', len(sorted_articles))
    for article in sorted_articles:
        print(article)
