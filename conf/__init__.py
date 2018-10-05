import platform
import sys

if platform.system() == 'Linux':
    filepath = '/usr/local/src/gonzo/'
else:
    filepath = '/Users/gogasca/Documents/Development/dpe/news/'
sys.path.append(filepath)
