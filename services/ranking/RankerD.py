"""Main instance to sort Articles based on source."""

import logging
import ranker

from api.version1_0.database import DbHelper
from conf import settings
from utils.reporting import Generator
from utils.reporting import Report


class RankerD(object):
    """Reads posts from DB and rank them based on: score, provider, keywords."""

    def __init__(self):
        """

        :return:
        """
        self._campaign_reference = Generator.Generator().generate_job(10)
        self._articles = []
        self._sorted_articles = []
        self._limit = settings.ranking_limit
        self._num_of_articles = 0
        self._provider = None
        self.report = Report.Report(subject='News ML | Daily Ranked Report')
        self._email_recipients = []
        self._send_report = False

    @property
    def campaign_reference(self):
        return self._campaign_reference

    @campaign_reference.setter
    def campaign_reference(self, campaign_reference):
        self._campaign_reference = campaign_reference

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
    def email_recipients(self):
        return self._email_recipients

    @email_recipients.setter
    def email_recipients(self, email_recipients):
        self._email_recipients = email_recipients

    @property
    def send_report(self):
        return self._send_report

    @send_report.setter
    def send_report(self, send_report):
        self._send_report = send_report

    def get_articles(self):
        """Gets latest news already inserted in database.

        :return:
        """
        logging.info('Getting news from Database')
        self.articles = ranker.get_and_rank_news_articles()
        self.num_of_articles = len(self.articles)
        logging.info('News found: %d.', self.num_of_articles)
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
                     len(self.sorted_articles))
        if settings.update_rank_articles_db:
            logging.info('Updating database')
            ranker.update_articles(self.sorted_articles)
            for article in self.sorted_articles:
                self.report.add_content(article._url,
                                        '%s | <b>Score</b>: %d | '
                                        '<b>Provider</b>: %s' % (
                                        article._title,
                                        article.score,
                                        article.source.upper()))
        return self.sorted_articles

    def terminate(self, status=1):
        """Updates campaign status and sends email report if reporting was enabled.

        :param status:
        :return:
        """
        if self.send_report:
            self.report.email_recipients = self.email_recipients
            self.report.send()

        if self.campaign_reference:
            sqlquery = 'UPDATE campaign SET campaign_end=\'%s\', status=%d WHERE campaign.reference=\'%s\'' % (
                settings.dbnow, status, self.campaign_reference)
            DbHelper.update_database(sqlquery)