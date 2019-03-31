import os
import pickle

import click

from core.api.api import get_contest, is_contest_valid  # , fetch_problemset
from core.popos.contest import Contest
from utils.config_utils import get_contest_info_file_path, get_repository_path
from utils.decorators import Rules, enforce_rules


class InitHelpers:
    '''Helper methods for handling initialization of cfcli repository
    '''

    def valid_contest(self, contest_code: int) -> bool:
        '''Returns True if contest exists on codeforces
        '''
        return is_contest_valid(contest_code)

    def _store_problems_data(self, contest):
        '''Fetches and stores problems data like, time-limit, memory-limit, sample-test-cases
        '''
        pass

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

    def store_contest_details(self, contest: Contest):
        '''Fetches more data about contests like problems
        '''
        if not contest.is_upcoming():
            self._store_problems_data(contest)
            # problemset = fetch_problemset(contest.get_contest_code())

        contest_data_file_path = get_contest_info_file_path(create_data_dir=True)

        pickle.dump(contest, open(contest_data_file_path, 'wb'))


helpers = InitHelpers()


@enforce_rules(Rules.REPOSITORY_NOT_INITIALISED)
def initialize(contest_code, language, editor):

    if helpers.is_already_initilized():
        click.echo('Repository already initialised!')
        return

    click.echo('Checking contest validity...')
    if not helpers.valid_contest(contest_code):
        raise click.BadOptionUsage('code', f'contest with code {contest_code} doesn\'t exist.')

    # TODO: add functionality

    contest = get_contest(contest_code)

    helpers.create_repository()
    helpers.store_contest_details(contest)
    # repository_info = {}


@enforce_rules(Rules.REPOSITORY_INITIALISED)
def clear_repository():
    repository_dir = get_repository_path()
    os.system(f'rm -rf {repository_dir}')
