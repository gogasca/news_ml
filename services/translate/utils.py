"""Perform translation."""

from conf import settings
from services.translate import translate

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


def translate_content(text, language=settings.translation_default_language):
    """

    :param post_id:
    :param text:
    :param language:
    :return:
    """
    translation = settings.EMPTY_TEXT
    if not settings.translation_service:
        print 'Translation service is disabled in settings.translation_service'
        return settings.EMPTY_TEXT
    if not text:
        raise ValueError('Invalid text')
    # Limited text (Limit requests to settings.translation_limit)
    limited_text = text[:settings.translation_limit]
    detected_language = translate.detect_language(limited_text)
    # Submit translation request.
    if detected_language != language:
        translated_text = translate.translate_text(language, limited_text)
    else:
        print 'No text to translate. Source language (%s) eq target language ' \
              '(%s)' % (
                  detected_language, language)
        return settings.EMPTY_TEXT
    # Verify language is detected and text is translated.
    if _LANGUAGE in detected_language and _TRANSLATED_TEXT in translated_text:
        # Clean text for SQL insertion.
        translation = translated_text[_TRANSLATED_TEXT].replace("'", "''")
    return translation
