import unittest

from utils import config_utils


class TestConfigUtils(unittest.TestCase):
    def test_language_supported(self):
        result = config_utils.language_supported('cpp11')
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()