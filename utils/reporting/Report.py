from utils.reporting import Generator
from services.email_client import email_client

_SEPARATOR = ' \n'


class Report(object):
    """
    Class instance to generate Email reports
    """

    def __init__(self, id=None,
                 subject='Silicon Valley | Daily Automatic Summary Report'):
        self._id = id
        if self._id is None:
            self._id = Generator.Generator().get_uuid()
        self._content = ''
        self._email_recipients = []
        self.valid_content = False
        self.subject = subject
        self.add_title('News ML')
        self.add_subtitle('Daily Summary Report')

    def add_title(self, title=''):
        """Adds a H1 title to email body.

        :param title:
        :return:
        """
        if not self.content:
            self.content = ''
        self.content += '<h1 style="text-align: center;"><span style="color: ' \
                        '#2b2301;">%s</span></h1>' % title

    def add_subtitle(self, subtitle=''):
        """Adds a H2 title to email body.

        :param subtitle:
        :return:
        """
        if not self.content:
            self.content = ''
        self.content += '<h2 style="text-align: center;"><span style="color: ' \
                        '#339966;">%s</span></h2>' % subtitle

    def add_body(self, body):
        """

        :param body:
        :return:
        """
        self.valid_content = True
        if not self.content:
            self.content = ''
        self.content += '<h4><span style="color: #339966;">%s%s &nbsp;</h4>' % (
        body, _SEPARATOR)

    def add_content(self, location, content):
        """Adds HTML text to email body.

        :param location:
        :param content:
        :return:
        """
        self.valid_content = True
        if not self.content:
            self.content = ''
        self.content += '<li> %s%s &nbsp;<a href=%s>Link</a></li><br/>' % (
        content, _SEPARATOR, location)

    def send(self):
        """Sends report via email. Using mail library.

        :return:
        """
        if self.valid_content:
            email_client.send_email_mailgun(
                email_recipients=self.email_recipients,
                subject=self.subject,
                body=self.content)
        else:
            print('Invalid content')

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        self._content = content

    @property
    def email_recipients(self):
        return self._email_recipients

    @email_recipients.setter
    def email_recipients(self, email_recipients):
        self._email_recipients = email_recipients

    @property
    def persons(self):
        return self._persons

    @persons.setter
    def persons(self, persons):
        self._persons = persons

    @property
    def organizations(self):
        return self._organizations

    @organizations.setter
    def organizations(self, organizations):
        self._organizations = organizations

    @property
    def __str__(self):
        return 'Report: <{}> Title: <{}>'.format(self._title)
