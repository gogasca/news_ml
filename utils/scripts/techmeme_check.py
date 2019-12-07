from bs4 import BeautifulSoup
import requests

_HTML_TITLE_CLASS = 'ourh'
LXML = 'lxml'
HTML_HREF = 'href'


def extract_articles(url=None):
    """
    Extracts titles from Techcrunch Popular web page.
    Extract title, short url and article content.
    Based on URL creates a dictionary of objects. This URL serves as index
    Currently TechMeme does not have Content field, we extract summary.

    :param url:
    :return: articles
    """
    try:
        if not url:
            destination_url = 'https://www.techmeme.com/'
        response = requests.get(destination_url)
        soup = BeautifulSoup(response.content, LXML)
        titles_html = soup.find_all("a", class_=_HTML_TITLE_CLASS)
        for title in titles_html:
            print(title.text)
            print(title[HTML_HREF])
            print(title[HTML_HREF])
        print('Total articles found: ', len(titles_html))
    except Exception as e:
        print('We failed with error - %s.', e)


extract_articles()