"""Perform translation."""

import logging

from api.version1_0.database import DbHelper
from conf import settings
from services.translate import translate

log = logging.getLogger()

_TRANSLATED_TEXT = 'translatedText'
_LANGUAGE = 'language'


def create_sql_query(translation, detected_language, news_id):
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
    return settings.EMPTY_TEXT


def translate_content(text, language=settings.TRANSLATION_DEFAULT_LANGUAGE):
    """

    :param post_id:
    :param text:
    :param language:
    :return:
    """
    translation = settings.EMPTY_TEXT
    if not settings.TRANSLATION_SERVICE:
        log.info(
            'Translation service is disabled in settings.translation_service')
        return settings.EMPTY_TEXT
    if not text:
        raise ValueError('Invalid text')
    # Limited text (Limit requests to settings.TRANSLATION_LIMIT)
    limited_text = text[:settings.TRANSLATION_LIMIT]
    detected_language = translate.detect_language(limited_text)
    # Submit translation request.
    if detected_language != language:
        translated_text = translate.translate_text(language, limited_text)
    else:
        log.warning(
            'No text to translate. Source language (%s) eq target language ('
            '%s)' % (detected_language, language))
        return settings.EMPTY_TEXT
    # Verify language is detected and text is translated.
    if _LANGUAGE in detected_language and _TRANSLATED_TEXT in translated_text:
        # Clean text for SQL insertion.
        translation = translated_text[_TRANSLATED_TEXT].replace("'", "''")
    return translation


def translate_article(campaign_instance, article, new_article, report, news_id):
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
    if new_article:
        # Update database record
        sql_query = create_sql_query(
            translated_text, settings.DEFAULT_LANGUAGE, news_id)
        DbHelper.update_database(sql_query)
    else:
        log.warning('Article already exists, skipping DB update')
    if campaign_instance.send_report and len(translated_text) > 1:
        log.info('Adding translated information to report.')
        report.add_content(article.url, translated_text)
    return translated_text
