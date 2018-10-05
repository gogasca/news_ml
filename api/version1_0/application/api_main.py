"""Initializes API classes and methods."""

import flask_restful
import json
import logging

from celery import Celery
from conf import logger
from conf import settings

from api.version1_0.authentication import authenticator
from api.version1_0.controller import api_controller
from api.version1_0.database import Model
from api.version1_0.database import ModelOperations

from error import errors
from flask import current_app
from flask import g
from flask import jsonify
from flask import request
from flask import Response
from flask_restful import Resource

# =========================================================
# API Controller
# =========================================================

api = flask_restful.Api
log = logger.LoggerManager().getLogger('__app__',
                                       logging_file=settings.api_logfile)
log.setLevel(level=logging.DEBUG)


class ApiBase(Resource):
    @authenticator.local_authentication
    def get(self):
        """Checks if API is currently active and returns API latest version.

        :return:
        """
        try:
            log.info('%s %r' % (request.remote_addr, request))
            if request.headers['Content-Type'] == settings.api_mime_type:
                log.info('api() | GET | Version %s' % settings.api_version)
                response = json.dumps('Version: %s' % settings.api_version)
                return Response(response, status=200,
                                mimetype=settings.api_mime_type)
        except KeyError as key_error:
            logging.exception(key_error)
            response = json.dumps(
                'Invalid type headers. Use %s' % settings.api_mime_type)
            return Response(response, status=415,
                            mimetype=settings.api_mime_type)
        except Exception as exception:
            log.exception(exception)
            return Response(json.dumps(errors.API_ERROR), status=500,
                            mimetype=settings.api_mime_type)


class ApiUser(Resource):
    """Finds a specific username by id."""
    def get(self, id):
        """Get User information from database.

        :param id:
        :return:
        """
        try:
            log.info('%s %r' % (request.remote_addr, request))
            log.info('api() | Finding user: %s' % id)
            user = Model.ApiUsers.query.filter(Model.ApiUsers.id == id).first()
            if user:
                log.info('api() | User %s found.' % id)
                return jsonify(user.serialize())
            log.warn('api() | User %s not found. ' % id)
            return Response(json.dumps(errors.USER_NOT_FOUND), status=404,
                            mimetype=settings.api_mime_type)

        except Exception as e:
            log.exception(e)
            return Response(json.dumps(errors.API_ERROR), status=500,
                            mimetype=settings.api_mime_type)


class ApiUserList(Resource):
    """Handles API users"""

    def get(self):
        """Get List of users.

        :return:
        """
        try:
            log.info('%s %r' % (request.remote_addr, request))
            users = ModelOperations.user_list()
            if not users:
                response = jsonify(users=[])
                response.status_code = 404
                return response
            response = [{"id": user[0], "username": user[1], "created": user[2]}
                        for user in users]
            return jsonify(users=response)
        except KeyError as key_error:
            log.exception(key_error)

    @api_controller.validate_json
    def post(self):
        """Creates a new user.

        New user requires a valid username and password. Password is clear text.
        API uses HTTPS hence password should be unreadable if intercepted.
        :return:
        """
        try:
            log.info('%s %r' % (request.remote_addr, request))
            # Get authentication parameters.
            username = request.json.get('username')
            password = request.json.get('password')
            if username is None or password is None:
                log.error('api() | Provide username and password.')
                response = json.dumps('Provide username and password')
                return Response(response, status=400,
                                mimetype=settings.api_mime_type)
            if Model.ApiUsers.query.filter_by(
                    username=username).first() is not None:
                log.error('api() | Username already exists.')
                response = json.dumps('Username already exists')
                return Response(response, status=400,
                                mimetype=settings.api_mime_type)
            # Insert user into Postgres database.
            user_id = ModelOperations.insert_user(username, password, 'now()')
            response = jsonify({'id': user_id})
            response.headers['Location'] = api.url_for(api(current_app),
                                                       ApiUser,
                                                       id=user_id,
                                                       _external=True,
                                                       _scheme=settings.api_scheme)
            response.status_code = 201
            return response
        except Exception as exception:
            log.exception(exception)
            response = json.dumps(errors.API_ERROR)
            return Response(response, status=500,
                            mimetype=settings.api_mime_type)


class Campaign(Resource):
    @authenticator.local_authentication
    def get(self, ref):
        """

        :param ref:
        :return:
        """
        try:
            log.info('%s %r' % (request.remote_addr, request))
            log.info('api() | Finding Campaign: ' + ref)
            campaign = Model.Campaign.query.filter(
                Model.Campaign.reference == ref).first()
            if campaign:
                log.info('api() | Campaign found: ' + ref)
                return jsonify(campaign.serialize())

            log.warn('api() | Campaign not found: ' + ref)
            return Response(status=404, mimetype=settings.api_mime_type)
        except Exception as exception:
            log.exception(exception)
            return Response(json.dumps(errors.API_ERROR), status=500,
                            mimetype=settings.api_mime_type)


class CampaignList(Resource):
    @authenticator.local_authentication
    def get(self):
        """

        :return:
        """
        try:
            log.info('%s %r' % (request.remote_addr,
                                request))  # TODO(gogasca) List of campaigns.
        except Exception as exception:
            log.exception(exception)

    @api_controller.validate_json
    @api_controller.validate_schema('campaign')
    @authenticator.local_authentication
    def post(self):
        """

        :return:
        """
        try:
            log.info('%s %r' % (request.remote_addr, request))
            log.info('api() | POST | Received request for Campaign')
            campaign_instance = api_controller.get_campaign(
                request.json) or None
            # Returns valid CampaignD object.
            if not campaign_instance:
                log.error('api() | Unable to process Campaign request %r',
                          request.data)
                response = json.dumps(errors.INVALID_CAMPAIGN)
                return Response(response, status=422,
                                mimetype=settings.api_mime_type)
            celery = Celery()
            celery.config_from_object("conf.celeryconfig")
            celery.send_task('process_campaign',
                             exchange='news_ml',
                             queue='gold',
                             routing_key='news_ml.gold',
                             kwargs={'campaign_instance': campaign_instance},
                             retries=3)
            response = jsonify({'campaign_id': campaign_instance.reference})
            response.headers['Location'] = api.url_for(api(current_app),
                                                       Campaign,
                                                       ref=campaign_instance.reference,
                                                       _external=True,
                                                       _scheme=settings.api_scheme)
            response.status_code = 202
            return response

        except Exception as exception:
            log.exception(exception)
            return Response(json.dumps(errors.API_ERROR), status=500,
                            mimetype=settings.api_mime_type)

        finally:
            # Insert campaign details into database.
            if campaign_instance:
                campaign_instance.id = ModelOperations.insert_campaign(0,
                                                                       'Campaign %s' % campaign_instance.reference,
                                                                       campaign_instance.reference,
                                                                       settings.dbnow,
                                                                       request.data,
                                                                       campaign_instance.provider,
                                                                       campaign_instance.send_report,
                                                                       campaign_instance.num_of_articles,
                                                                       False)


class GetToken(Resource):
    """Generates Token for authentication."""

    @authenticator.db_authentication
    def get(self):
        """Returns a Token.

        :return:
        """

        # TODO(gonzalo): The problem here is if almost expired token is
        # stolen you can get a new token with the old one.
        # Consider accepting only username and password to get a new token.

        duration = settings.token_expiration_secs
        token = g.user.generate_auth_token(duration)
        return jsonify({
            'token': token.decode('ascii'),
            'duration': duration,
            'message': 'After Duration: %s secs, request for a new token.' %
                       duration
        })


class Person(Resource):
    @authenticator.local_authentication
    def get(self, person_id):
        """

        :param person_id:
        :return:
        """
        try:
            log.info('%s %r' % (request.remote_addr, request))
            log.info('api() | Finding Person: ' + person_id)
            person = Model.Person.query.filter(
                Model.Person.id == person_id).first()
            if person:
                log.info('api() | Person found: ' + person_id)
                return jsonify(person.serialize())
            log.warn('api() | Person not found: ' + person_id)
            return Response(status=404, mimetype=settings.api_mime_type)
        except Exception as exception:
            log.exception(exception)
            return Response(json.dumps(errors.API_ERROR), status=500,
                            mimetype=settings.api_mime_type)


class PersonList(Resource):
    """Gets lists of persons."""

    @authenticator.local_authentication
    def get(self):
        """

        :return:
        """
        try:
            log.info('%s %r' % (request.remote_addr, request))
            response = []
            if len(request.args) > 0:
                persons = ModelOperations.person_filter(request)
            else:
                persons = ModelOperations.person_list()
                if not persons:
                    return jsonify(persons=response)
            response = [{"mentions": int(person[0]), "name": person[1]} for
                        person in persons]
            return jsonify(persons=response)

        except Exception as exception:
            log.exception(exception)
            return Response(json.dumps(errors.API_ERROR), status=500,
                            mimetype=settings.api_mime_type)

    @api_controller.validate_json
    @api_controller.validate_schema('person')
    @authenticator.local_authentication
    def post(self):
        """

        :return:
        """
        try:
            log.info('%s %r' % (request.remote_addr, request))
            log.info('api() | POST | Received request for Person')
            # Assign API request information
            person_instance = api_controller.get_person(request.json)
            # Returns valid CampaignD object
            if not person_instance:
                log.error('api() | Unable to process Person request %r',
                          request.data)
                response = json.dumps(errors.INVALID_PERSON)
                resp = Response(response, status=422,
                                mimetype=settings.api_mime_type)
                return resp
            person_instance.id = ModelOperations.insert_person(
                person_instance.name, settings.dbnow)
            response = jsonify({'person_id': person_instance.id})
            response.headers['Location'] = api.url_for(api(current_app),
                                                       Person,
                                                       ref=person_instance.id,
                                                       _external=True,
                                                       _scheme=settings.api_scheme)
            response.status_code = 202
            return response
        except Exception as exception:
            log.exception(exception)
            return Response(json.dumps(errors.API_ERROR), status=500,
                            mimetype=settings.api_mime_type)


class NewsList(Resource):
    """Gets lists of news."""

    @authenticator.local_authentication
    def get(self):
        """

        :return:
        """
        try:
            log.info('%s %r' % (request.remote_addr, request))
            if len(request.args) > 0:
                news_list = ModelOperations.news_filter(request)
            else:
                news_list = Model.News.query.order_by(
                    Model.News.published_at.desc()).limit(
                    settings.max_news).all()
            if news_list:
                log.info('api() | %d News found ' % len(news_list))
                # Extract fields:
                # ['title', 'content', 'url', 'published_at', 'provider']
                response = [{field: getattr(news, field) for field in
                             settings.NEWS_FIELDS} for news in news_list]
                return jsonify(news=response, status='ok', source='gonzo')
            log.warn('api() | No News found')
            return Response(json.dumps(errors.NO_NEWS), status=404,
                            mimetype=settings.api_mime_type)

        except UnboundLocalError as exception:
            log.exception(exception)
            response = json.dumps(errors.INVALID_REQUEST)
            return Response(response, status=400,
                            mimetype=settings.api_mime_type)


class Status(Resource):
    """Verifies API status."""

    @authenticator.db_authentication
    def get(self):
        """

        :return:
        """
        try:
            log.info('%s %r' % (request.remote_addr, request))
            log.info('api() | GET | Received request for Status')
            response = json.dumps('Status: GET. Hola %s!' % g.user.username)
            return Response(response, status=200,
                            mimetype=settings.api_mime_type)
        except (TypeError, ValueError) as e:
            log.exception(e)
            return Response(json.dumps(errors.API_ERROR), status=500,
                            mimetype=settings.api_mime_type)

    @authenticator.local_authentication
    def post(self):
        try:
            log.info('%s %r' % (request.remote_addr, request))
            log.info('api() | POST | Received request for Status')
            response = json.dumps('Status: POST. %s' % settings.api_ok)
            return Response(response, status=202,
                            mimetype=settings.api_mime_type)
        except (TypeError, ValueError) as exception:
            log.exception(exception)
            return Response(json.dumps(errors.API_ERROR), status=500,
                            mimetype=settings.api_mime_type)

    @authenticator.local_authentication
    def delete(self):
        try:
            log.info('%s %r' % (request.remote_addr, request))
            log.info('api() | DELETE | Received request for Status')
            response = json.dumps('Status: DELETE. %s' % settings.api_ok)
            return Response(response, status=202,
                            mimetype=settings.api_mime_type)
        except (TypeError, ValueError) as exception:
            log.exception(exception)
            return Response(json.dumps(errors.API_ERROR), status=500,
                            mimetype=settings.api_mime_type)

    @authenticator.local_authentication
    def put(self):
        try:
            log.info('%s %r' % (request.remote_addr, request))
            log.info('api() | PUT | Received request for Status')
            response = json.dumps('Status: PUT. %s' % settings.api_ok)
            return Response(response, status=202,
                            mimetype=settings.api_mime_type)
        except (TypeError, ValueError) as exception:
            log.exception(exception)
            return Response(json.dumps(errors.API_ERROR), status=500,
                            mimetype=settings.api_mime_type)
