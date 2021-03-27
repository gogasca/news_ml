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


def process_entities(article, news_id, db_update=True):
    """

    :param article:
    :param news_id:
    :param db_update:
    :return:
    """
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = settings.CREDENTIALS
    log.info('process_entities() Processing content for : %s using NLP',
             article.url)
    num_of_entities = 0
    entities = nlp.analyze_entities(
        '%r %r' % (article.title, article.description))
    if entities:
        num_of_entities = len(entities)
    if num_of_entities < 1:
        log.error('No NLP entities found')
        return

    log.info('Processing %d entities: %s', num_of_entities, article.url)
    # Extract tags and associate them with original article.

    log.info('Processing article tags: %s', article.url)
    tags = nlp_utils.extract_tags(entities)
    log.info('Found %d tags', len(tags))

    log.info('Processing persons in tags: %s', article.url)
    persons = nlp_utils.extract_entity(entities, 'PERSON')
    log.info('Found %d persons', len(persons))

    log.info('Processing organizations in tags: %s', article.url)
    organizations = nlp_utils.extract_entity(entities, 'ORGANIZATION')
    log.info('Found %d organizations', len(organizations))

    if db_update:
        log.info('Updating database...')
        for tag in tags:
            tag_id = DbHelper.insert_tag(tag_name=tag)
            if news_id and tag_id:
                DbHelper.associate_tag_news(news_id, tag_id)
        for person in persons:
            DbHelper.insert_person(person)
        for organization in organizations:
            DbHelper.insert_company(organization)

    return {'persons': persons, 'organizations': organizations}
