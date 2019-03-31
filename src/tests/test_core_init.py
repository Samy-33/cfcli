import os
import unittest
import uuid

from core import init
# from settings import logger
from utils.constants import REPOSITORY_DIRECTORY_NAME


class TestCoreInit(unittest.TestCase):

    def test_valid_contest(self):
        is_contest_valid = init.helpers.valid_contest(100)
        self.assertTrue(is_contest_valid)

    def test_is_already_initialized(self):
        cfcli_path = os.path.join(os.getcwd(), REPOSITORY_DIRECTORY_NAME)

        backup_cfcli_path = str(uuid.uuid4())

        if os.path.exists(cfcli_path):
            backup_cfcli_path = cfcli_path + backup_cfcli_path
            os.system(f'mv {cfcli_path} {backup_cfcli_path}')

        is_initialized = init.helpers.is_already_initilized()

        if os.path.exists(backup_cfcli_path):
            os.system(f'mv {backup_cfcli_path} {cfcli_path}p')

        self.assertFalse(is_initialized)


if __name__ == '__main__':
    unittest.main()
