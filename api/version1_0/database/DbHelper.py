"""Helper function for DB operations."""

import logging
import psycopg2
import psycopg2.extensions

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

from api.version1_0.database import Db
from conf import logger
from conf import settings

if settings.remove_stop_words:
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize

log = logger.LoggerManager().getLogger("__app__",
                                       logging_file=settings.app_logfile)
log.setLevel(level=logging.DEBUG)

DB_NOW = 'now()'
SEPARATOR = "','"


def item_exists(url, table='news'):
    """

    :param url:
    :param table:
    :return: boolean
    """
    try:
        if url:
            sql_query = """SELECT url FROM %s WHERE url='%s'""" % (
                table, url.strip())
            db = Db.Db()
            db.initialize(dsn=settings.SQLALCHEMY_DSN)
            result = db.query(sql_query)
            if result:
                return True
            return False
    except psycopg2.ProgrammingError as exception:
        log.exception(exception)


def insert_news(title=None, author='', description='', content='', url='',
                url_to_image='', source_id='', source='', campaign='',
                published_at='', score=0, magnitude=0, sentiment='',
                **kwargs):
    """

    :param title:
    :param author:
    :param description:
    :param content:
    :param url:
    :param url_to_image:
    :param source_id:
    :param source:
    :param campaign:
    :param published_at:
    :param kwargs:
    :return:
    """
    try:
        if not (title and url):
            raise ValueError('Title or url missing')
        sql_query = \
            "INSERT INTO news (" \
            "title, author, description, content, url, url_to_image, " \
            "source_id, source, campaign, published_at, score, magnitude, " \
            "sentiment, inserted_at ) " \
            "VALUES ('%s','%s','%s','%s', '%s','%s','%s','%s','%s','%s', " \
            "%s, %s, '%s', '%s')" \
            % (title.replace("'", "''"),
               author.replace("'", "''"),
               description.replace("'", "''"),
               content[:settings.content_size].replace("'", "''"),
               url,
               url_to_image,
               source_id,
               source,
               campaign,
               published_at,
               score,
               magnitude,
               sentiment,
               DB_NOW)
        db = Db.Db()
        db.initialize(dsn=settings.SQLALCHEMY_DSN)
        return db.insert_content(sql_query, 'news_id')
    except psycopg2.ProgrammingError as exception:
        log.exception(exception)


def remove_stopwords(text, language='english'):
    """

    :param text:
    :param language:
    :return:
    """
    stop_words = set(stopwords.words(language))
    word_tokens = word_tokenize(text)
    return ' '.join([w for w in word_tokens if not w in stop_words])


def insert_tag(tag_name='', source='', language='english'):
    """Inserts tag into database.

    :param tag_name:
    :param source:
    :param language:
    :return:
    """
    try:
        if tag_name:
            if settings.remove_stop_words:
                tag_name = remove_stopwords(tag_name, language)
            # Insert into database.
            db = Db.Db()
            db.initialize(dsn=settings.SQLALCHEMY_DSN)
            sql_query = "INSERT INTO tags (tag_name) VALUES ('%s')" % tag_name
            return db.insert_content(sql_query, 'tag_id')
    except psycopg2.DataError as exception:
        log.exception(exception)
    except psycopg2.ProgrammingError as exception:
        log.exception(exception)


def insert_person(person_name=''):
    """

    :param person_name:
    :return:
    """
    try:
        if person_name:
            sql_query = 'INSERT INTO persons (name, mention_date)'
            content = "'" + person_name.replace("'", "''") + "'," + DB_NOW
            db = Db.Db()
            db.initialize(dsn=settings.SQLALCHEMY_DSN)
            return db.insert(sql_query, content, None)
    except psycopg2.ProgrammingError as exception:
        log.exception(exception)


def insert_company(company_name=''):
    """

    :param company_name:
    :return:
    """

    try:
        if company_name:
            sql_query = 'INSERT INTO companies (name, mention_date)'
            content = "'" + company_name.replace("'", "''") + "'," + DB_NOW
            db = Db.Db()
            db.initialize(dsn=settings.SQLALCHEMY_DSN)
            return db.insert(sql_query, content, None)
    except psycopg2.ProgrammingError as exception:
        log.exception(exception)


def associate_tag_news(news_id, tag_id):
    """

    :param post_id:
    :param tag_id:
    :return:
    """

    try:
        if news_id and tag_id:
            sql_query = 'INSERT INTO tags_news (tag_id, news_id)'
            content = str(tag_id) + "," + str(news_id)
            db = Db.Db()
            db.initialize(dsn=settings.SQLALCHEMY_DSN)
            return db.insert(sql_query, content, None)
    except psycopg2.ProgrammingError as exception:
        log.exception(exception)


def update_ranked_post(news_id, rank_score, rank_order):
    """

    :param news_id:
    :param rank_score:
    :param rank_order:
    :return:
    """

    sql_query = 'UPDATE news SET rank_score = %s, rank_order = %s WHERE ' \
                'news_id = %d' % (rank_score, rank_order, news_id)
    try:
        db = Db.Db()
        db.initialize(dsn=settings.SQLALCHEMY_DSN)
        return db.update(sql_query)
    except psycopg2.ProgrammingError as exception:
        log.exception(exception)


def insert_cluster_article(news_id=-1, title=None, content='', source='',
                           url='',
                           cluster=-1, campaign_reference='', **kwargs):
    """
    :param news_id:
    :param title:
    :param content:
    :param source:
    :param url:
    :param cluster:
    :param campaign_reference:
    :param kwargs:
    :return:
    """
    try:
        if title and url:
            sql_query = "INSERT INTO clustering_news (news_id, inserted_at, " \
                        "title, content, url, source, cluster, " \
                        "campaign_reference) " \
                        "VALUES (%d,'%s','%s','%s','%s','%s', %d,'%s') " \
                        % (news_id,
                           DB_NOW,
                           title.replace("'", "''"),
                           content[:settings.content_size].replace("'", "''"),
                           url,
                           source,
                           cluster,
                           campaign_reference)
            db = Db.Db()
            db.initialize(dsn=settings.SQLALCHEMY_DSN)
            return db.insert_content(sql_query, 'id')
    except psycopg2.ProgrammingError as exception:
        log.exception(exception)


def get_multiple_records(sqlquery):
    """

    :param sqlquery:
    :return:
    """
    try:
        db = Db.Db()
        db.initialize(dsn=settings.SQLALCHEMY_DSN)
        return db.query_multiple(sqlquery)
    except psycopg2.ProgrammingError as exception:
        log.exception(exception)


def get_record(sqlquery):
    """Gets a single Record (LIMIT 1)

    :param sqlquery:
    :return:
    """
    try:
        db = Db.Db()
        db.initialize(dsn=settings.SQLALCHEMY_DSN)
        return db.query(sqlquery)
    except psycopg2.ProgrammingError as exception:
        log.exception(exception)


def update_database(sqlquery):
    """

    :param sqlquery:
    :return:
    """
    try:
        db = Db.Db()
        db.initialize(dsn=settings.SQLALCHEMY_DSN)
        db.update(sqlquery)
    except psycopg2.ProgrammingError as exception:
        log.exception(exception)


def test_connection():
    """

    :return:
    """
    try:
        sql_query = 'SELECT COUNT(*) FROM news;'
        db = Db.Db()
        db.initialize(dsn=settings.SQLALCHEMY_DSN)
        return db.query(sql_query)
    except psycopg2.ProgrammingError as exception:
        log.exception(exception)
