"""Class which represents text when performing texts tasks"""

from api.version1_0.database import DbHelper
from utils.reporting import Generator
from services.nlp import utils as nlp_utils


class TextD(object):
    """
    Text Object to analyze
    """

    def __init__(self):
        """

        :return:
        """
        self.id = 0
        self.reference = Generator.Generator().generate_job(10)
        self.run_sentiment_analysis = False
        self._content = None
        self._location = None
        self._score = 0
        self._magnitude = 0
        self._sentiment_analysis = None

    @property
    def sentiment_analysis(self):
        return self._sentiment_analysis

    @sentiment_analysis.setter
    def sentiment_analysis(self, sentiment_analysis):
        """
        Set sentiment_analysis and update database if valid value.

        :param sentiment_analysis: (tuple)
        :return:
        """
        self._score, self._magnitude = sentiment_analysis

        if sentiment_analysis:
            # Update DB with score, magnitude and sentiment analysis.
            self.update_sentiment(self._score, self._magnitude)

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        self._score = score

    @property
    def magnitude(self):
        return self._magnitude

    @magnitude.setter
    def magnitude(self, magnitude):
        self._magnitude = magnitude

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        self._content = content

    def update_sentiment(self, score, magnitude):
        """Updates scores and magnitude in database. Based on score value
        determined sentiment analysis.

        :param score:
        :param magnitude:
        :return:
        """
        if score and magnitude:
            sentiment = nlp_utils.get_sentiment(score)
            sql_query = 'UPDATE text_analysis SET score=%0.2f, ' \
                        'magnitude=%0.2f, sentiment=\'%s\' WHERE ' \
                        'reference=\'%s\'' % (
                score, magnitude, sentiment, self.reference)
            DbHelper.update_database(sql_query)

    def __repr__(self):
        return self.reference

    def __str__(self):
        return self.reference
