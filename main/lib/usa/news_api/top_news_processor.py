"""Read News from Google API."""

import logging
from api.version1_0.database import DbHelper
from conf import settings
from conf import logger
from services.nlp import nlp
from services.nlp import utils as nlp_utils
from services.translate import utils as translate_utils
from utils import url_extract
from utils.reporting import Report

log = logger.LoggerManager().getLogger("__app__",
                                       logging_file=settings.app_logfile)
log.setLevel(level=logging.DEBUG)


def process_articles(articles, news_provider, campaign_instance):
    """

    :param articles:
    :param news_provider:
    :param campaign_instance:
    :return:
    """

    num_of_articles = len(articles)
    log.info('Analyzing %d articles...', len(articles))
    if num_of_articles > 1:
        campaign_instance.set_articles(num_of_articles)
        # Create Report instance and attach recipients.
        if campaign_instance.send_report:
            subject = 'Silicon Valley | Daily Automatic Summary Report | News ' \
                      '' \
                      '' \
                      '' \
                      '' \
                      '' \
                      'API | %s' % news_provider
            report = Report.Report(subject=subject)
            report.email_recipients = campaign_instance.email_recipients
        for _, article in articles.items():
            if article.description:
                log.info(
                    'Analyzing article %r, %r' % (article.title, article.url))
                new_article = False
                if not DbHelper.item_exists(article.url):
                    log.info('Inserting into database')
                    news_id = None
                    try:
                        score, magnitude = nlp_utils.get_sentiment_scores(
                            article.content or article.description)
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
                            log.error('Unable to Insert record %s', article.url)
                            continue
                    except (ValueError, UnicodeDecodeError) as exception:
                        log.exception(exception)
                    new_article = True
                    log.info('Processing content for : %s', article.url)
                    entities = nlp.analyze_entities(
                        '%r %r' % (article.title, article.description))
                    num_of_entities = len(entities)
                    log.info('Processing %d entities: %s', num_of_entities,
                             article.url)
                    if num_of_entities > 1:
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
                        log.info('Processing persons: %s', article.url)
                        persons = nlp_utils.extract_entity(entities)
                        log.info('Found %d persons', len(persons))
                        for person in persons:
                            DbHelper.insert_person(person)
                        log.info('Processing organizations: %s', article.url)
                        organizations = nlp_utils.extract_entity(entities,
                                                                 'ORGANIZATION')
                        log.info('Found %d organizations', len(organizations))
                        for organization in organizations:
                            DbHelper.insert_company(organization)
                    else:
                        log.error('No entities found')
                else:
                    log.warning('Article %r already exists ', article.url)

                if campaign_instance.translation_enable:
                    log.info('Translating: %s', article.url)
                    if new_article:
                        log.info('Translating...%r', article.url)
                        translated_text = translate_utils.translate_content(
                            article.title + ' ' + article.description,
                            campaign_instance.translation_lang)
                        sql_query = translate_utils.create_sql_query(
                            translated_text, settings.default_language,
                            news_id)
                        if sql_query:
                            DbHelper.update_database(sql_query)
                    else:
                        translated_text = translate_utils.translate_content(
                            article.title + ' ' + article.description,
                            campaign_instance.translation_lang)
                    if campaign_instance.send_report and len(
                            translated_text) > 1:
                        log.info('Adding translated information to report')
                        report.add_content(article.url, translated_text)
                elif campaign_instance.send_report:
                    log.info('Adding article information to report: %s %s' % (
                        article.title, article.url))
                    report.add_content(article.url, article.title)
            else:
                log.error('Not content found: %s', article.url)
    else:
        log.error('No titles found')
    if campaign_instance.send_report:
        log.info('Sending email notification...')
        report.send()
    log.info('Extraction completed')
