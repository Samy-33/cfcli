class Contest:
    def __init__(self, contest_code, is_upcoming, problems={}):
        self._contest_code = contest_code
        self._is_upcoming = is_upcoming
        self._problems = problems

    def get_contest_code(self):
        return self._contest_code

    def add_problem(self, problem_code, problem):
        self._problems.update({problem_code: problem})

    def is_upcoming(self):
        return self._is_upcoming
