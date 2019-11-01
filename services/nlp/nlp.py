"""Analyzes text using the Google Cloud Natural Language API."""
#!/usr/bin/env python
# coding=utf-8

import logging
import os
import sys

from conf import settings
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials


logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)


def get_service():
    """
    Connects to Google Cloud NLP Service

    :return:
    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.CREDENTIALS
    credentials = GoogleCredentials.get_application_default()
    return discovery.build('language', 'v1',
                           cache_discovery=False,
                           credentials=credentials)


def get_native_encoding_type():
    """Returns the encoding type that matches Python's native strings."""

    if sys.maxunicode == 65535:
        return 'UTF16'
    else:
        return 'UTF32'


def analyze_entities(text, encoding='UTF32'):
    """

    :param text:
    :param encoding:
    :return:
    """

    if not text:
        raise ValueError('Invalid text')

    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text,
        },
        'encoding_type': encoding,
    }

    service = get_service()
    request = service.documents().analyzeEntities(body=body)
    response = request.execute()
    return response


def analyze_sentiment(text, encoding='UTF32'):
    """

    :param text:
    :param encoding:
    :return:
    """
    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text,
        },
        'encoding_type': encoding
    }

    service = get_service()
    request = service.documents().analyzeSentiment(body=body)
    response = request.execute()

    return response


def analyze_syntax(text, encoding='UTF32'):
    """

    :param text:
    :param encoding:
    :return:
    """
    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text,
        },
        'encoding_type': encoding
    }

    service = get_service()
    request = service.documents().analyzeSyntax(body=body)
    response = request.execute()

    return response
