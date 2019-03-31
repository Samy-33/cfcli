from core.api.api import fetch_problem_sample_tests, get_contest
from core.popos.contest import Contest
from utils.config_utils import (dump_contest_object, dump_test_data,
                                get_set_contest_code)
from utils.decorators import Rules, enforce_rules


class FetchHelpers:

    def _get_name_for_test_file(self, problem_code: str, file_type: str, index: int) -> str:
        '''creates a prefix for test file basis of problem_code and file_type (input or output)
        '''
        return '{}_{}_{}.txt'.format(problem_code, file_type, index)

    def store_problems_sample_tests(self, contest):
        '''Fetches and stores problems data like, time-limit, memory-limit, sample-test-cases
        '''
        for problem_code, problem in contest.get_problems().items():
            sample_tests = fetch_problem_sample_tests(problem.get_url())

            for index, test in enumerate(sample_tests):
                input_name = self._get_name_for_test_file(problem.get_code(), 'input', index)
                output_name = self._get_name_for_test_file(problem.get_code(), 'output', index)

                dump_test_data(input_name, test['input'])
                dump_test_data(output_name, test['output'])

    def store_contest_details(self, contest: Contest):
        '''Fetches more data about contests like problems
        '''
        dump_contest_object(contest, create_data_dir=True)


fetch_helpers = FetchHelpers()


@enforce_rules(Rules.NOT_FETCHED_CONTENT)
def fetch_contest_data(fetch_samples=False):
    contest_code = get_set_contest_code()
    contest = get_contest(contest_code)

    fetch_helpers.store_contest_details(contest)
    if not contest.is_upcoming() and fetch_samples:
        fetch_helpers.store_problems_sample_tests(contest)
