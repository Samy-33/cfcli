import click
from requests.exceptions import ConnectionError

import settings
from core.fetch import fetch_contest_data, refresh_contest_data
from core.init import clear_repository, initialize
from utils.config_utils import (get_supported_editors_list,
                                get_supported_languages_list)
from utils.constants import DEFAULT_EDITOR, DEFAULT_LANGUAGE


@click.group()
def cli():
    pass


@cli.command()
@click.option('-cc', '--contest-code', required=True, type=click.INT, help='Contest Code')
@click.option('-l', '--language', default=DEFAULT_LANGUAGE,
              type=click.Choice(get_supported_languages_list()), help='Preferred Language')
@click.option('-e', '--editor', default=DEFAULT_EDITOR,
              type=click.Choice(get_supported_editors_list()), help='Preferred Editor')
def init(contest_code, language, editor):

    try:
        initialize(contest_code, language, editor)
    except ConnectionError:
        raise click.ClickException(f'Connection Error. Check your network connectivity.')
    except click.ClickException as e:
        raise e
    except Exception as e:
        # clear_repository()
        if settings.DEBUG:
            raise e
        raise click.ClickException(f'System Error Occured\nMessage: {e}')


@cli.command()
def clean():
    try:
        clear_repository()
    except click.ClickException as e:
        raise e
    except Exception as e:
        if settings.DEBUG:
            raise e
        raise click.ClickException(f'System Error Occured\nMessage: {e}')


@cli.command()
@click.option('-s', '--with-samples', 'fetch_samples', is_flag=True,
              help='Fetch Samples testcases too.')
def fetch(fetch_samples):
    try:
        fetch_contest_data(fetch_samples=fetch_samples)
    except click.ClickException as e:
        raise e
    except Exception as e:
        if settings.DEBUG:
            raise e
        raise click.ClickException(f'System Error Occerred\nMessage: {e}')


@cli.command()
@click.option('-s', '--with-samples', 'refresh_samples', is_flag=True,
              help='Refresh Sample testcases too.')
def refresh(refresh_samples):
    try:
        refresh_contest_data(refresh_samples=refresh_samples)
    except click.ClickException as e:
        raise e
    except Exception as e:
        if settings.DEBUG:
            raise e
        raise click.ClickException(f'System Error Occerred\nMessage: {e}')
