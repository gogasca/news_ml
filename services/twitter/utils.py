"""Send Tweets."""

from bs4 import BeautifulSoup
import logging
import time
import tweepy
import requests
from conf import settings
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


def get_twitter_element(url, element):
    """

    :return:
    """
    headers = requests.utils.default_headers()
    headers.update(
        { 'User-Agent': settings.USER_AGENT,
          }
    )
    session = requests.Session()
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    element_class = soup.find_all('meta', attrs={"name": element})
    if not element_class:
        logging.error('No Twitter image found in {}'.format(url))
        return
    twitter_element = element_class[0].get('content')
    if not twitter_element:
        logging.warning('Element: {} not found'.format(element))
    return twitter_element


def add_hash_tags(tweet, entities):
    """For all entities add hashtags to words.
    Example:
        tweet: Thai startup Lightnet, which aims to provide remittance services in Southeast Asia through its Stellar based blockchain network, raises $31.2M Series A
        entities: return {'persons': [], 'organizations': ['Lightnet', 'Stellar', 'blockchain']}
        for _,
    :param tweet:
    :param entities:
    :return:
    """
    if tweet is None:
        raise ValueError('No tweet defined')
    if entities is None:
        raise ValueError('No entities defined')
    persons = list(entities.values())[0] or []
    organizations = list(entities.values())[1] or []
    for person in persons:
        tweet = tweet.replace(person, '#{}'.format(person))
    for organization in organizations:
        tweet = tweet.replace(organization, '#{}'.format(organization))
    return tweet
