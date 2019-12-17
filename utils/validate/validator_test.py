import unittest
import json
from .validator import check_campaign, check_person, check_email_addresses, \
    check_report, check_translation, check_limit


class TestValidator(unittest.TestCase):
    """Our basic test class."""

    def test_campaign(self):
        """

        :return:
        """
        # Valid request
        self.assertTrue(check_campaign(
            json_request=json.loads("""{
                "provider": "techmeme",
                "report": {
                    "email": "gonzalo@newsml.io"
                },
                "translate": {
                    "language": "es"
                }}""")))
        # Valid campaign
        self.assertTrue(check_campaign(
            json_request=json.loads("""{
                "provider": "techmeme",
                "report": {
                    "email": "gonzalo@newsml.io"
                }}""")))
        # Valid campaign with limit
        self.assertTrue(check_campaign(
            json_request=json.loads("""{
                        "provider": "techmeme",
                        "limit": 8,
                        "report": {
                            "email": "gonzalo@newsml.io"
                        }}""")))
        # Valid campaign with report
        self.assertTrue(check_campaign(
            json_request=json.loads("""{
                                "provider": "techmeme",                                
                                "report": {
                                    "email": "gonzalo@newsml.io"
                                }}""")))
        # Invalid language.
        self.assertFalse(check_campaign(
            json_request=json.loads("""{
                "provider": "techmeme",
                "report": {
                    "email": "gonzalo@newsml.io"
                },
                "translate": {
                    "language": "en"
                }}""")))

        # Invalid campaign with invalid limit number
        self.assertTrue(check_campaign(
            json_request=json.loads("""{
                                "provider": "techmeme",
                                "limit": 0,
                                "report": {
                                    "email": "gonzalo@newsml.io"
                                }}""")))

    def test_person(self):
        """

        :return:
        """
        self.assertTrue(check_person(
            json_request=json.loads("""{"name": "Elon Musk"}""")))

    def test_email(self):
        """
        The actual test.
        Any method which starts with ``test_`` will considered as a test case.
        """
        self.assertTrue(check_email_addresses('gonzalo@newsml.io'))
        self.assertTrue(check_email_addresses(
            'gonzalo@newsml.io;carlos@newsml.io'))
        self.assertTrue(check_email_addresses('gonzalo@newsml.io;'))
        self.assertTrue(
            check_email_addresses(';gonzalo@newsml.io;'))
        self.assertFalse(
            check_email_addresses('gonzalo@newsml', check_mx=True))

    def test_report(self):
        """

        :return:
        """
        self.assertTrue(check_report(
            json.loads("""{"report": { "email": "gonzalo@newsml.io"}}""")))
        self.assertFalse(check_report(
            json.loads("""{"report": { "email": ""}}""")))
        self.assertFalse(
            check_report(json.loads("""{"report": { }}""")))

    def test_language(self):
        """

        :return:
        """
        self.assertTrue(check_translation(
            json.loads("""{"translate": {"language": "es"}}""")))
        self.assertTrue(check_translation(
            json.loads("""{"translate": {"language": "fr"}}""")))
        self.assertTrue(check_translation(
            json.loads("""{"translate": {"language": "de"}}""")))
        self.assertFalse(check_translation(
            json.loads("""{"translate": {"language": "xx"}}""")))
        self.assertFalse(check_translation(
            json.loads("""{"translate": {"language": 1}}""")))

    def test_limit(self):
        self.assertTrue(check_limit(
            json.loads("""{"limit": 5}""")))
        self.assertTrue(check_limit(
            json.loads("""{"limit": 1000000}""")))
        self.assertTrue(check_limit(
            json.loads("""{"limit": 1}""")))
        self.assertFalse(check_limit(
            json.loads("""{"limit": -1}""")))
        self.assertFalse(check_limit(
            json.loads("""{"limit": 0}""")))
        self.assertFalse(check_limit(
            json.loads("""{"limits": 1}""")))


if __name__ == '__main__':
    unittest.main()
