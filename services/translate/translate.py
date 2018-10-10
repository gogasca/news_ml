import os
import six

from conf import settings
from google.cloud import translate


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.credentials


def detect_language(text):
    """Detects the text's language.

     Text can also be a sequence of strings, in which case this method
     will return a sequence of results for each text.
    :param text:
    :return:
    """
    translate_client = translate.Client()
    result = translate_client.detect_language(text)
    print('Confidence: {}'.format(result['confidence']))
    print('Language: {}'.format(result['language']))
    return result


def list_languages():
    """Lists all available languages."""
    translate_client = translate.Client()
    results = translate_client.get_languages()
    for language in results:
        print(u'{name} ({language})'.format(**language))


def list_languages_with_target(target):
    """Lists all available languages and localizes them to the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    translate_client = translate.Client()
    results = translate_client.get_languages(target_language=target)

    for language in results:
        print(u'{name} ({language})'.format(**language))


def translate_text_with_model(target, text, model=translate.NMT):
    """Translates text into the target language.

    Make sure your project is whitelisted.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    :param target:
    :param text:
    :param model:
    :return:
    """
    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(
        text, target_language=target, model=model)
    print(u'Text: {}'.format(result['input']))
    print(u'Translation: {}'.format(result['translatedText']))
    print(u'Detected source language: {}'.format(
        result['detectedSourceLanguage']))


def translate_text(target, text):
    """
    Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    :param target:
    :param text:
    :return:
    """
    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(
        text, target_language=target)
    print(u'Text: {}'.format(result['input']))
    print(u'Translation: {}'.format(result['translatedText']))
    print(u'Detected source language: {}'.format(
        result['detectedSourceLanguage']))
    return result
