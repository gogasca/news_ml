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
        if settings.sms_alerts:
            account_sid = settings.twilio_accountId
            auth_token = settings.twilio_tokenId
            client = TwilioRestClient(account_sid, auth_token)

            if destination_number:
                message = client.messages.create(to=destination_number,
                                                 from_=settings.twilio_from,
                                                 body=body)
                print(str(message))
            else:
                for number in settings.phone_numbers:
                    client.messages.create(to=number,
                                           from_=settings.twilio_from,
                                           body=body)

    except Exception as excpt:
        print(excpt)
