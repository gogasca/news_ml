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
    if not settings.EMAIL_REPORT:
        print('Email report is disabled in settings.EMAIL_REPORT')
        return
    if not email_recipients:
        raise ValueError('Empty email recipient')
    if not body:
        raise ValueError('Empty body')

    url = 'https://api.mailgun.net/v3/%s/messages' % settings.MAILGUN_DOMAIN
    response = requests.post(url,
                             auth=('api', settings.MAILGUN_API_KEY),
                             data={"from": '%s <%s>' % (
                                 settings.EMAIL_NAME, settings.MAILGUN_SENDER),
                                   "to": email_recipients,
                                   "subject": subject,
                                   "html": body})

    print(response.text, response.status_code, response.reason)
    if response.status_code == 200:
        print('Email sent successfully!')
    else:
        print('Email failed! Something went wrong...:(')


def send_email(email_recipients=None, subject='News Email sender',
               body='Hello from News ML', **kwargs):
    """
    Send email via Gmail account via SMTP library. Use email settings which
    obtain information via ENV variables.

    :param email_to:
    :param subject:
    :param body:
    :return:
    """

    if not settings.EMAIL_REPORT:
        print('Email report is disabled in settings.EMAIL_REPORT')
        return

    if email_recipients is None:
        print('Warning: email_recipients is empty using default ' \
              'settings.email_to')
        email_recipients = settings.EMAIL_TO

    if not email_recipients:
        raise ValueError('Empty email recipient')
    if not body:
        raise ValueError('Empty body')

    gmail_user = settings.EMAIL_ADDRESS
    gmail_password = settings.EMAIL_PASSWORD

    email_from = gmail_user

    msg = MIMEMultipart('alternative')
    msg.set_charset('utf8')
    msg['FROM'] = "%s <%s>" % (settings.EMAIL_NAME, email_from)
    msg['To'] = (", ".join(email_recipients))
    msg['Subject'] = Header(subject, "utf-8")
    _attach = MIMEText(body.encode('utf-8'), 'html', 'UTF-8')
    msg.attach(_attach)

    try:
        server = smtplib.SMTP(settings.EMAIL_SERVER, settings.EMAIL_PORT)
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
