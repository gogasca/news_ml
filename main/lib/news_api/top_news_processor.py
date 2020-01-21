"""Read News from Google API."""

import logging
from datetime import datetime

from api.version1_0.database import DbHelper

from conf import settings
from conf import logger

from main.common import utils as common_utils
from services.nlp import utils as nlp_utils
from services.twitter import utils as twitter_utils
from services.translate import utils as translate_utils

from utils.reporting import Report

log = logger.LoggerManager().getLogger("__app__",
                                       logging_file=settings.APP_LOGFILE)
log.setLevel(level=logging.DEBUG)


def process_articles(articles, news_provider, campaign_instance):
    """Get content from News API.
    For each article verifies if exists in DB or not.
    If exists, ignore it, otherwise, process each field.
    Perform sentiment analysis on article content or description fields.


    :param articles:
    :param news_provider:
    :param campaign_instance:
    :return:
    """
    news_id = None
    translated_text = None
    tweets = []
    num_of_articles = len(articles)
    campaign_instance.set_articles(num_of_articles)
    report = Report.Report(subject='News ML | %s' % news_provider)

    log.info('Analyzing %d articles...', num_of_articles)
    if num_of_articles < 1:
        if campaign_instance.send_report:
            log.warning('Skipping report via email...')
        log.error('No titles found')
        return
    # Create Report instance and attach recipients.
    log.info('Translation enabled: %s', campaign_instance.translation_enable)
    log.info('Email reporting enabled: %s', campaign_instance.send_report)
    log.info('Twitter enabled: %s', campaign_instance.twitter)
    log.info('Twitter image extraction: %s', settings.EXTRACT_TWITTER_IMAGE)

    if campaign_instance.send_report:
        report.email_recipients = campaign_instance.email_recipients

    for _, article in articles.items():
        new_article = False
        if not article.description:
            log.error('Not description found in article: %s', article.url)
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
                    article.content or article.description)
                log.info('Insert article into Database')
                news_id = DbHelper.insert_news(title=article.title,
                                               author=article.author,
                                               description=article.description,
                                               content=article.content,
                                               url=article.url,
                                               url_to_image=article.url_to_image,
                                               source_id=article.source_id,
                                               source=article.source,
                                               campaign=campaign_instance.reference,
                                               published_at=article.published_at,
                                               score=score,
                                               magnitude=magnitude,
                                               sentiment=nlp_utils.get_sentiment(
                                                   score))
                if not news_id:
                    log.error('Unable to insert record %s', article.url)
                    continue
            except (ValueError, UnicodeDecodeError) as exception:
                log.exception(exception)
            new_article = True
            if settings.PROCESS_ENTITIES:
                entities = common_utils.process_entities(article, news_id)
        else:
            log.warning('Article %r already exists ', article.url)

        if campaign_instance.translation_enable:
            translated_text = translate_utils.translate_article(
                campaign_instance, article,
                new_article, news_id)
            if len(translated_text) > 1:
                log.info('Adding translated content to report.')
                article.title = translated_text
            else:
                logging.error('Translated text is empty.')

        if campaign_instance.send_report:
            # Only send today articles in Report.
            today = datetime.now().date()
            published_at = datetime.strptime(article.published_at[:10],
                                             '%Y-%m-%d').date()
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

        # Handle Twitter
        if campaign_instance.twitter:
            tweet_text = article.title
            if campaign_instance.translation_enable:
                tweet_text = translated_text
            tweets.append('{} {}'.format(tweet_text, article.url))

    if campaign_instance.send_report:
        log.info('Sending report via email...')
        report.send()

    if campaign_instance.twitter:
        log.info('Sending Tweets')
        twitter_utils.send_tweets(tweets, campaign_instance.twitter_delay)

    log.info('Extraction completed')
