import unittest

import click

from cli import clean, init
from core import init as init_core


class TestCoreInit(unittest.TestCase):

    def setUp(self):
        self.runner = click.testing.CliRunner()

    def test_valid_contest(self):
        is_contest_valid = init_core.helpers.valid_contest(100)
        self.assertTrue(is_contest_valid)

    def test_init_command_passing(self):
        '''Should pass for correct contest code
        '''
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(init, ['-cc', '100'])
            self.assertEqual(result.exit_code, 0, f'init command fails for contest code 100.')

    def test_init_command_failing(self):
        '''Should fail with return code 1 for incorrect contest code
        '''
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(init, ['-cc', '0'])
            self.assertEqual(result.exit_code, 1, f'Expected Return Code 1 found \
                             {result.exit_code}')

    def test_clean_command_passing(self):
        '''Must pass for repository initialised
        '''
        with self.runner.isolated_filesystem():
            self.runner.invoke(init, ['-cc', '100'])

            result = self.runner.invoke(clean)
            self.assertEqual(result.exit_code, 0, f'Repository Initialized. But clean command \
                             fails.')

    def test_clean_command_failing(self):
        '''Must fail as repository not initialised
        '''
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(clean)

            self.assertEqual(result.exit_code, 1, f'clean command returned code \
                             {result.exit_code} instead of 1')


if __name__ == '__main__':
    unittest.main()
