"""Validation library."""

from conf import settings
from functools import wraps
from validate_email import validate_email

EMAIL = 'email'
LANG = 'language'
NAME = u'name'
PROVIDER = 'provider'
REPORT = 'report'
TRANSLATE = 'translate'
LIMIT = 'limit'


def required(**mandatory):
    """

    :param mandatory:
    :return:
    """

    def decorator(f):
        @wraps(f)
        def wrapper(**dicts):
            for argname, d in dicts.items():
                for key in mandatory.get(argname, []):
                    if key not in d:
                        raise Exception(
                            'Key "%s" is missing from argument "%s"' % (
                                key, argname))
            return f(**dicts)
        return wrapper
    return decorator


@required(json_request=(PROVIDER,))
def check_campaign(json_request=None):
    """

    :param json_request:
    :return:
    """

    if check_provider(json_request):
        if REPORT in json_request and TRANSLATE in json_request:
            return check_translation(json_request) & check_report(json_request)
        if REPORT in json_request:
            return check_report(json_request)
        if TRANSLATE in json_request:
            return check_translation(json_request)
        if LIMIT in json_request:
            return check_limit(json_request)
        return True
    return False


@required(json_request=(NAME,))
def check_person(json_request=None):
    """

    :param json_request:
    :return:
    """
    return True


def check_provider(provider_request):
    """

    :param provider_request:
    :return: bool
    """
    if (provider_request[PROVIDER]).upper() in settings.VALID_PROVIDERS:
        return True
    return False


def check_email_addresses(recipients, check_mx=settings.EMAIL_CHECK_MX,
                          verify=settings.EMAIL_VERIFY):
    """
    Example: "report": {"email": "email@d.com"}}

    :param recipients:
    :param check_mx:
    :param verify:
    :return:
    """
    valid_addresses = []
    if recipients:
        email_addresses = filter(None,
                                 recipients.split(settings.EMAIL_SEPARATOR))
        for email in email_addresses:
            if validate_email(email, check_mx=check_mx, verify=verify):
                valid_addresses.append(email)
            else:
                print('Invalid email address: %s' % email)
    if valid_addresses:
        return True
    return False


def check_report(report_request):
    """
    {"report": {"email": "jbernal@edujam.com.mx"}}
    :param report_request:
    :return: bool
    """
    if report_request[REPORT]:
        if EMAIL in report_request[REPORT]:
            if check_email_addresses(report_request[REPORT][EMAIL]):
                return True
    return False


def check_limit(limit_request):
    """
    {"limit": 10, "provider": "techmeme", "report": {"email": "email@d.com"}}

    :param limit_request:
    :return:
    """
    limit_number = limit_request.get(LIMIT)
    if limit_number:
        if isinstance(limit_number, int) and limit_number > 0:
            return True
    return False


def check_translation(translation_request):
    """

    translate: { "language": "es" } or translate: { "language": "fr" }

    :param translation_request:
    :return: bool
    """
    if translation_request.get(TRANSLATE) and LANG in translation_request.get(
        TRANSLATE):
        if translation_request.get(TRANSLATE).get(
            LANG) in settings.TRANSLATION_LANGUAGES:
            return True
    return False
