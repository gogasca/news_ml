"""Send Tweets."""

import logging
import time
import tweepy
from services.twitter import config


log = logging.getLogger()


def send_tweets(tweets, delay):
    """

    :param tweets:
    :param delay:
    :return:
    """
    twitter_api = config.create_api()
    for tweet in tweets:
        try:
            if twitter_api.update_status(tweet):
                log.info('Tweet posted')
        except tweepy.error.TweepError as e:
            log.exception(e)
        time.sleep(delay)
