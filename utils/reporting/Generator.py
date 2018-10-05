"""Generates a new UUID."""

import random
import string
import uuid


class Generator(object):

    def __init__(self):
        """

        :return:
        """
        pass

    @staticmethod
    def generate_job(job_length):
        """
        :param job_length:
        :return:
        """

        return ''.join(
            random.SystemRandom().choice(string.ascii_uppercase + string.digits)
            for _ in range(job_length))

    def get_uuid(self):
        """

        :return:
        """
        return (str(uuid.uuid1()).upper().replace("-", "")[:8].lower() + '-' + \
                self.generate_key(4, 4) + '-' + \
                str(uuid.uuid1()).upper().replace("-", "")[:10].lower()).lower()

    @staticmethod
    def get_registration_code():
        """

        :return:
        """
        return ''.join(
            random.SystemRandom().choice(string.digits) for _ in range(4))

    @staticmethod
    def generate_key(parts, job_length):
        """

        :param parts:
        :param job_length:
        :return:
        """
        if parts > 0 and job_length > 0:
            key = ''
            for y in xrange(0, parts):
                key += ''.join(
                    random.SystemRandom().choice(
                        string.ascii_uppercase + string.digits) for _ in
                    range(job_length))
                key += '-'

            # Remove last characters
            return key[:-1]
        return ''
