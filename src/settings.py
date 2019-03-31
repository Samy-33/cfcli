import json
import logging
import os

from utils.constants import FilePathConstants

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

config = json.load(open(os.path.join(PROJECT_ROOT, FilePathConstants.CONFIG_FILE_PATH), 'r'))

DEBUG = os.environ.get('CFCLI_ENV', 'prod') == 'dev'

if DEBUG:
    # logging.basicConfig(format='%(asctime)s - %(levelname)s: %(name)s: \
    #     %(pathname)s - %(message)s')
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(name)s: %(pathname)s:%(lineno)s - \
        %(message)s', level=logging.DEBUG)


logger = logging.getLogger('cfcli_logger')
