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
            destination_url = 'https://www.techmeme.com'
        response = requests.get(destination_url)
        soup = BeautifulSoup(response.content, 'lxml')
        titles_html = soup.find_all('a', class_='ourh')
        print(len(titles_html))
        published_dates = soup.find_all('div', class_='itc2')
        print(len(published_dates))
        #names_html = soup.find_all('a')
        published_dates = [x.get('id') for x in published_dates if x.get('id')]
        print(published_dates)
        print('Articles found: {}'.format(len(titles_html)))
        print('Dates found: {}'.format(len(published_dates)))
        articles = {}
        count = 0
        for title in titles_html:
            url = title.get('href')
            if not articles.get(url):
                print(url)
                articles[url] = count
                count = count + 1
        print(len(articles))
        print(count)
        print(articles)
    except Exception as e:
        print(e)


extract_articles()