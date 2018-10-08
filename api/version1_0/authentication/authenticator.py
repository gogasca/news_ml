"""Handles Authentication.

Handles authentication for API requests.
These file supports the following:
 - Basic authentication using local username and password.
 - Basic authentication using database username and password
 - Token based authentication.
"""

from conf import settings
from functools import wraps

from api.version1_0.database import Model

from flask import jsonify
from flask import request
from flask import g


def _check_local(username, password):
    """ Basic authentication: local username and password.

    :param username:
    :param password:
    :return:
    """
    return username == settings.api_account and password == \
                                                settings.api_password


def _check_db(username_or_token, password):
    """Authenticate user authentication token method in DB.

    First try to authenticate by token.
    Second authenticate in DB with password.

    :param username_or_token:
    :param password:
    :return: boolean
    """
    user = Model.ApiUsers.verify_auth_token(username_or_token)
    if not user:
        # Authenticate with database password.
        user = Model.ApiUsers.query.filter_by(
            username=username_or_token).first()
        # Lookup password in database.
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


def _authentication_error():
    """
    Authentication error.
    :return:
    """

    response = jsonify({'message': "Authenticate."})
    response.headers['WWW-Authenticate'] = settings.api_realm
    response.status_code = 401
    return response


def local_authentication(f):
    """Decorator to check local authentication.

    :param f: A function
    :return: itself: Decorator check_credentials
    """

    @wraps(f)
    def check_credentials(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return _authentication_error()

        elif not _check_local(auth.username, auth.password):
            return _authentication_error()
        return f(*args, **kwargs)

    return check_credentials


def db_authentication(f):
    """Decorator to check database authentication.
    :param f: A function
    :return: itself: Decorator check_credentials
    """

    @wraps(f)
    def check_credentials(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return _authentication_error()

        elif not _check_db(auth.username, auth.password):
            return _authentication_error()
        return f(*args, **kwargs)

    return check_credentials
