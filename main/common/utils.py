"""Common libraries."""

import logging
import os

from api.version1_0.database import DbHelper
from conf import settings
from conf import logger
from services.nlp import nlp
from services.nlp import utils as nlp_utils
from utils import url_extract

log = logger.LoggerManager().getLogger("__app__",
                                       logging_file=settings.APP_LOGFILE)
log.setLevel(level=logging.DEBUG)


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
        if tag != '' and len(tag) > 1:
            tag_id = DbHelper.insert_tag(tag_name=tag,
                                         source=url_extract.get_domain(
                                             article.url))
            if news_id and tag_id:
                DbHelper.associate_tag_news(news_id, tag_id)
    # Extract entities.
    log.info('Processing persons in tags: %s', article.url)
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