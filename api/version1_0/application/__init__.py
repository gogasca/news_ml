import platform
import sys
import warnings

if platform.system() == 'Linux':
    filepath = '/usr/local/src/gonzo/'
else:
    filepath = '/Users/gogasca/Documents/Development/dpe/news/'
warnings.filterwarnings("ignore")
sys.path.append(filepath)
