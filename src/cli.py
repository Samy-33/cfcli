import click
import os

from core.init import initialize
from requests.exceptions import ConnectionError
from settings import logger
from utils.constants import DEFAULT_LANGUAGE, DEFAULT_EDITOR


@click.group()
def cli():
	pass


@cli.command()
@click.option('-c', '--code', type=click.INT, help='Contest Code')
@click.option('-l', '--language', default=DEFAULT_LANGUAGE, help='Preferred Language')
@click.option('-e', '--editor', default=DEFAULT_EDITOR, help='Preferred Editor')
def init(code, language, editor):
	
	try:
		initialize(code, language, editor)
	except ConnectionError as e:
		raise click.ClickException(f'Connection Error. Check your network connectivity.')
