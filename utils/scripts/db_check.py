"""Verify DB connection."""
import os
import sys

FILEPATH = os.environ.get('NEWSML_ENV')

if not FILEPATH:
    raise Exception('Define NEWSML_ENV first')

sys.path.append(FILEPATH)
from api.version1_0.database import DbHelper


def main():
    DbHelper.test_connection()


if __name__ == "__main__":
    main()
