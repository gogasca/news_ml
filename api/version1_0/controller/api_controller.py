"""Handles instances."""

from main import CampaignD
from main import TextD
from main import PersonD
from functools import wraps
from services.clustering.k_means import ClusterD
from services.ranking import RankerD
from conf import settings
from conf import constants
from flask import (
    request,
    abort
)

from error import errors
from utils.validate import validator


def validate_json(f):
    """
    # Validate Request comes in valid JSON form
    :param f:
    :return:
    """

    @wraps(f)
    def wrapper(*args, **kw):
        try:
            request.json
        except Exception:
            msg = 'Invalid JSON Request. Use Content-Type: application/json'
            abort(400, description=msg)
        return f(*args, **kw)

    return wrapper


def validate_schema(schema_name):
    """

    :param schema_name:
    :return:
    :raise: Exception
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            try:
                if schema_name == 'campaign':
                    # Validate POST for new campaign
                    validator.check_campaign(json_request=request.json)
                if schema_name == 'person':
                    # Validate POST for new person
                    validator.check_person(json_request=request.json)
            except Exception as exception:
                print(exception)
                msg = 'Request must be a valid JSON for %s' % schema_name
                abort(400, description=msg)
            return f(*args, **kw)

        return wrapper

    return decorator


def get_campaign(json_request):
    """

    :param json_request:
    :return:
    :raise: ValueError
    """

    if not json_request:
        raise ValueError(errors.INVALID_CAMPAIGN)

    campaign_instance = CampaignD.CampaignD()
    provider = json_request.get('provider')
    query = json_request.get('query')
    report = json_request.get('report')
    translate = json_request.get('translate')
    if provider:
        campaign_instance.provider = json_request['provider'].upper()
    if query:
        campaign_instance.query = json_request['query']
    if report:
        campaign_instance.send_report = True
        email = json_request.get('report').get('email')
        if email:
            campaign_instance.email_recipients = \
                json_request['report']['email'].split(settings._EMAIL_SEPARATOR)
    if translate:
        campaign_instance.translation_enable = True
        campaign_instance.translation_lang = json_request.get('translate').get(
            'language')
    else:
        campaign_instance.translation_enable = False
    return campaign_instance


def get_clustering(json_request):
    """

    :param json_request:
    :return:
    :raise: ValueError
    """

    if not json_request:
        raise ValueError(errors.INVALID_CAMPAIGN)

    clustering_instance = ClusterD.Clustering(settings.num_of_clusters)
    clustering_instance.provider = settings.clustering_provider.upper()

    if settings.api_num_of_clusters in json_request:
        num_of_clusters = json_request[settings.api_num_of_clusters]
        if isinstance(num_of_clusters, int) and (num_of_clusters > 1):
            clustering_instance.num_of_clusters = num_of_clusters
        else:
            raise ValueError(errors.INVALID_NUM_CLUSTERS)

    if constants.REPORT in json_request:
        clustering_instance.send_report = True
        if constants.EMAIL in json_request[constants.REPORT]:
            clustering_instance.email_recipients = \
            json_request[constants.REPORT][constants.EMAIL].split(
                settings.EMAIL_SEPARATOR)
    return clustering_instance


def get_ranker(json_request):
    """
    Gets Rank information from JSON Request.
        -provider
        -report

    :param json_request:
    :return:
    :raise: ValueError
    """

    if not json_request:
        raise ValueError(errors.INVALID_CAMPAIGN)

    # Create a Ranker instance which will process news.
    ranker_instance = RankerD.RankerD()
    if constants.PROVIDER in json_request:
        ranker_instance.provider = json_request[constants.PROVIDER].upper()
    if constants.REPORT in json_request:
        ranker_instance.send_report = True
        if constants.EMAIL in json_request[constants.REPORT]:
            ranker_instance.email_recipients = json_request[constants.REPORT][constants.EMAIL].split(
                settings.EMAIL_SEPARATOR)
    return ranker_instance


def get_text(json_request):
    """
    Extracts field information from JSON Request.
    The field is: 'text' which contains the text to analyze.

    curl -u AC64861838b417b555d1c8868705e4453f
    :YYPKpbIAYqz90oMN8A11YYPKpbIAYqz90o
        -H "Content-Type: application/json"
        -X POST -d '{ "text": "I love my life" }'
        http://0.0.0.0:8081/api/1.0/sentiment -v

    :param json_request:
    :return: The text to analyze
    """

    if not json_request:
        raise ValueError(errors.INVALID_REQUEST)

    text_instance = TextD.TextD()
    # Verify text parameter exist.
    text_in_request = json_request.get(constants.TEXT)
    if text_in_request:
        text_instance.run_sentiment_analysis = True  # TODO(gogasca) Add FLAG
        #  in API: sentiment_analysis=True
        text_instance.content = text_in_request

    return text_instance


def get_person(json_request):
    """

    :param json_request:
    :return:
    :raise: ValueError
    """

    if not json_request:
        raise ValueError(errors.INVALID_PERSON)

    person_instance = PersonD.PersonD()
    if constants._NAME in json_request:
        person_instance.name = json_request[constants._NAME]
    return person_instance
