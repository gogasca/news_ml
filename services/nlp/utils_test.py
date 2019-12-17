import json
import unittest
from .utils import extract_persons


class TestUrl(unittest.TestCase):
    """
    Our basic test class
    """

    def setUp(self):
        self.entities = """
            {
                "entities":  [
                    {
                        "salience":  0.2623617,
                         "mentions":  [
                            {
                                "text":  {
                                    "content":  "Etsy Q1",
                                     "beginOffset":  0
                                },
                                 "type":  "PROPER"
                            }
                        ],
                         "type":  "OTHER",
                         "name":  "Etsy Q1",
                         "metadata":  {

                        }
                    },
                     {
                        "salience":  0.25569758,
                         "mentions":  [
                            {
                                "text":  {
                                    "content":  "Chad Dickerson",
                                     "beginOffset":  38
                                },
                                 "type":  "PROPER"
                            },
                             {
                                "text":  {
                                    "content":  "CEO",
                                     "beginOffset":  34
                                },
                                 "type":  "COMMON"
                            }
                        ],
                         "type":  "PERSON",
                         "name":  "Chad Dickerson",
                         "metadata":  {

                        }
                    },
                     {
                        "salience":  0.17310241,
                         "mentions":  [
                            {
                                "text":  {
                                    "content":  "YoY",
                                     "beginOffset":  21
                                },
                                 "type":  "COMMON"
                            }
                        ],
                         "type":  "OTHER",
                         "name":  "YoY",
                         "metadata":  {

                        }
                    },
                     {
                        "salience":  0.08873737,
                         "mentions":  [
                            {
                                "text":  {
                                    "content":  "chair role",
                                     "beginOffset":  92
                                },
                                 "type":  "COMMON"
                            }
                        ],
                         "type":  "OTHER",
                         "name":  "chair role",
                         "metadata":  {

                        }
                    },
                     {
                        "salience":  0.085505955,
                         "mentions":  [
                            {
                                "text":  {
                                    "content":  "stock",
                                     "beginOffset":  139
                                },
                                 "type":  "COMMON"
                            }
                        ],
                         "type":  "OTHER",
                         "name":  "stock",
                         "metadata":  {

                        }
                    },
                     {
                        "salience":  0.07427541,
                         "mentions":  [
                            {
                                "text":  {
                                    "content":  "Josh Silverman",
                                     "beginOffset":  71
                                },
                                 "type":  "PROPER"
                            }
                        ],
                         "type":  "PERSON",
                         "name":  "Josh Silverman",
                         "metadata":  {
                            "mid":  "/m/026wfg",
                             "wikipedia_url":  "http:
                             //en.wikipedia.org/wiki/Skype"
                        }
                    },
                     {
                        "salience":  0.03789061,
                         "mentions":  [
                            {
                                "text":  {
                                    "content":  "firm",
                                     "beginOffset":  119
                                },
                                 "type":  "COMMON"
                            }
                        ],
                         "type":  "ORGANIZATION",
                         "name":  "firm",
                         "metadata":  {

                        }
                    },
                     {
                        "salience":  0.022428967,
                         "mentions":  [
                            {
                                "text":  {
                                    "content":  "Fred Wilson",
                                     "beginOffset":  106
                                },
                                 "type":  "PROPER"
                            }
                        ],
                         "type":  "PERSON",
                         "name":  "Fred Wilson",
                         "metadata":  {
                            "mid":  "/m/0261w4n",
                             "wikipedia_url":  "http:
                             //en.wikipedia.org/wiki/Fred_Wilson_(financier)"
                        }
                    }
                ]
            }
            """

    def test_extract_entities(self):
        """
        The actual test.
        Any method which starts with ``test_`` will considered as a test case.
        """

        assert extract_persons(json.loads(self.entities)) == [
            u'Chad Dickerson', u'Josh Silverman',
            u'Fred Wilson']


if __name__ == '__main__':
    unittest.main()
