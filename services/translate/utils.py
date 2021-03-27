"""Perform translation."""

import logging

from api.version1_0.database import DbHelper
from conf import settings
from services.translate import translate

log = logging.getLogger()

_TRANSLATED_TEXT = 'translatedText'
_LANGUAGE = 'language'


def update_db_query(translation, detected_language, news_id):
    """

    :param translation:
    :param detected_language:
    :param news_id:
    :return:
    """
    if translation and detected_language and news_id:
        return u"UPDATE news SET translated_content='%s', detected_language='%s' " \
               u"WHERE news_id=%s;" % (
                   translation, detected_language, str(news_id))
    return


def translate_content(text, language=settings.TRANSLATION_DEFAULT_LANGUAGE):
    """

    :param post_id:
    :param text:
    :param language:
    :return:
    """
    if not text:
        raise ValueError('Invalid text')
    if not settings.TRANSLATION_SERVICE:
        log.info(
            'Translation service is disabled in settings.translation_service')
        return settings.EMPTY_TEXT
    # Limited text (Limit requests to settings.TRANSLATION_LIMIT)
    limited_text = text[:settings.TRANSLATION_LIMIT]

    detected_language = translate.detect_language(limited_text)
    # Submit translation request.
    if detected_language.get('language') != language:
        logging.info(
            'Translating from {} to {}'.format(
                detected_language.get('language'), language))
        translated_text = translate.translate_text(language, limited_text)
        if translated_text.get('translatedText'):
            return translated_text.get('translatedText')
    else:
        log.warning(
            'No text to translate. Source language (%s) eq target language ('
            '%s)' % (detected_language.get('language'), language))
        return text


def translate_article(campaign_instance, article, new_article, news_id):
    """

    :param campaign_instance:
    :param article:
    :param new_article:
    :param report:
    :param news_id:
    :return:
    """
    # Perform translation using Google Translate API
    log.info('Translating...%r', article.url)
    translated_text = translate_content(
        article.title, campaign_instance.translation_lang)
    if new_article and translated_text:
        # Update database record
        sql_query = update_db_query(
            translated_text.replace("'", "''"), settings.DEFAULT_LANGUAGE, news_id)
        DbHelper.update_database(sql_query)
    else:
        log.warning('Article already exists, skipping DB update')
    return translated_text
