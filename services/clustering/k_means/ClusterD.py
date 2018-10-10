"""Cluster instance."""

import clustering
import logging
import pandas as pd
import re

from api.version1_0.database import DbHelper
from conf import settings

from services.nlp.utils import tokenize_and_stem
from services.nlp.utils import tokenize_only
from utils.reporting import Generator
from utils.reporting import Report
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_articles_by_date(date):
    """

    :param date:
    :return:
    """
    logging.info('Looking news for %s', date)
    articles = DbHelper.get_multiple_records(
        settings.clustering_query_get_news % date)
    logging.info('Total news found: %s', len(articles))
    return articles


def get_cosine_similarity(document, document_list):
    """
    :param document:
    :param document_list:
    :return:
    """
    all_documents = document + document_list
    tfidf_vectorizer = TfidfVectorizer(stop_words='english',
                                       ngram_range=(1, 3))
    tfidf_matrix = tfidf_vectorizer.fit_transform(all_documents)
    cosine_results = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
    if cosine_results.tolist():
        return cosine_results.tolist()[0]
    return None


def get_document_term_matrix(all_documents):
    """ Counts word occurrences by document. Then transform it into a
    document-term matrix (dtm).

    Returns a Tf-idf matrix, first count word occurrences by document.
    This is transformed into a document-term matrix (dtm). This is also
    just called a term frequency matrix.
    :param all_documents:
    :return:
    """
    tfidf_vectorizer = TfidfVectorizer(stop_words='english',
                                       ngram_range=(1, 3))
    tfidf_matrix = tfidf_vectorizer.fit_transform(all_documents)
    terms = tfidf_vectorizer.get_feature_names()
    logging.info('Total terms found: %d' % len(terms))
    logging.info('(TFM/DTM) Matrix size: %s' % (tfidf_matrix.shape,))
    return terms, tfidf_matrix


def document_processor(documents):
    """Tokenize words in documents.

    :param documents:
    :return:
    """
    total_vocab_stemmed = []
    total_vocab_tokenized = []
    for document in documents:
        # Use NLP Libraries for tokenize and stem.
        all_words_stemmed = tokenize_and_stem(document)
        total_vocab_stemmed.extend(all_words_stemmed)
        all_words_tokenized = tokenize_only(document)
        total_vocab_tokenized.extend(all_words_tokenized)
    return total_vocab_stemmed, total_vocab_tokenized


def sort_articles(articles):
    """Sort articles based on score.

    :param articles:
    :return:
    """
    if articles < 1:
        raise ValueError('No news')

    sorted_articles = sorted(articles, key=lambda x: x.cluster)
    return sorted_articles


class Clustering(object):
    """Cluster class."""

    def __init__(self, num_of_clusters):
        """

        :param num_of_clusters:
        :return:
        """
        self.campaign_reference = Generator.Generator().generate_job(10)
        self._articles = None
        self._num_of_articles = 0
        self._num_of_clusters = num_of_clusters
        self.clustered_articles = []
        self.report = Report.Report(subject='News ML | Daily Clustered Report')
        self._send_report = False
        self._email_recipients = []

    @property
    def articles(self):
        return self._articles

    @articles.setter
    def articles(self, articles):
        self._articles = articles

    @property
    def email_recipients(self):
        return self._email_recipients

    @email_recipients.setter
    def email_recipients(self, email_recipients):
        self._email_recipients = email_recipients

    @property
    def send_report(self):
        return self._send_report

    @send_report.setter
    def send_report(self, send_report):
        self._send_report = send_report

    @property
    def num_of_articles(self):
        return self._num_of_articles

    @num_of_articles.setter
    def num_of_articles(self, num_of_articles):
        self._num_of_articles = num_of_articles

    @property
    def num_of_clusters(self):
        return self._num_of_clusters

    @num_of_clusters.setter
    def num_of_clusters(self, num_of_clusters):
        self._num_of_clusters = num_of_clusters

    def insert_records(self, clustered_news, campaign_reference):
        """
        :param clustered_news:
        :param campaign_reference:
        :return:
        """
        logging.info('Processing %d articles', len(clustered_news))
        sorted_clustered_news_list = sort_articles(clustered_news)
        clusters = set()
        for sort_clustered_news in sorted_clustered_news_list:
            cluster = (int(sort_clustered_news.cluster) + 1)
            if cluster not in clusters:
                logging.info('Cluster %d', cluster)
                self.report.add_body('<b>Cluster %d</b>' % cluster)
            clusters.add(cluster)
            DbHelper.insert_cluster_article(post_id=sort_clustered_news.news_id,
                                            title=sort_clustered_news.title,
                                            content=sort_clustered_news.content,
                                            source=sort_clustered_news.source,
                                            url=sort_clustered_news.url,
                                            cluster=cluster,
                                            campaign_reference=campaign_reference)
            self.report.add_content(sort_clustered_news.url,
                                    '%s | <b>Cluster</b>: %s | '
                                    '<b>Provider</b>: %s' % (
                                        sort_clustered_news.title,
                                        cluster,
                                        sort_clustered_news.source.upper()))
        logging.info('Process %d articles', len(sorted_clustered_news_list))

    def get_clusters(self, tfidf_matrix):
        """

        :rtype: object
        :param tfidf_matrix:
        :return:
        """
        logging.info(
            'Starting clustering [%d] clusters.' % self.num_of_clusters)
        km = KMeans(n_clusters=self.num_of_clusters)
        km.fit(tfidf_matrix)
        clusters = km.labels_.tolist()
        return clusters

    def assign_cluster(self, dataframe):
        """Assigns cluster to articles.

        :param dataframe:
        :return:
        """
        logging.info('Finding cluster information:')
        if self.num_of_clusters < settings.num_of_clusters:
            for idx in xrange(0, self.num_of_clusters):
                logging.info(dataframe.ix[idx]['title'])
        else:
            for idx in xrange(0, self.num_of_clusters):
                logging.warning('[%d] Cluster #%d titles:' % (idx, idx + 1))
                for title in dataframe.ix[idx]['title'].values.tolist():
                    try:
                        logging.info(title)
                    except AttributeError as exception:
                        logging.exception(exception)
        for _, record in dataframe.iterrows():
            record['news_article'].cluster = record['cluster']
            logging.info('Assigning cluster: %s to %s ' % (
                record['news_article'].cluster, record['url']))
        return dataframe

    def _set_articles(self, num_of_articles):
        """Set articles number in DB using campaign reference..

        :param num_of_articles:
        :return:
        """
        if isinstance(num_of_articles, int):
            self.num_of_articles = num_of_articles

        if self.campaign_reference and num_of_articles > -1:
            sqlquery = 'UPDATE campaign SET articles=%s WHERE ' \
                       'campaign.reference=\'%s\'' % (
                           num_of_articles, self.campaign_reference)
            DbHelper.update_database(sqlquery)

    def process_articles(self):
        """

        :return:
        """
        documents = []
        titles = []
        urls = []
        clustered_articles = []

        # Iterate over each extracted article in table _news_ from DB.
        for article in self.articles:
            # Create an instance of each article.
            clustered_article = clustering.ClusteredNews(news_id=article[0],
                                                         title=article[1],
                                                         content=article[2],
                                                         source=article[3],
                                                         url=article[4])
            clustered_articles.append(clustered_article)
            # Use both title and content.
            title = '%s' % article[1].lstrip()
            document = '%s %s' % (title.lstrip(), article[2].lstrip())
            url = '%s' % article[4]
            # Store information.
            documents.append(document)
            titles.append(title)
            urls.append(url)
            tokenize_only(document)
            if settings.process_cosine_similarity:
                get_cosine_similarity([document], documents)
        num_of_documents = len(documents)
        self._set_articles(num_of_articles=num_of_documents)
        logging.info('Processed %d documents.' % num_of_documents)
        if num_of_documents < self.num_of_clusters:
            raise ValueError(
                'Samples [%d] should be greater of equal number of '
                'clusters [%d].' % (
                    num_of_documents, self.num_of_clusters))

        # Extract terms in documents + term frequency matrix.
        terms, tfidf_matrix = get_document_term_matrix(documents)
        vocab_stemmed, vocab_tokenized = document_processor(documents)
        vocab_frame = pd.DataFrame({'words': vocab_tokenized},
                                   index=vocab_stemmed)
        logging.info('There are %d items in vocabulary.' % vocab_frame.shape[0])
        # This function executes clustering K-Means for the news articles.
        clusters = self.get_clusters(tfidf_matrix)
        news = {'url': urls, 'title': titles, 'document': documents,
                'cluster': clusters, 'news_article': clustered_articles}
        dataframe = pd.DataFrame(news, index=[clusters],
                                 columns=['url', 'title', 'document', 'cluster',
                                          'news_article'])
        logging.info('Overview:\n%r.' % dataframe['cluster'].value_counts())
        cluster_dataframe = self.assign_cluster(dataframe)
        if settings.update_clustering_articles_db:
            logging.info(
                'Inserting records in DB: %s.' % self.campaign_reference)
            self.insert_records(cluster_dataframe['news_article'].tolist(),
                                self.campaign_reference)

    def get_articles(self, date='latest'):
        """Read posts from database.

        :param date:
        :return:
        """

        # Get latest date for News inserted in Database.
        if date == 'latest':
            date = DbHelper.get_record(settings.clustering_query_date)
            logging.info('Using latest date. The latest date found was: %s',
                         date)
        logging.info('Using date: %s', date)
        if re.match('\d{4}-\d{1,2}-\d{2}', date):
            self.articles = get_articles_by_date(date)
            logging.info('Found %d articles.' % len(self.articles))
        return self.articles

    def terminate(self, status=1):
        """Updates campaign status and sends email report if reporting was
        enabled.

        :param status:
        :return:
        """
        if self.send_report:
            logging.info('Sending Email report')
            self.report.email_recipients = self.email_recipients
            self.report.send()

        if self.campaign_reference:
            sqlquery = 'UPDATE campaign SET campaign_end=\'%s\', status=%d ' \
                       'WHERE campaign.reference=\'%s\'' % (
                           settings.dbnow, status, self.campaign_reference)
            DbHelper.update_database(sqlquery)


"""
clustering_instance = Clustering(8)
clustering_instance.send_report = True
clustering_instance.email_recipients.append('gogasca@google.com')
articles = clustering_instance.get_articles()
clustering_instance.process_articles()
clustering_instance.terminate(1)
"""
