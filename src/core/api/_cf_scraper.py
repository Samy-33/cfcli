import requests as rq
from bs4 import BeautifulSoup as bs
from exceptions import InvalidContestException


CONTEST_URL_STRING = 'https://codeforces.com/contests/{contest_code}'


class Helpers:
    
    @staticmethod
    def is_upcoming_contest(html: str) -> bool:
        return not 'class="problems"' in html


def parse_contest_page(contest_code: int) -> dict:
    contest_url = CONTEST_URL_STRING.format(contest_code)
    page = rq.get(contest_url)

    if page.url != contest_url:
        raise InvalidContestException

    contest_data = {}

    contest_data['is_upcoming'] = Helpers.is_upcoming_contest(page.text)

    #TODO: Parse whole data

    return contest_data

