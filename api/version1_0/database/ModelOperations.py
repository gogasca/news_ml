import Model
import logging
import re

from Model import db as db
from api.version1_0.database import DbHelper
from conf import logger
from conf import settings

log = logger.LoggerManager().getLogger("__app__",
                                       logging_file=settings.api_logfile)
log.setLevel(level=logging.DEBUG)

DATE_FILTER_PATTERN = re.compile(
    r'\d{4}-((1[0-2]|[1-9])|0[1-9])-((3[01]|[12][0-9]|[1-9])|0[1-9])')


def news_filter(request):
    """

    :param request:
    :return:(Model.Posts) List of posts.
    """
    log.info('/news request: %s', request)
    # Date parameters (YYYY-MM-DD) or settings.DATE_LATEST (u'latest')
    date_value = request.args.get('date')
    # Get news provider.
    provider_value = request.args.get('provider')
    provider_value = provider_value or settings.DEFAULT_PROVIDER

    # Process invalid date format.
    if date_value and not (DATE_FILTER_PATTERN.match(
            date_value) or date_value.lower() == settings.DATE_LATEST):
        log.error('Invalid date value parameter: %r', date_value)
        return None

    queryset = Model.News.query.filter(Model.News.provider == provider_value)

    if not date_value or date_value.lower() == settings.DATE_LATEST:
        queryset = queryset.order_by(Model.News.published_at.desc())
    else:
        queryset = queryset.filter(Model.News.published_at == date_value)

    return queryset.limit(settings.max_news).all()


def insert_user(username, password, created):
    """

    :param title:
    :param text:
    :param short_url:
    :param source:
    :return:
    """
    try:
        if username and password:
            user = Model.ApiUsers(username, password, created)
            db.session.add(user)
            db.session.commit()
            return user.id
    except Exception as exception:
        log.error(exception)
        db.session.rollback()
    finally:
        db.session.close()


def insert_post(title, text, short_url, source):
    """

    :param title:
    :param text:
    :param short_url:
    :param source:
    :return:
    """
    try:
        if title and text:
            news = Model.News(title, text, short_url, source)
            db.session.add(news)
            db.session.commit()
            return news.news_id
    except Exception as exception:
        log.error(exception)
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
    :param test:
    :return:
    """
    try:
        campaign = Model.Campaign(status, description, reference, start,
                                  request_data, campaign_type, send_report,
                                  articles, test)
        db.session.add(campaign)
        db.session.commit()
        return campaign.id
    except Exception as exception:
        print(exception)
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
        # title, text, short_url
        if name:
            person = Model.Person(name, mention_date)
            db.session.add(person)
            db.session.commit()
            return person.id
    except Exception as exception:
        print(exception)
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
