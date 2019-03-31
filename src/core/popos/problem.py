class Problem:
    def __init__(self, code: int, name: str, url: str, time_limit: str, memory_limit: str,
                 test_cases: list = [], correct_submissions: int = 0):

        self._code = code
        self._name = name
        self._url = url
        self._time_limit = time_limit
        self._memory_limit = memory_limit
        self._test_cases = test_cases
        self._correct_submissions = correct_submissions

    def get_code(self):
        return self._code

    def get_name(self):
        return self._name

    def get_url(self):
        return self._url

    def get_time_limit(self):
        return self._time_limit

    def get_memory_limit(self):
        return self._memory_limit

    def get_test_cases(self):
        return self._test_cases

    def get_correct_submissions(self):
        return self._correct_submissions

    def add_test_case(self, input_file_path: str, output_file_path: str):
        self._test_cases.append((input_file_path, output_file_path))

    def __str__(self):
        return f'{self._code}: {self._name} @ {self._url}'
