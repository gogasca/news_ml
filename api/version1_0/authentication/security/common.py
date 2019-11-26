"""Handles Security."""

import os
from cryptography.fernet import Fernet


def encrypt(plain_text):
    """Encrypts using plain text using SECRET_FERNET_KEY.

    Reference: https://cryptography.io/en/latest/fernet/

    :param plain_text:
    :return:
    """
    crypto = Fernet(os.environ.get('SECRET_FERNET_KEY'))
    if not crypto:
        raise Exception('decrypt() No Key defined in ENV')
    if isinstance(plain_text, str):
        string_text = str(plain_text)
        return crypto.encrypt(bytes(string_text))
    else:
        raise Exception('encrypt() Only strings are allowed.')


def decrypt(cipher_text):
    """Decrypts using SECRET_FERNET_KEY.

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
