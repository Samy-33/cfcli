from core.api._cf_scraper import scraper_helpers, fetch_contest_info

def is_contest_valid(contest_code: int) -> bool:
    page = scraper_helpers.get_contest_response(contest_code)
    return scraper_helpers.is_contest_valid(contest_code, page)

def get_contest(contest_code):
    contest = fetch_contest_info(contest_code)
    return contest

def get_problemset(contest_code):
    pass

def fetch_problemset(contest):
    pass