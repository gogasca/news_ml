import unittest
from .url_extract import get_domain


class TestValidator(unittest.TestCase):
    """Our basic test class."""

    def test_get_domain(self):
        """

        :return:
        """
        # Valid request
        self.assertEqual(get_domain('www.yahoo.com'), 'yahoo')
        self.assertEqual(get_domain('https://www.yahoo.co.uk'), 'yahoo')
        self.assertEqual(get_domain('https://www.yahoo.com.mx'), 'yahoo')
        self.assertEqual(get_domain('https://www.newsml.io'), 'newsml')
