import click
from requests.exceptions import ConnectionError

from core.init import clear_repository, initialize
# from settings import logger
from utils.constants import DEFAULT_EDITOR, DEFAULT_LANGUAGE


@click.group()
def cli():
    pass


@cli.command()
@click.option('-cc', '--contest-code', required=True, type=click.INT, help='Contest Code')
@click.option('-l', '--language', default=DEFAULT_LANGUAGE, type=click.STRING,
              help='Preferred Language')
@click.option('-e', '--editor', default=DEFAULT_EDITOR, type=click.STRING, help='Preferred Editor')
def init(contest_code, language, editor):

    try:
        initialize(contest_code, language, editor)
    except ConnectionError:
        raise click.ClickException(f'Connection Error. Check your network connectivity.')
    except click.ClickException as e:
        raise e
    except Exception as e:
        # clear_repository()
        raise click.ClickException(f'System Error Occured\nMessage: {e}')


@cli.command()
def clean():
    try:
        clear_repository()
    except click.ClickException as e:
        raise e
    except Exception as e:
        raise click.ClickException(f'System Error Occured\nMessage: {e}')


# @cli.command()
# def testing():

# 	from utils.decorators import Rules, enforce_rules

# 	@enforce_rules(Rules.UPCOMING_CONTEST)
# 	def temporary():
# 		pass
# 	temporary()
