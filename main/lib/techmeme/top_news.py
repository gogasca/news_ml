"""Crawls TechMeme URL"""

from bs4 import BeautifulSoup
from datetime import datetime

import logging
import itertools
import requests

from api.version1_0.database import DbHelper
from conf import settings
from conf import logger
from conf import constants
from main.common.NewsArticle import Article
from main.common import utils as common_utils
from services.nlp import utils as nlp_utils
from services.translate import utils as translate_utils
from services.twitter import utils as twitter_utils
from utils import url_extract
from utils.reporting import Report

log = logger.LoggerManager().getLogger("__app__",
                                       logging_file=settings.APP_LOGFILE)
log.setLevel(level=logging.DEBUG)

_HTML_TITLE_CLASS = 'ourh'


def extract_articles(url=None):
    """
    Extracts titles from Techememe Popular web page.
    Extract title, short url and article content.
    Based on URL creates a dictionary of objects. This URL serves as index
    Currently TechMeme does not have Content field, we extract summary.

    :param url:
    :return: articles
    """
    try:
        if not url:
            raise ValueError('URL not found')
        response = requests.get(url)
        soup = BeautifulSoup(response.content, constants.LXML)
        titles_html = soup.find_all('a', class_=_HTML_TITLE_CLASS)
        published_dates = soup.find_all('div', class_='itc2')
        published_dates = [article.get('id') for article in published_dates if
                           article.get('id')]
        log.info('Found %d articles: [%d]', len(titles_html),
                 len(published_dates))
        articles = {}
        for title in titles_html:
            url = title.get('href')
            if not articles.get(url):
                article_instance = Article(settings.TECHMEME)
                article_instance.url = url
                article_instance.title = title.text
                article_instance.content = title.text
                if published_dates:
                    article_instance.published_at = published_dates.pop(0)[:6]
                articles[title['href']] = article_instance
        log.info('Created %d article objects', len(articles))
        return articles
    except Exception as e:
        log.exception('We failed with error - %s.', e)


def launch(campaign_instance=None):
    """
    The logic is as follows:
        1. Extract Articles from <Provider: (Techmeme, Techcrunch)> web page
        2. For each article extract title, short url and content.
        3. Translate Article information
        4. Use Google NLP to extract meaningful keywords from content
        5. Insert record in database.
        6. Send report.

    :param campaign_instance:
    :return:
    """
    entities = None
    news_id = None
    num_of_articles = 0
    translated_text = None
    tweets = []
    articles = extract_articles(settings.TECHMEME_URL)
    if articles:
        num_of_articles = len(articles)
    else:
        logging.error('No articles found.')
    report = Report.Report(subject=settings.TECHMEME_REPORT)

    log.info('Retrieving %d articles...', num_of_articles)
    if campaign_instance.limit > 0:
        logging.warning('Limit is defined. Skipping other news')
        articles = dict(
            itertools.islice(articles.items(), campaign_instance.limit))
        num_of_articles = len(articles)
    if num_of_articles < 1:
        log.error('No articles found')
        if campaign_instance.send_report:
            log.warning('Skipping report via email...')
        return
    log.info('Processing %d articles...', num_of_articles)
    campaign_instance.set_articles(num_of_articles)
    # Create Report instance and attach recipients.
    log.info('Translation enabled: %s', campaign_instance.translation_enable)
    log.info('Email reporting enabled: %s', campaign_instance.send_report)
    log.info('Twitter enabled: %s', campaign_instance.twitter)
    log.info('Twitter image extraction: %s', settings.EXTRACT_TWITTER_IMAGE)
    if campaign_instance.send_report:
        report.email_recipients = campaign_instance.email_recipients
    for _, article in articles.items():
        new_article = False
        if not article.title:
            log.warning('No title found. Article won\'t be inserted')
            continue
        if settings.EXTRACT_TWITTER_IMAGE:  # meta:twitter:image
            article.twitter_image = twitter_utils.get_twitter_element(
                article.url, 'twitter:image')
        log.info('Article: %s, [%s], [%s]', article.title, article.url,
                 article.twitter_image)
        if not DbHelper.record_exists(article.url):
            news_id = None
            log.info('New Article retrieved: %r, %r' % (
                article.title, article.url))
            try:
                log.info('Processing sentiment analysis')
                score, magnitude = nlp_utils.get_sentiment_scores(
                    article.content)
                source = url_extract.get_domain(article.url) or ''
                log.info('Insert article into Database')
                news_id = DbHelper.insert_news(title=article.title,
                                               content=article.content,
                                               url=article.url,
                                               provider=settings.TECHMEME,
                                               source=source.upper(),
                                               source_id=source,
                                               campaign=campaign_instance.reference,
                                               score=score,
                                               magnitude=magnitude,
                                               sentiment=nlp_utils.get_sentiment(
                                                   score)
                                               )
                if not news_id:
                    log.error('Unable to insert record %s', article.url)
                    continue
            except (ValueError, UnicodeDecodeError) as exception:
                log.exception(exception)
            new_article = True
            if settings.PROCESS_ENTITIES:
                entities = common_utils.process_entities(article, news_id)
        else:
            log.warning('Article already exists.')

        if campaign_instance.translation_enable:
            translated_text = translate_utils.translate_article(
                campaign_instance, article, new_article, news_id)
            if translated_text:
                log.info('Adding translated content to report.')
                article.title = translated_text
            else:
                logging.warning('Translated text is empty.')

        if campaign_instance.send_report:
            # Only send today articles in Report.
            today = datetime.now().date()
            published_at = datetime.strptime(article.published_at,
                                             '%y%m%d').date()
            if settings.REPORT_ALL_DATES_ARTICLES:
                log.info('Publishing all dates articles')
            log.info('Today: %s Report date: %s. ', today, published_at)
            if today == published_at or settings.REPORT_ALL_DATES_ARTICLES:
                log.info(
                    'Adding article information to Report: %s %s' % (
                        article.title, article.url))
                report.add_content(article.url, article.title,
                                   article.twitter_image)
            else:
                log.warning(
                    'Article published date is not today (%s), '
                    'skipping article from Report', published_at)

        if campaign_instance.twitter:
            tweet_text = article.title
            if campaign_instance.translation_enable:
                tweet_text = translated_text
            tweets.append('{} {}'.format(tweet_text, article.url))

    if campaign_instance.send_report:
        log.info('Sending email notification...')
        report.send()

    if campaign_instance.twitter:
        log.info('Sending Tweets...')
        twitter_utils.send_tweets(tweets, campaign_instance.twitter_delay)

    log.info('Extraction completed')
