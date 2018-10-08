"""Ranks articles from Database."""
import logging
import random

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
    def news_id(self):
        return self._news_id

    @news_id.setter
    def news_id(self, news_id):
        self._news_id = news_id

    @property
    def bag_of_words(self):
        return self._content.split

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

        :return:
        """
        try:
            self._ranking_source = 1.001 ** settings.ranking_sources.index(
                self._source)
        except ValueError:
            self._ranking_source = settings.unknown_source_score

        try:
            # Divide score by ranking source, higher sources get higher score.
            self.score += 20 // self._ranking_source
            # Articles which are displayed first are prioritized.
            self.score += self.order + random.randrange(0, 10)
        except ZeroDivisionError as e:
            logging.exception(e)

    def __str__(self):
        return "RankedArticle: (%d) Source: [%r] Ranking: %d Score: (%f) %r,  " \
               "" \
               "" \
               "" \
               "" \
               "<%r>." % (
                   self.order,
                   self._source,
                   self._ranking_source,
                   self.score,
                   self._title.encode('utf-8'),
                   self._url)

    def __repr__(self):
        return "RankedArticle: (%d) Source: [%r] Ranking: %d Score: (%f) %r,  " \
               "" \
               "" \
               "" \
               "" \
               "<%r>." % (
                   self.order,
                   self._source,
                   self._ranking_source,
                   self.score,
                   self._title.encode('utf-8'),
                   self._url)


def get_and_rank_news_articles(campaign):
    """Get Articles in DB and assigns them a score.

    Args:
        campaign: (str)
        date: (str) Date format could be: 2017-07-27
                    date = time.strftime('%Y-%m-%d')
    Returns:
        News information from Database.
    """
    if not campaign:
        raise ValueError('Invalid campaign')

    news = DbHelper.get_multiple_records(
        settings.ranking_query_get_news % campaign)
    if news:
        logging.info('Ranking started.')
        return rank_articles(news)
    else:
        raise ValueError('No news found')


def rank_articles(news_articles):
    """

    :param news_articles:
    :return:
    """
    ranked_articles = []
    order = 1
    logging.info('Ranking %d posts and assign score.' % len(news_articles))
    for news_article in news_articles:
        ranked_article = RankedArticle(news_id=news_article[0],
                                       title=news_article[1],
                                       content=news_article[2],
                                       source=news_article[3],
                                       url=news_article[4])
        # Order in which the article was read.
        ranked_article.order = order
        # Rank article based on the source.
        ranked_article.rank()
        ranked_articles.append(ranked_article)
        logging.info('Added Ranked Article %r', ranked_article)
        order += 1
    return ranked_articles


def sort_articles(articles):
    """Sort articles based on score.

    :param articles:
    :return:
    """
    if articles < 1:
        raise ValueError('No news')
    sorted_articles = sorted(articles, key=lambda x: x.score, reverse=True)
    return sorted_articles


def process_articles(campaign, limit=10):
    """

    :param campaign:
    :param limit:
    :return:
    """
    ranked_articles = get_and_rank_news_articles(campaign=campaign)
    sorted_articles = sort_articles(ranked_articles)
    order = 0
    if not isinstance(limit, int) and limit > 1:
        raise ValueError('Invalid limit')

    for article in sorted_articles[:limit]:
        logging.info(article)
        order += 1
        DbHelper.update_ranked_post(news_id=article.news_id,
                                    rank_score=article.score,
                                    rank_order=order)
    logging.info('Process %d articles', order)


def print_articles(campaign):
    """

    :param campaign:
    :return:
    """
    articles = get_and_rank_news_articles(campaign=campaign)
    sorted_articles = sort_articles(articles)
    logging.info('Found %d articles. Printing results:', len(sorted_articles))
    for article in sorted_articles:
        print article


process_articles('E1GPL5QY6Q')
