import click
import os

from core.api.api import is_contest_valid, get_contest, fetch_problemset
from core.popos.contest import Contest
from utils.constants import REPOSITORY_DIRECTORY_NAME


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
        current_dir = os.getcwd()
        repository_dir = os.path.join(current_dir, REPOSITORY_DIRECTORY_NAME)
        return os.path.exists(repository_dir)

    def create_repository(self):
        '''Creates .cfcli directory to store configurations as well as other files related to problems
        '''
        current_dir = os.getcwd()
        repository_dir = os.path.join(current_dir, REPOSITORY_DIRECTORY_NAME)
        os.mkdir(repository_dir)

    def store_contest_details(self, contest: Contest):
        '''Fetches more data about contests like problems
        '''
        if not contest.is_upcoming():
            self._store_problems_data(contest)
            problemset = fetch_problemset(contest.get_contest_code())


helpers = InitHelpers()


def initialize(contest_code, language, editor):

    if helpers.is_already_initilized():
        click.echo('Repository already initialised!')
        return

    click.echo('Checking contest validity...')
    if not contest_code:
        raise click.BadOptionUsage('code', 'invalid contest code.')

    if not helpers.valid_contest(contest_code):
        raise click.BadOptionUsage('code', f'contest with code {contest_code} doesn\'t exist.')

    # TODO: add functionality

    contest = get_contest(contest_code)
    helpers.store_contest_details(contest)

    # helpers.create_repository()
    repository_info = {}

