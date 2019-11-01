#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import nltk
import re

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from services.nlp import nlp

from conf import settings
from conf import logger

log = logger.LoggerManager().getLogger("__app__",
                                       logging_file=settings.APP_LOGFILE)
log.setLevel(level=logging.DEBUG)

_ENTITIES = 'entities'
_METADATA = 'metadata'
_TYPE = 'type'
_NAME = 'name'
_MENTIONS = 'mentions'
_SALIENCE = 'salience'
_PERSON = 'PERSON'

STOP_WORDS = set(stopwords.words("english"))


def extract_filter(dictionary=settings.ENTITY_FILTER):
    """

    :param dictionary:
    :return:
    """
    with open(dictionary) as f:
        return f.read().splitlines()


def extract_tags(text):
    """

    :param text:
    :return:
    """
    try:
        relevant_words = []
        if _ENTITIES in text:
            for entity in text[_ENTITIES]:
                if entity[_SALIENCE] > settings.SALIENCE_SCORE and text[
                    'language'] == 'en' \
                        or text['language'] == 'es':
                    if _MENTIONS in entity:
                        if len(entity[_MENTIONS]) > 0:
                            # Fix NLP defect getting: ['season', "u'SNL",
                            # "u'Saturday Night Live"]
                            word = entity[_MENTIONS][0]['text'][
                                'content'].replace("u'", "").replace("'", "''")
                            relevant_words.append(word)
                elif entity[
                    _SALIENCE] < settings.SALIENCE_SCORE and \
                        settings.LOG_SALIENCE:
                    log.warning('extract_tags() Salience score is too low [%r]',
                                entity[_SALIENCE])
        log.info('extract_tags() Found relevant keywords: %r',
                 list(set(relevant_words)))
        # Remove duplicate words if any.
        return list(set(relevant_words))
    except KeyError as e:
        log.exception(e)
    except TypeError as e:
        log.exception(e)


def extract_entity(entities, entity_type=_PERSON):
    """
    Extract name from the entity specified in entity_type.
    We use the JSON format to extract the entity information:
        -

    :param entities:
    :param entity_type:
    :return:
    """
    if not entity_type:
        raise ValueError('Invalid entity type')
    if _ENTITIES not in entities:
        raise ValueError('No entities format')
    try:
        extracted_entities = []
        log.info('extract_entity() Searching for %s in %r', entity_type,
                 entities)
        for entity in entities[_ENTITIES]:
            # Extract entity (PERSON, ORGANIZATION)
            if _TYPE in entity:
                if entity[_TYPE] == entity_type:
                    entity_name = entity[_NAME]
                    log.info('extract_entity() Extracting %s from entity %s',
                             entity_type, entity_name)
                    if entity_name[0].isupper():
                        if entity[_METADATA]:
                            log.info('extract_entity() | Insert %s: %s | %s ',
                                     entity_type, entity_name,
                                     entity[_METADATA])
                            extracted_entities.append(entity[_NAME])
                        else:
                            # Filter entity name by discarding dictionary of
                            # words.
                            if not set(extract_filter()) & set(
                                    entity_name.lower().split()):
                                log.info('extract_entity() | Insert %s %s ',
                                         entity_type, entity_name)
                                extracted_entities.append(entity[_NAME])
        return extracted_entities
    except KeyError as e:
        log.exception(e)


def extract_persons(entities):
    """

    :param entities:
    :return:
    """
    try:
        persons = []
        for entity in entities[_ENTITIES]:
            # Extract PERSON from tags
            if _TYPE in entity:
                if entity[_TYPE] == _PERSON:
                    entity_name = entity[_NAME]
                    log.info(
                        'extract_person() Extracting person from entity %s',
                        entity_name)
                    if len(entity_name.lower().split()) > 1 and entity_name[
                        0].isupper():
                        if entity[_METADATA]:
                            log.info(
                                'extract_person() | Insert Person: %s | %s ',
                                entity_name, entity[_METADATA])
                            persons.append(entity[_NAME])
                        else:
                            # Filter person name by discarding dictionary of
                            # words.
                            if not set(extract_filter()) & set(
                                    entity_name.lower().split()):
                                log.info('extract_person() | Insert Person %s ',
                                         entity_name)
                                persons.append(entity[_NAME])
        return persons
    except KeyError as e:
        log.exception(e)


def tokenize_and_stem(document):
    """Tokenize by sentence, then by word to ensure that punctuation is
    caught as it's own token.

    :param document:
    :return:
    """
    tokens = [word for sent in nltk.sent_tokenize(document) for word in
              nltk.word_tokenize(sent) if
              word not in STOP_WORDS]
    filtered_tokens = []
    # Filter out any tokens not containing letters (e.g., numeric tokens,
    # raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)

    stemmer = SnowballStemmer('english')
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems


def tokenize_only(document):
    """Tokenize by sentence, then by word to ensure that punctuation is
    caught as it's own token.

    :param document:
    :return:
    """
    tokens = [word.lower() for sent in nltk.sent_tokenize(document) for word in
              nltk.word_tokenize(sent) if
              word not in STOP_WORDS]
    filtered_tokens = []
    # Filter out any tokens not containing letters (e.g., numeric tokens,
    # raw punctuation).
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens


def get_sentiment_scores(text):
    """

    Sentiment analysis:
        "documentSentiment": {
            "magnitude": 2.4,
            "score": 0.4
        },

    https://cloud.google.com/natural-language/docs/basics#interpreting_sentiment_analysis_values

    :param text:

    :return: a tuple score and magnitude.
    """
    if not text:
        raise ValueError('No text')
    sentiment_anaysis_result = nlp.analyze_sentiment(text)
    document_sentiment = sentiment_anaysis_result.get('documentSentiment')
    score = document_sentiment.get('score')
    magnitude = document_sentiment.get('magnitude')
    if score and magnitude:
        return score, magnitude
    return 0, 0


def get_sentiment(score):
    """Returns sentiment analysis value based in score. # TODO(gonzalo) use magnitude.
    :param score:
    :return:
    """
    if score > 0:
        return 'positive'
    elif score == 0:
        return 'neutral'
    else:
        return 'negative'
