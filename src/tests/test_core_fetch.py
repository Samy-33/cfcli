import unittest

import click

from cli import fetch, init


class TestCoreFetch(unittest.TestCase):
    def setUp(self):

        self.runner = click.testing.CliRunner()

    def test_fetch_cli(self):
        with self.runner.isolated_filesystem():
            self.runner.invoke(init, ['-cc', '100'])
            result = self.runner.invoke(fetch, ['-s'], input='y')

            self.assertEqual(result.exit_code, 0, f'cli exitted with non zero code')
