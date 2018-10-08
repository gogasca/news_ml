import urlparse

GENERIC_TLDS = [
    'aero', 'asia', 'biz', 'com', 'coop', 'edu', 'gov', 'info', 'int', 'jobs',
    'mil', 'mobi', 'museum', 'name', 'net', 'org', 'pro', 'tel', 'travel', 'cat'
]


def get_domain(url):
    """

    :param url:
    :return:
    """

    hostname = urlparse.urlparse(url.lower()).netloc
    if hostname == '':
        # Force the recognition as a full URL
        hostname = urlparse.urlparse('http://' + url).netloc

    # Remove the 'user:passw', and ':port' parts
    hostname = filter(None,
                      hostname.split('@')[-1].split(':')[0].lstrip('www').split(
                          '.'))
    num_parts = len(hostname)
    if (num_parts < 3) or (len(hostname[-1]) > 2):
        return '.'.join(hostname[:-1])
    if len(hostname[-2]) > 2 and hostname[-2] not in GENERIC_TLDS:
        return '.'.join(hostname[:-1])
    if num_parts >= 3:
        return '.'.join(hostname[:-2])
