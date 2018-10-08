import logging
import time

from celery.task import task
from conf import logger
from conf import settings

from main.lib.usa.news_api import top_news as news_ml
from services.nlp import utils as nlp_utils
from services.ranking import RankerD

log = logger.LoggerManager().getLogger("__app__",
                                       logging_file=settings.app_logfile)
log.setLevel(level=logging.DEBUG)


@task(name='process_campaign', queue='gold', bind=True, default_retry_delay=30,
      max_retries=3,
      soft_time_limit=settings.max_task_processing)
def process_campaign(self, campaign_instance):
    """Handle News request via API. Creates a celery task which run
    asynchronously.

    :param self:
    :param campaign_instance:
    :return:
    """

    log.info('process_campaign() Initializing...')
    start_time = time.time()
    # Select campaign instance based on Provider
    if campaign_instance.provider == settings.news_api:
        log.info('process_campaign() News API')
        news_ml.launch(campaign_instance)
    else:
        log.info(
            'process_campaign() Provider not found: %s' %
            campaign_instance.provider)
        campaign_instance.terminate(status='-1')

    elapsed_time = time.time() - start_time
    log.info(
        'process_campaign() Process took %f seconds processed ' % elapsed_time)
    if settings.rank_articles:
        log.info('rank_news() Reading posts then ranking...')
        ranker_instance = RankerD.RankerD(campaign_instance.reference)
        ranker_instance.rank_articles()
        log.info('rank_news() Process took %f seconds processed ' % elapsed_time)
    # Terminate campaign. Update database with end_date.
    campaign_instance.terminate()


@task(name='process_text', queue='gold', bind=True, default_retry_delay=30,
      max_retries=3,
      soft_time_limit=settings.max_api_processing)
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
