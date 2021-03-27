"""Helper function for DB operations."""

import logging
import psycopg2
import psycopg2.extensions

from api.version1_0.database import Db
from conf import settings

if settings.REMOVE_STOP_WORDS:
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
log = logging.getLogger()
log.setLevel(level=logging.DEBUG)

DB_NOW = 'now()'


def _get_db():
    db = Db.Db()
    db.initialize(dsn=settings.SQLALCHEMY_DSN)
    return db


def test_connection():
    """

    :return:
    """
    try:
        db = _get_db()
        sql_query = 'SELECT COUNT(*) FROM news;'
        return db.query(sql_query)
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


def record_exists(url, table='news'):
    """

    :param url:
    :param table:
    :return: boolean
    """
    try:
        if url:
            db = _get_db()
            sql_query = """SELECT url FROM %s WHERE url='%s'""" % (
                table, url.strip())
            result = db.query(sql_query)
            if result:
                return True
            return False
    except psycopg2.ProgrammingError as exception:
        log.exception(exception)


def insert_news(title=None, author='', description='', content='', url='',
                url_to_image='', source_id='', source='', campaign='',
                published_at='NULL', score=0, magnitude=0, sentiment='',
                **kwargs):
    """
    Techmeme do not provide published at information
    the best we can do is leave the field NULL or add the day which we read that
    info. We already have inserted_at which provides this.

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
    :param score:
    :param magnitude:
    :param sentiment:
    :param kwargs:
    :return:
    """
    try:
        if not (title and url):
            raise ValueError('Title or url missing')
        db = _get_db()
        sql_query = \
            "INSERT INTO news (" \
            "title, author, description, content, url, url_to_image, " \
            "source_id, source, campaign, published_at, score, magnitude, " \
            "sentiment, inserted_at ) " \
            "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', " \
            "{}, {}, {}, '{}', '{}')".format(
                title.replace("'", "''"),
                author.replace("'", "''"),
                description.replace("'", "''"),
                content[:settings.CONTENT_SIZE].replace("'", "''"),
                url,
                url_to_image,
                source_id,
                source,
                campaign,
                ''.join(('\'', published_at,
                         '\'')) if published_at and published_at != 'NULL'
                else published_at,
                score,
                magnitude,
                sentiment,
                DB_NOW)
        return db.insert_content(sql_query, 'news_id')
    except psycopg2.ProgrammingError as exception:
        log.exception(exception)


def insert_tag(tag_name='', language='english'):
    """Inserts tag into database.

    :param tag_name:
    :param source:
    :param language:
    :return:
    """
    try:
        if tag_name != '' and len(tag_name) > 1:
            if settings.REMOVE_STOP_WORDS:
                tag_name = remove_stopwords(tag_name, language)
            # Insert into database.
            db = _get_db()
            sql_query = "INSERT INTO tags (tag_name) VALUES ('%s')" % tag_name
            return db.insert_content(sql_query, 'tag_id')
    except (psycopg2.DataError, psycopg2.ProgrammingError) as exception:
        log.exception(exception)


def insert_person(person_name=''):
    """

    :param person_name:
    :return:
    """
    try:
        if person_name and len(person_name) > 1:
            db = _get_db()
            sql_query = 'INSERT INTO persons (name, mention_date)'
            content = "'" + person_name.replace("'", "''") + "'," + DB_NOW
            return db.insert(sql_query, content, None)
    except psycopg2.ProgrammingError as exception:
        log.exception(exception)


def insert_company(company_name=''):
    """

    :param company_name:
    :return:
    """

    try:
        if company_name and len(company_name) > 1:
            db = _get_db()
            sql_query = 'INSERT INTO companies (name, mention_date)'
            content = "'{}',{}".format(company_name.replace("'", "''"), DB_NOW)
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
            db = _get_db()
            sql_query = 'INSERT INTO tags_news (tag_id, news_id)'
            content = '{},{}'.format(tag_id, news_id)
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
        db = _get_db()
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
                           content[:settings.CONTENT_SIZE].replace("'", "''"),
                           url,
                           source,
                           cluster,
                           campaign_reference)
            db = _get_db()
            return db.insert_content(sql_query, 'id')
    except psycopg2.ProgrammingError as exception:
        log.exception(exception)


def get_multiple_records(sqlquery):
    """

    :param sqlquery:
    :return:
    """
    try:
        db = _get_db()
        return db.query_multiple(sqlquery)
    except psycopg2.ProgrammingError as exception:
        log.exception(exception)


def get_record(sqlquery):
    """Gets a single Record (LIMIT 1)

    :param sqlquery:
    :return:
    """
    try:
        db = _get_db()
        return db.query(sqlquery)
    except psycopg2.ProgrammingError as exception:
        log.exception(exception)


def update_database(sqlquery):
    """

    :param sqlquery:
    :return:
    """
    try:
        db = _get_db()
        db.update(sqlquery)
    except psycopg2.ProgrammingError as exception:
        log.exception(exception)
