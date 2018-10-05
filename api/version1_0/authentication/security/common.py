"""Handles Security."""

import os

from cryptography.fernet import Fernet


def encrypt(plain_text):
    """Encrypt using plain text.

    Reference: https://cryptography.io/en/latest/fernet/

    :param plain_text:
    :return:
    """
    crypto = Fernet(os.environ.get('SECRET_FERNET_KEY'))
    if not crypto:
        raise Exception('decrypt() No Key defined in ENV')

    if isinstance(plain_text, basestring):
        string_text = str(plain_text)
        return crypto.encrypt(bytes(string_text))
    else:
        raise Exception('encrypt() Only strings are allowed.')


def decrypt(cipher_text):
    """

    :param cipher_text:
    :return:
    """
    key = os.environ.get('SECRET_FERNET_KEY')
    if key:
        crypto = Fernet(key)
    else:
        raise Exception('decrypt() No Key defined in ENV')

    if not crypto:
        raise Exception('decrypt() No Crypto defined')
    else:
        return crypto.decrypt(bytes(cipher_text))
