"""Extract URL information"""

import base64
import logging
import requests


from io import BytesIO
from urllib.parse import urlparse
from tenacity import retry, retry_if_exception_type, stop_after_attempt, \
    wait_exponential

_RATE_LIMIT_RETRIES = 3
_RETRY_DELAY = 1
_RETRY_MULTIPLIER = 1
_RETRY_MAX_DELAY = 4

GENERIC_TLDS = [
    'aero', 'asia', 'biz', 'com', 'coop', 'edu', 'gov', 'info', 'int', 'jobs',
    'mil', 'mobi', 'museum', 'name', 'net', 'org', 'pro', 'tel', 'travel', 'cat'
]


def get_domain(url):
    """

    :param url:
    :return:
    """

    hostname = urlparse(url.lower()).netloc
    if hostname == '':
        # Force the recognition as a full URL
        hostname = urlparse('http://' + url).netloc

    # Remove the 'user:passw', and ':port' parts
    hostname = list(filter(None,
                           hostname.split('@')[-1].split(':')[0].lstrip(
                               'www').split(
                               '.')))
    num_parts = len(hostname)
    if (num_parts < 3) or (len(hostname[-1]) > 2):
        return '.'.join(hostname[:-1])
    if len(hostname[-2]) > 2 and hostname[-2] not in GENERIC_TLDS:
        return '.'.join(hostname[:-1])
    if num_parts >= 3:
        return '.'.join(hostname[:-2])


@retry(retry=retry_if_exception_type(Exception),
       stop=stop_after_attempt(_RATE_LIMIT_RETRIES),
       wait=wait_exponential(multiplier=_RETRY_MULTIPLIER,
                             min=_RETRY_DELAY,
                             max=_RETRY_MAX_DELAY),
       reraise=True,)
def convert_image(image_url):
    """

    :param image_url:
    :return:
    """
    if not image_url:
        raise ValueError('No image')
    logging.info('Converting image [{}] to base64...'.format(image_url))
    headers = requests.utils.default_headers()
    session = requests.Session()
    response = session.get(image_url, headers=headers)
    content_type = response.headers['content-type']
    if 'image' not in content_type:
        logging.error('Not a valid image type {}'.format(content_type))
        return
    buffered = BytesIO(response.content)
    img_base64 = base64.b64encode(buffered.getvalue())
    return """<br/><img src="data:{};base64,{}" alt="img"/>""".format(
        content_type,
        img_base64.decode())


