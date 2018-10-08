"""Campaign information."""

from conf import settings
from utils.reporting import Generator
from api.version1_0.database import DbHelper

from services.sms import send_sms


class CampaignD(object):
    """Crawler object in charge of launching Web requests."""

    def __init__(self):
        """

        :return:
        """
        self.reference = Generator.Generator().generate_job(10)
        self._provider = None
        self._query = ''
        self._send_report = False
        self._email_recipients = []
        self._sms_enabled = False
        self._sms_recipients = []
        self._translation_enable = False
        self._translation_lang = None
        self._test = False
        self._status = 0
        self._num_of_articles = 0

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
    def sms_enabled(self):
        return self._sms_enabled

    @sms_enabled.setter
    def sms_enabled(self, sms_enabled):
        self._sms_enabled = sms_enabled

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, query):
        self._query = query

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

    @property
    def translation_enable(self):
        return self._translation_enable

    @translation_enable.setter
    def translation_enable(self, translation_enable):
        self._translation_enable = translation_enable

    @property
    def translation_lang(self):
        return self._translation_lang

    @translation_lang.setter
    def translation_lang(self, translation_lang):
        self._translation_lang = translation_lang

    @property
    def test(self):
        return self._test

    @test.setter
    def test(self, test):
        self._test = test

    def add_email_recipient(self, recipient):
        """

        :param recipient:
        :return:
        """
        if recipient:
            self._email_recipients.append(recipient)

    def add_sms_recipient(self, recipient):
        """

        :param recipient:
        :return:
        """

        if recipient:
            self._sms_recipients.append(recipient)

    def set_articles(self, num_of_articles):
        """

        :param num_of_articles:
        :return:
        """
        if isinstance(num_of_articles, int):
            self.num_of_articles = num_of_articles

        if self.reference and num_of_articles > -1:
            sqlquery = 'UPDATE campaign SET articles=%s WHERE ' \
                       'campaign.reference=\'%s\'' % (
                           num_of_articles, self.reference)
            DbHelper.update_database(sqlquery)

    def terminate(self, status='1'):
        """

        :param status:
        :return:
        """

        if self.reference:
            sqlquery = 'UPDATE campaign SET campaign_end=\'%s\', status=%s ' \
                       'WHERE campaign.reference=\'%s\'' % (
                           settings.dbnow, status, self.reference)
            DbHelper.update_database(sqlquery)
        # Notify via SMS.
        send_sms.send_sms_alert(
            body='Campaign: %s for [%s] %d articles completed' % (
                self.reference, self.provider,
                self.num_of_articles))

    def __repr__(self):
        return self.reference

    def __str__(self):
        return self.reference
