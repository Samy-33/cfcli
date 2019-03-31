import os

import click
import requests as rq
from bs4 import BeautifulSoup
# from settings import logger
from terminaltables import AsciiTable

from core.popos.contest import Contest
from core.popos.problem import Problem
from utils.constants import (ALL_CONTSET_URL, CODEFORCES_HOST,
                             CONTEST_URL_STRING)


class ScraperHelpers:

    def is_upcoming_contest(self, html: str) -> bool:
        '''Tells whether contest is upcoming or not
            Uses the fact that if problems are visible then it's not upcoming
        '''
        return 'class="problems"' not in html

    def get_contest_response(self, contest_code: int) -> rq.Response:
        contest_url = CONTEST_URL_STRING.format(contest_code=contest_code)
        return rq.get(contest_url)

    def is_contest_valid(self, http_response: rq.Response) -> bool:
        return http_response.url != ALL_CONTSET_URL


class ParserHelpers:

    def _parse_line_breaks_in_dom_elem(self, element: BeautifulSoup) -> str:
        '''Converts a dome element of type BeautifulSoup into a string replacing line breaks to \n
        '''
        element = element.decode_contents()
        parsed_string = str(element).replace('<br/>', '\n').replace('<br>', '\n')
        return parsed_string

    def _split_text_and_strip(self, element: BeautifulSoup, delimiter: str) -> list:
        splitted = element.text.strip().split(delimiter)
        splitted = list(x.strip() for x in splitted if x.strip() != '')

        return splitted

    def parse_problems(self, contest_soup: BeautifulSoup) -> dict:
        '''parses the problems list and returns a dictionary mapping from problem_code to its url
        '''
        problems = {}
        problems_table = contest_soup.find('table', {'class': 'problems'})
        table_rows = problems_table.find_all('tr')

        # First Row is the header, ignore it
        if len(table_rows) > 1:
            table_rows = table_rows[1:]

        for row in table_rows:
            problem_info_cols = row.find_all('td')
            problem_code = problem_info_cols[0].text.strip()
            problem_url = problem_info_cols[1].a['href'][1:]
            problem_url = os.path.join(CODEFORCES_HOST, problem_url)

            splitted_second_col = self._split_text_and_strip(problem_info_cols[1], '\n')
            problem_name = splitted_second_col[0]
            time_limit, memory_limit = list(x.strip() for x in splitted_second_col[2].split(','))
            submissions = int(problem_info_cols[3].text.strip()[1:])

            problem = Problem(problem_code, problem_name, problem_url, time_limit,
                              memory_limit, correct_submissions=submissions)

            problems[problem.get_code()] = problem

        return problems

    def print_problems(self, problems: dict):
        table_data = [['Code', 'Name', 'Correct Submissions']]

        for _, problem in problems.items():
            table_data.append([problem.get_code(), problem.get_name(),
                              problem.get_correct_submissions()])

        table = AsciiTable(table_data)
        click.echo(table.table)


scraper_helpers = ScraperHelpers()
parser_helpers = ParserHelpers()


def fetch_contest_info(contest_code: int) -> Contest:
    page = scraper_helpers.get_contest_response(contest_code)

    if not scraper_helpers.is_contest_valid(page):
        raise click.BadOptionUsage('code', 'Contest doesn\'t exist.')

    is_upcoming = scraper_helpers.is_upcoming_contest(page.text)
    contest = Contest(contest_code, is_upcoming)

    if not is_upcoming:
        click.echo('Extracting Problems from page...')
        bsoup = BeautifulSoup(page.text, 'html.parser')
        problems = parser_helpers.parse_problems(bsoup)

        for problem_code, problem in problems.items():
            contest.add_problem(problem_code, problem)

        click.echo(f'Extracted {len(problems)} problems')
        response = input('Display problems list? [y/n] ')

        if response in ['y', 'Y']:
            parser_helpers.print_problems(problems)
    else:
        click.echo('Contest is yet to start.')
    return contest
