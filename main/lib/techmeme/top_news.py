"""Crawls TechMeme URL"""

from bs4 import BeautifulSoup

import logging
import itertools
import os
import requests


from api.version1_0.database import DbHelper
from conf import settings
from conf import logger
from conf import constants
from main.common.NewsArticle import Article
from services.nlp import nlp
from services.nlp import utils as nlp_utils
from services.translate import utils as translate_utils
from services.twitter import utils as twitter_utils
from utils import url_extract
from utils.reporting import Report

log = logger.LoggerManager().getLogger("__app__",
                                       logging_file=settings.APP_LOGFILE)
log.setLevel(level=logging.DEBUG)

_HTML_TITLE_CLASS = 'ourh'


def process_entities(article, news_id):
    """

    :param article:
    :param news_id:
    :return:
    """
    log.info('process_entities() Processing content for : %s using NLP',
             article.url)
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = settings.CREDENTIALS
    entities = nlp.analyze_entities(
        '%r %r' % (article.title, article.description))
    num_of_entities = 0
    if entities:
        num_of_entities = len(entities)
    if num_of_entities < 1:
        log.error('No NLP entities found')
        return
    log.info('Processing %d entities: %s', num_of_entities, article.url)
    # Extract tags and associate them with original article.
    log.info('Processing article tags: %s', article.url)
    tags = nlp_utils.extract_tags(entities)
    for tag in tags:
        if tag != '':
            tag_id = DbHelper.insert_tag(tag_name=tag,
                                          source=url_extract.get_domain(
                                              article.url))
            if news_id and tag_id:
                DbHelper.associate_tag_news(news_id, tag_id)
                log.info('Processing persons in tags: %s', article.url)
    # Extract entities.
    persons = nlp_utils.extract_entity(entities, 'PERSON')
    log.info('Found %d persons', len(persons))
    for person in persons:
        DbHelper.insert_person(person)
    log.info('Processing organizations in tags: %s', article.url)
    organizations = nlp_utils.extract_entity(entities, 'ORGANIZATION')
    log.info('Found %d organizations', len(organizations))
    for organization in organizations:
        DbHelper.insert_company(organization)
    return {'persons': persons, 'organizations': organizations}


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
        titles_html = soup.find_all("a", class_=_HTML_TITLE_CLASS)
        articles = {}
        for title in titles_html:
            article_instance = Article(settings.TECHMEME)
            article_instance.title = title.text
            article_instance.content = title.text
            article_instance.url = title[constants.HTML_HREF]
            articles[title[constants.HTML_HREF]] = article_instance
        log.info('Found %d articles', len(articles))
        return articles
    except Exception as e:
        log.exception('We failed with error - %s.', e)


def translate_article(campaign_instance, article, new_article, report, news_id):
    """

    :param campaign_instance:
    :param article:
    :param new_article:
    :param report:
    :param news_id:
    :return:
    """
    # Perform translation using Google Translate API
    log.info('Translating...%r', article.url)
    translated_text = translate_utils.translate_content(
        article.title, campaign_instance.translation_lang)
    if new_article:
        # Update database record
        sql_query = translate_utils.create_sql_query(
            translated_text, settings.DEFAULT_LANGUAGE, news_id)
        DbHelper.update_database(sql_query)
    else:
        log.warn('Article already exists, skipping DB update')
    if campaign_instance.send_report and len(translated_text) > 1:
        log.info('Adding translated information to report.')
        report.add_content(article.url, translated_text)
    return translated_text


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
    news_id = None
    tweets = []
    articles = extract_articles(settings.TECHMEME_URL)
    num_of_articles = len(articles)
    report = Report.Report(subject=settings.TECHMEME_REPORT)
    log.info('Retrieved %d articles...', num_of_articles)
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
    log.info('Reporting enabled: %s', campaign_instance.send_report)
    log.info('Twitter enabled: %s', campaign_instance.twitter)
    if campaign_instance.send_report:
        report.email_recipients = campaign_instance.email_recipients
    for _, article in articles.items():
        if not article.title:
            log.warning('No title found. Article won\'t be inserted')
            continue
        log.info('Analyzing article %s, %s', article.title, article.url)
        new_article = False

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
                entities = process_entities(article, news_id)
        else:
            log.warning('Article already exists.')

        if campaign_instance.twitter:
            tweet_text = article.title
            if campaign_instance.translation_enable:
                tweet_text = translated_text
            tweets.append('{} {}'.format(tweet_text, article.url))

        if campaign_instance.translation_enable:
            translated_text = translate_article(campaign_instance, article,
                                                new_article, report, news_id)
        elif campaign_instance.send_report:
            log.info('Adding information to report.')
            report.add_content(article.url, article.title)
        else:
            pass

    if campaign_instance.send_report:
        log.info('Sending email notification...')
        report.send()

    if campaign_instance.twitter:
        log.info('Sending Tweets...')
        twitter_utils.send_tweets(tweets, campaign_instance.twitter_delay)

    log.info('Extraction completed')
