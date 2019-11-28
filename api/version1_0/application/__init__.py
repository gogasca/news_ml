"""API configuration."""

import os
import sys

FILEPATH = os.environ.get('NEWSML_ENV')
sys.path.append(FILEPATH)
