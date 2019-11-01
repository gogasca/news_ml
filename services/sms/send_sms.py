"""Send SMS via Twilio API."""

from conf import settings
from twilio.rest import TwilioRestClient


def send_sms_alert(body='News ML', destination_number=None, **kwargs):
    """Send alarms via Twilio SMS API.

    :param body:
    :param destination_number:
    :param kwargs:
    :return:
    """
    try:
        if settings.SMS_ALERTS:
            account_sid = settings.TWILIO_ACCOUNTID
            auth_token = settings.TWILIO_TOKENID
            client = TwilioRestClient(account_sid, auth_token)

            if destination_number:
                message = client.messages.create(to=destination_number,
                                                 from_=settings.TWILIO_FROM,
                                                 body=body)
                print(str(message))
            else:
                for number in settings.PHONE_NUMBERS:
                    client.messages.create(to=number,
                                           from_=settings.TWILIO_FROM,
                                           body=body)

    except Exception as exception:
        print(exception)
