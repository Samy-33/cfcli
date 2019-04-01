import json
import os

import click

from core.api.api import is_contest_valid
from utils.config_utils import get_local_conf_file_path, get_repository_path
from utils.decorators import Rules, enforce_rules


class InitHelpers:
    '''Helper methods for handling initialization of cfcli repository
    '''

    def valid_contest(self, contest_code: int) -> bool:
        '''Returns True if contest exists on codeforces
        '''
        return is_contest_valid(contest_code)

    def is_already_initilized(self):
        '''Checks whether repository already initialized or not
            returns True if already initialized
        '''
        repository_dir = get_repository_path()
        return os.path.exists(repository_dir)

    def create_repository(self):
        '''Creates .cfcli directory to store configurations as well as other files related to problems
        '''
        repository_dir = get_repository_path()
        os.mkdir(repository_dir)

    def create_local_conf_file(self, contest_code: int, language: str, editor: str):
        '''Creates local_conf.json in repository directory
        '''
        conf_file_path = get_local_conf_file_path()
        data = {
            'contestCode': contest_code,
            'language': language,
            'editor': editor
        }

        json.dump(data, open(conf_file_path, 'w'))


helpers = InitHelpers()


@enforce_rules(Rules.REPOSITORY_NOT_INITIALISED)
def initialize(contest_code, language, editor):

    click.echo('Checking contest validity...')
    if not helpers.valid_contest(contest_code):
        raise click.ClickException(f'contest with code {contest_code} doesn\'t exist.')

    helpers.create_repository()
    helpers.create_local_conf_file(contest_code, language, editor)


@enforce_rules(Rules.REPOSITORY_INITIALISED)
def clear_repository():
    repository_dir = get_repository_path()
    os.system(f'rm -rf {repository_dir}')
