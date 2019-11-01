"""Main class to handle Database connection."""

import logging
import bleach
import psycopg2
import psycopg2.extensions

from conf import logger
from conf import settings

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

log = logger.LoggerManager().getLogger("__app__",
                                       logging_file=settings.APP_LOGFILE)
log.setLevel(level=logging.DEBUG)


class Db(object):
    """Database handling."""

    def __init__(self,
                 server=settings.DBHOST,
                 username=settings.DBUSERNAME,
                 password=settings.DBPASSWORD,
                 database=settings.DBNAME,
                 port=settings.DBPORT, **kwargs):
        """
        :param server:
        :param username:
        :param password:
        :param database:
        :param port:
        :param kwargs:
        :return:
        """
        self.server = server
        self.username = username
        self.password = password
        self.database = database
        self.port = port
        self.conn = None
        self.dsn = 'dbname=%s host=%s port=%d user=%s password=%s' % (
            self.database,
            self.server,
            self.port,
            self.username,
            self.password)

    def initialize(self, dsn=None, **kwargs):
        """

        :param dsn:
        :param kwargs:
        :return:
        """
        if self.dsn:
            self.conn = psycopg2.connect(self.dsn)
            return True
        elif dsn:
            self.conn = psycopg2.connect(dsn)
            return True
        else:
            log.error('initialize() DB not initialized.')

    def insert_content(self, sql_query, id=''):
        """

        :param query:
        :param id:
        :return:
        """
        try:
            if self.conn:
                if id:
                    return_id = " RETURNING " + id + ";"
                else:
                    return_id = ";"
                cur = self.conn.cursor()
                final_query = sql_query + return_id
                log.info('SQL query: %s ' % final_query)
                cur.execute(final_query)
                self.conn.commit()
                if id:
                    return cur.fetchone()[0]
            else:
                log.error('insert_content() Invalid DB parameters to DB')
        except psycopg2.ProgrammingError as e:
            log.exception('insert_content() Database configuration: %r' % e)
        finally:
            if self.conn:
                self.conn.close()
            if cur:
                cur.close()

    def insert(self, query, values, id):
        """

        :param query:
        :param values:
        :param id:  Name of the field to return
        :return:
        Example:
        INSERT INTO posts (title, text, url, short_url, source, post_date)
        VALUES
        ( 'Hola','TSLA','http://w.com','','TECHMEME', now()')

        """
        try:
            if self.conn:
                if id:
                    return_id = " RETURNING " + id + ";"
                else:
                    return_id = ";"
                cur = self.conn.cursor()
                content = bleach.clean(values)
                # content = [bleach.clean(element) for element in content]
                final_query = query + " VALUES (" + content + ")" + return_id
                log.info('DB insert() Executing SQL query: ' + final_query)
                cur.execute(final_query)
                self.conn.commit()
                if id:
                    return cur.fetchone()[0]
            else:
                log.error('insert() Invalid DB parameters No connection to DB')

        except psycopg2.ProgrammingError as e:
            log.exception('insert() Database configuration: %r' % e)
        finally:
            if self.conn:
                self.conn.close()
            if cur:
                cur.close()

    def update(self, query):
        """

        :param query:
        :return:
        """
        try:
            if self.conn:
                cur = self.conn.cursor()
                cur.execute(query)
                self.conn.commit()
            else:
                log.error('update() Invalid db parameters')
                return
        except TypeError as e:
            log.exception('update() Database Error: %r' % e)
        except psycopg2.ProgrammingError as e:
            log.exception('update() Database configuration: %r' % e)
        finally:
            if self.conn:
                self.conn.close()
            if cur:
                cur.close()

    def query_multiple(self, query):
        """

        :param query:
        :return:
        """
        try:
            if self.conn:
                cur = self.conn.cursor()
                cur.execute(query)
                # A commit may go here...
                result = cur.fetchall()
                if result:
                    return result
            else:
                log.error('query_multiple() Invalid db parameters.')
                return
        except psycopg2.ProgrammingError as e:
            log.exception('query_multiple() Database configuration: %r' % e)
        finally:
            if self.conn:
                self.conn.close()
            if cur:
                cur.close()

    def query(self, query):
        """

        :param query:
        :return:
        """
        try:
            if self.conn:
                cur = self.conn.cursor()
                cur.execute(query)
                result = cur.fetchone()
                if result:
                    return result[0]
            else:
                log.error('query() Invalid db parameters.')
        except psycopg2.ProgrammingError as e:
            log.exception('query() Database configuration: %r' % e)
        finally:
            if self.conn:
                self.conn.close()
            if cur:
                cur.close()

    def clean_up(self):
        """
        Clean up idle connections
        :return:
        """
        query = "select pg_terminate_backend(pid) from pg_stat_activity where " \
                "usename = '" + settings.DBUSERNAME + \
                "' and state = 'idle' and query_start < current_timestamp - " \
                "interval '5 minutes';"
        try:
            if self.conn:
                cur = self.conn.cursor()
                cur.execute(query)
                # A commit may go here...
                rows = cur.fetchall()
                return rows
            else:
                log.error('clean_up() Invalid Database parameters')
                print('No connection to Database!')
        except psycopg2.ProgrammingError as e:
            log.exception('clean_up() Database configuration: %r' % e)
        finally:
            if self.conn:
                self.conn.close()
            if cur:
                cur.close()
