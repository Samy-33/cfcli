import unittest

import click
from click.testing import CliRunner

from cli import clean, init
# from settings import logger
from utils import config_utils
from utils.decorators import Rules, enforce_rules


class TestConfigUtils(unittest.TestCase):
    def test_language_supported(self):
        result = config_utils.language_supported('cpp11')
        self.assertTrue(result)


class TestDecorators(unittest.TestCase):
    def setUp(self):

        @click.group()
        def cli_temp():
            pass

        @cli_temp.command()
        def repo_must_be_initd():
            @enforce_rules(Rules.REPOSITORY_INITIALISED)
            def wrapped():
                pass

            wrapped()

        @cli_temp.command()
        def repo_must_not_be_initd():

            @enforce_rules(Rules.REPOSITORY_NOT_INITIALISED)
            def wrapped():
                pass

            wrapped()

        self.repo_must_be_initd = repo_must_be_initd
        self.repo_must_not_be_initd = repo_must_not_be_initd

        self.runner = CliRunner()

    def test_enfore_rules_func(self):
        with self.runner.isolated_filesystem():

            self.runner.invoke(init, ['-cc', '1000'], input='y\n')

            result = self.runner.invoke(self.repo_must_be_initd)

            self.assertEqual(result.exit_code, 0,
                             'Repo initialised but Rules.REPOSITORY_INITIALISED not enforced')

            result = self.runner.invoke(self.repo_must_not_be_initd)
            self.assertNotEqual(result.exit_code, 0,
                                'Repo initialised and \
                                    Rules.REPOSITORY_NOT_INITIALISED not enforced')

            self.runner.invoke(clean)

            result = self.runner.invoke(self.repo_must_not_be_initd)
            self.assertEqual(result.exit_code, 0,
                             'Repo not initialised and \
                                 Rules.REPOSITORY_NOT_INITIALISED rule not enforced')

            result = self.runner.invoke(self.repo_must_be_initd)
            self.assertNotEqual(result.exit_code, 0,
                                'Repo initialised and Rules.REPOSITORY_INITIALISED not enforced')


if __name__ == '__main__':
    unittest.main()
