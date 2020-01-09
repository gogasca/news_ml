"""Database operations"""

from .Model import ApiUsers
from .Model import Campaign
from .Model import db as db
from .Model import News
from .Model import Person

import logging
import re

from api.version1_0.database import DbHelper
from conf import settings

log = logging.getLogger()
log.setLevel(level=logging.DEBUG)

DATE_FILTER_PATTERN = re.compile(
    r'\d{4}-((1[0-2]|[1-9])|0[1-9])-((3[01]|[12][0-9]|[1-9])|0[1-9])')


def validate_date(date_value):
    """

    :param date_value:
    :return:
    """
    if not (DATE_FILTER_PATTERN.match(date_value) or
            date_value == settings.DATE_LATEST):
        log.error('Invalid date value parameter: %r', date_value)
        return False
    return True


def news_filter(request):
    """Filter news based on source parameters:
     -date
     -source

    By date parameters: (YYYY-MM-DD), otherwise use latest. (
    settings.DATE_LATEST (u'latest'))
        http://0.0.0.0:8081/api/1.0/news?date=2018-10-09

    By source:
        http://0.0.0.0:8081/api/1.0/news?source=AMAZON.COM

    :param request:
    :return:(Model.News) List of news.
    """
    log.info('/news Request: %s', request)
    date_value = request.args.get('date')
    source_value = request.args.get('source')
    # Check Date value and source value.
    queryset = News.query.order_by(News.published_at.desc(), News.source)
    if date_value:
        logging.info('News date: %s', date_value)
        date_value = date_value.lower()
        if not validate_date(date_value):
            return None
        if settings.DATE_LATEST != date_value:
            queryset = queryset.filter(News.published_at == date_value)
    if source_value:
        logging.info('News source: %s', source_value)
        source_value = source_value.upper()

    # Process arguments.
    if source_value:
        return queryset.filter(News.source == source_value).limit(
            settings.MAX_NEWS).all()
    if date_value:
        return queryset.limit(settings.MAX_NEWS).all()


def insert_user(username, password, created):
    """

    :param username:
    :param password:
    :param created:
    :return:
    """
    try:
        if username and password:
            user = ApiUsers(username, password, created)
            db.session.add(user)
            db.session.commit()
            return user.id
    except Exception as exception:
        log.exception(exception)
        db.session.rollback()
    finally:
        db.session.close()


def insert_campaign(status, description, reference, start, request_data,
                    campaign_type, send_report, articles, test):
    """

    :param status:
    :param description:
    :param reference:
    :param start:
    :param request_data:
    :param campaign_type:
    :param send_report:
    :param articles:
    :param test:
    :return:
    """
    try:
        campaign = Campaign(status, description, reference, start,
                            request_data, campaign_type, send_report,
                            articles, test)
        db.session.add(campaign)
        db.session.commit()
        return campaign.id
    except Exception as exception:
        log.exception(exception)
        db.session.rollback()
    finally:
        db.session.close()


def insert_person(name, mention_date):
    """

    :param name:
    :param mention_date:
    :return:
    """
    try:
        if name:
            person = Person(name, mention_date)
            db.session.add(person)
            db.session.commit()
            return person.id
    except Exception as exception:
        log.exception(exception)
        db.session.rollback()
    finally:
        db.session.close()


def user_list(limit=10):
    """

    :param limit:
    :return:
    """

    if limit < 1:
        limit = 10
    sqlquery = """SELECT id, username, created FROM api_users GROUP BY id,
    username, created ORDER BY created DESC LIMIT %s;""" % str(
        limit)
    return DbHelper.get_multiple_records(sqlquery)


def person_list(limit=10):
    """

    :param limit:
    :return:
    """

    if limit < 1:
        limit = 10
    sqlquery = """SELECT COUNT(id) AS mentions,name FROM persons WHERE
    valid=True GROUP BY name ORDER BY mentions DESC LIMIT %s;""" % str(
        limit)
    return DbHelper.get_multiple_records(sqlquery)


def person_filter(request):
    """

    :param request:
    :return:
    """
    persons = None
    name_value = request.args.get('name')

    if name_value and len(name_value) > 1:
        name_value = name_value.replace("'", "''")
        sqlquery = """SELECT COUNT(id) AS mentions,name FROM persons WHERE
        name='%s' AND valid=True GROUP BY name ORDER BY mentions DESC;""" % \
                   name_value
        persons = DbHelper.get_multiple_records(sqlquery)
    return persons


def person_top(request):
    """

    :param request:
    :return:
    """
    sqlquery = """SELECT COUNT(id) AS mentions,name FROM persons GROUP BY
    name ORDER BY mentions DESC;"""
    return DbHelper.get_multiple_records(sqlquery)
