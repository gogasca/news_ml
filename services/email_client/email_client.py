"""Sends Report via Email."""

import smtplib
import requests

from conf import settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


def send_email_mailgun(email_recipients=None, subject='News ML Email sender',
                       body='Hello from <b>News ML</b>',
                       **kwargs):
    """

    :param email_recipients:
    :param subject:
    :param body:
    :param kwargs:
    :return:
    """
    if not settings.email_report:
        print('Email report is disabled in settings.email_report')
        return
    if not email_recipients:
        raise ValueError('Empty email recipient')
    if not body:
        raise ValueError('Empty body')

    url = 'https://api.mailgun.net/v3/sandboxd889a188057e4256a7c9d29e6688b406' \
          '.mailgun.org/messages'
    response = requests.post(url,
                             auth=('api', settings.mailgun_api_key),
                             data={"from": '%s <%s>' % (
                                 settings.email_name, settings.mailgun_sender),
                                   "to": email_recipients,
                                   "subject": subject,
                                   "html": body})

    print(response.text, response.status_code, response.reason)
    if response.status_code == 200:
        print('Email sent successfully!')
    else:
        print('Email failed! Something went wrong...:(')


def send_email(email_recipients=None, subject='Techie(8) Email sender',
               body='Hello from Techie(8)', **kwargs):
    """
    Send email via Gmail account via SMTP library. Use email settings which
    obtain information via ENV variables.

    :param email_to:
    :param subject:
    :param body:
    :return:
    """

    if not settings.email_report:
        print('Email report is disabled in settings.email_report')
        return

    if email_recipients is None:
        print('Warning: email_recipients is empty using default ' \
              'settings.email_to')
        email_recipients = settings.email_to

    if not email_recipients:
        raise ValueError('Empty email recipient')
    if not body:
        raise ValueError('Empty body')

    gmail_user = settings.email_address
    gmail_password = settings.email_password

    email_from = gmail_user

    msg = MIMEMultipart('alternative')
    msg.set_charset('utf8')
    msg['FROM'] = "%s <%s>" % (settings.email_name, email_from)
    msg['To'] = (", ".join(email_recipients))
    msg['Subject'] = Header(subject, "utf-8")
    _attach = MIMEText(body.encode('utf-8'), 'html', 'UTF-8')
    msg.attach(_attach)

    try:
        server = smtplib.SMTP(settings.email_server, settings.email_port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(email_from, email_recipients, msg.as_string())
        server.close()
        print('Email sent successfully!')
        return True
    except Exception as exception:
        print('Email failed! Something went wrong...:(')
        print(exception)
