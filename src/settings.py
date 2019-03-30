import json
import logging
import os
from utils.constants import FilePathConstants

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

config = json.load(open(os.path.join(PROJECT_ROOT, FilePathConstants.CONFIG_FILE_PATH), 'r'))

if os.environ.get('CFCLI_ENV', 'prod') == 'dev':
    logging.basicConfig(level=logging.DEBUG)


logger = logging.getLogger('cfcli_logger')
