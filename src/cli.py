import click
import requests as rq
from helpers import helper

class Context:
	def __init__(self):
		pass

@click.group()
def cli():
	pass

@cli.command()
@click.option('--url', default=None, help='URL of the problem')
@click.option('--contest-code', help='Contest Code')
@click.option('--problem-code', help='Problem Code')
def download_tests(url, contest_code, problem_code):
	
	if url:
		helper.download_tests_from_url(url)

	else:
		helper.download_tests_from_code(contest_code, problem_code)


@cli.command()
@click.option('--contest-code', required=True, help='Contest Code')
@click.option('--problem-code', required=True, help='Problem Code')
@click.argument('exe')
def test(contest_code, problem_code, exe):
	
	helper.test(contest_code, problem_code, exe)