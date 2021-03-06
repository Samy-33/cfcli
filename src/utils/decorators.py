import os
import pickle

import click

from settings import logger
from utils.config_utils import get_contest_info_file_path, get_repository_path


class Rules:
    REPOSITORY_INITIALISED = 'repository_initialised'
    REPOSITORY_NOT_INITIALISED = 'repository_not_initialised'
    UPCOMING_CONTEST = 'upcoming_contest'
    NOT_UPCOMING_CONTEST = 'not_upcoming_contest'
    FETCHED_CONTENT = 'fetched_content'
    NOT_FETCHED_CONTENT = 'not_fetched_content'


class Enforcer:

    class MetaMethods:

        @staticmethod
        def is_repository_initialised():
            repository_path = get_repository_path()
            return os.path.exists(repository_path)

        @staticmethod
        def fetched_content():
            if not Enforcer.MetaMethods.is_repository_initialised():
                raise click.ClickException(
                    'You must use init command to initialize the repo before using this command'
                )

            return os.path.exists(get_contest_info_file_path())

        @staticmethod
        def is_upcoming_contest():
            try:
                data_file = open(get_contest_info_file_path(), 'rb')
                contest = pickle.load(data_file)

                return contest.is_upcoming()

            except FileNotFoundError:
                raise click.ClickException(
                    'Repository already exists in this directory.')

            except Exception as e:
                logger.debug(f'{e}')
                raise click.ClickException('System Error Occured! Please Report.')

    def repository_initialised(self):
        initd = self.MetaMethods.is_repository_initialised()

        if not initd:
            raise click.ClickException(
                'You must use init command to initialize the repo before using this command'
            )

        return initd

    def repository_not_initialised(self):
        already_initd = self.MetaMethods.is_repository_initialised()
        if already_initd:
            raise click.ClickException('Repository already exists in this directory.')

        return not already_initd

    def upcoming_contest(self):
        upcoming = self.MetaMethods.is_upcoming_contest()

        if not upcoming:
            raise click.ClickException('Contest set must be upcoming. Found: not upcoming')

        return upcoming

    def not_upcoming_contest(self):

        upcoming = self.MetaMethods.is_upcoming_contest()

        if upcoming:
            raise click.ClickException('Contest set must be ongoing or past. Found, upcoming')

        return not upcoming

    def fetched_content(self):
        fetched = self.MetaMethods.fetched_content()

        if not fetched:
            raise click.ClickException('Contest must be fetched before using this command. \
                                       Use fetch contest command')

        return fetched

    def not_fetched_content(self):
        fetched = self.MetaMethods.fetched_content()

        if fetched:
            raise click.ClickException('Contest already fetched. \
                                        Use refresh to refresh the contest data.')

        return not fetched


enforcer = Enforcer()


def enforce_rules(*rules):
    '''Enforces rules given in Rules
    '''
    def wrapper(f):
        def wrapped_f(*args, **kwargs):
            for rule in rules:
                try:
                    is_valid = getattr(enforcer, rule)
                    if callable(is_valid) and is_valid():
                        return f(*args, **kwargs)

                except AttributeError as ae:
                    logger.debug(f'{ae}')
                    raise click.ClickException(f'System Error Occured, please report.')

        return wrapped_f
    return wrapper
