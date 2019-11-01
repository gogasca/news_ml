import logging
import time

from celery.task import task
from conf import logger
from conf import settings

from main.lib.news_api import top_news as news_ml
from services.nlp import utils as nlp_utils

log = logger.LoggerManager().getLogger("__app__",
                                       logging_file=settings.APP_LOGFILE)
log.setLevel(level=logging.DEBUG)


@task(name='process_campaign', queue='gold', bind=True, default_retry_delay=30,
      max_retries=3,
      soft_time_limit=settings.MAX_TASK_PROCESSING)
def process_campaign(self, campaign_instance):
    """Handle News request via API. Creates a celery task which run
    asynchronously.

    :param self:
    :param campaign_instance:
    :return:
    """

    log.info('process_campaign() Initializing...')

    # Select campaign instance based on Provider
    if campaign_instance.provider == settings.NEWS_API:
        log.info('process_campaign() News API')
        news_ml.launch(campaign_instance)
    else:
        log.info(
            'process_campaign() Provider not found: %s' %
            campaign_instance.provider)
        campaign_instance.terminate(status='-1')
    # Terminate campaign. Update database with end_date.
    campaign_instance.terminate()


@task(name='process_clustering', queue='gold', bind=True,
      default_retry_delay=30, max_retries=3,
      soft_time_limit=settings.MAX_TASK_PROCESSING)
def process_clustering(self, clustering_instance):
    """Handle Clustering request via API. Creates a celery task which run
    asynchronously.


    :param self:
    :param clustering_instance:
    :return:
    """
    log.info('process_clustering() Initializing...')
    campaign_status = 1
    start_time = time.time()
    log.info('Clustering process started for: %s using %d clusters.' % (
        clustering_instance.campaign_reference,
        clustering_instance.num_of_clusters))
    clustering_instance.get_articles()
    try:
        clustering_instance.process_articles()
    except ValueError as exception:
        campaign_status = -1
        log.exception(exception)
    elapsed_time = time.time() - start_time
    log.info(
        'process_clustering() Process took %f seconds processed.' %
        elapsed_time)
    # Terminate campaign. Update database with end_date
    clustering_instance.terminate(status=campaign_status)


@task(name='rank_news', queue='gold', bind=True, default_retry_delay=30, max_retries=3,
      soft_time_limit=settings.MAX_RANK_PROCESSING)
def rank_news(self, ranker_instance):
    """Rank a list of articles based on predefined algorithm.
        Algorithm in README.md file. Reads news then ranks them.

    :param self:
    :param ranker_instance:
    :return:
    """

    log.info('rank_news() Reading posts then ranking...')
    campaign_status = 1
    start_time = time.time()
    ranker_instance.rank_articles()
    elapsed_time = time.time() - start_time
    log.info('rank_news() Process took %f seconds processed ' % elapsed_time)
    # Terminate campaign. Update database with end_date.
    ranker_instance.terminate(status=campaign_status)


@task(name='process_text', queue='gold', bind=True, default_retry_delay=30,
      max_retries=3, soft_time_limit=settings.MAX_API_PROCESSING)
def process_text(self, text_instance):
    """Process sentiment analysis u other text requests using Google Cloud
    NLP API.

    :param self:
    :param text_instance:
    :return:
    """

    log.info('process_text() Initializing...')
    start_time = time.time()

    if text_instance.run_sentiment_analysis:
        sentiment_analysis = nlp_utils.get_sentiment_scores(
            text_instance.content)
        if sentiment_analysis:
            score, magnitude = sentiment_analysis
            text_instance.sentiment_analysis = sentiment_analysis
            log.info(
                'process_text() Sentiment analysis: %s Score: %s Magnitude: '
                '%s' % (
                    text_instance.reference,
                    score,
                    magnitude))

    elapsed_time = time.time() - start_time
    log.info('process_text() Process took %f seconds processed ' % elapsed_time)
