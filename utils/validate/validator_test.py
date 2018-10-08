import unittest
import json
import validator


class TestValidator(unittest.TestCase):
    """Our basic test class."""

    def test_campaign(self):
        """

        :return:
        """
        self.assertTrue(validator.check_campaign(
            json_request=json.loads("""{
                "provider": "techmeme",
                "report": {
                    "email": "gonzalo@techie8.com"
                },
                "translate": {
                    "language": "es"
                }}""")))
        self.assertTrue(validator.check_campaign(
            json_request=json.loads("""{
                "provider": "techmeme",
                "report": {
                    "email": "gonzalo@techie8.com"
                }}""")))
        # Invalid language.
        self.assertFalse(validator.check_campaign(
            json_request=json.loads("""{
                "provider": "techmeme",
                "report": {
                    "email": "gonzalo@techie8.com"
                },
                "translate": {
                    "language": "en"
                }}""")))

    def test_person(self):
        """

        :return:
        """
        self.assertTrue(validator.check_person(
            json_request=json.loads("""{"name": "Elon Musk"}""")))

    def test_email(self):
        """
        The actual test.
        Any method which starts with ``test_`` will considered as a test case.
        """
        self.assertTrue(validator.check_email_addresses('gonzalo@techie8.com'))
        self.assertTrue(validator.check_email_addresses(
            'gonzalo@techie8.com;carlos@techie8.com'))
        self.assertTrue(validator.check_email_addresses('gonzalo@techie8.com;'))
        self.assertTrue(
            validator.check_email_addresses(';gonzalo@techie8.com;'))
        self.assertFalse(
            validator.check_email_addresses('gonzalo@techie8', check_mx=True))

    def test_report(self):
        """

        :return:
        """
        self.assertTrue(validator.check_report(
            json.loads("""{"report": { "email": "gonzalo@techie8.com"}}""")))
        self.assertFalse(validator.check_report(
            json.loads("""{"report": { "email": ""}}""")))
        self.assertFalse(
            validator.check_report(json.loads("""{"report": { }}""")))

    def test_language(self):
        """

        :return:
        """
        self.assertTrue(validator.check_translation(
            json.loads("""{"translate": {"language": "es"}}""")))
        self.assertTrue(validator.check_translation(
            json.loads("""{"translate": {"language": "fr"}}""")))
        self.assertTrue(validator.check_translation(
            json.loads("""{"translate": {"language": "de"}}""")))
        self.assertFalse(validator.check_translation(
            json.loads("""{"translate": {"language": "xx"}}""")))
        self.assertFalse(validator.check_translation(
            json.loads("""{"translate": {"language": 1}}""")))


if __name__ == '__main__':
    unittest.main()
