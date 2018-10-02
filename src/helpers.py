import requests as rq
from bs4 import BeautifulSoup as bs
import os
import json


PROBLEM_URL = 'http://codeforces.com/contest/{contest_code}/problem/{problem_code}'
CONF_FILE_NAME = 'conf.json'
NO_OF_TESTS_KEY = 'number_of_tests'

# def download_problem_tests(contest, problem):
# 	url = PROBLEM_URL.format(contest_code=contest, problem_code=problem)
# 	print(url)

def get_contest_code_from_url(url):
	url = url.split('/')

	if len(url) < 5:
		raise Exception('URL NOT VALID')

	return url[4]

def get_problem_code_from_url(url):
	url = url.split('/')

	if len(url) < 7:
		raise Exception('URL NOT VALID')

	return url[6]


def get_directory_from_codes(contest, problem):
	return '{}/{}'.format(contest, problem)


class CodeforcesCLI:
	def __init__(self):
		pass

	def download_tests_from_url(self, url):

		problem_code = get_problem_code_from_url(url)
		contest_code = get_contest_code_from_url(url)

		resp = rq.get(url).text
		soup = bs(resp, 'html.parser')

		title = soup.find(class_='title')

		if not title:
			print(f'No problem found')
			return

		test_wrapper = soup.find(class_='sample-test')

		inputs = test_wrapper.find_all(class_='input')
		outputs = test_wrapper.find_all(class_='output')

		directory = get_directory_from_codes(contest_code, problem_code)

		if not os.path.exists(directory):
			os.makedirs(directory)

		conf_data = {
			NO_OF_TESTS_KEY: len(inputs)
		}

		config_file = os.path.join(directory, CONF_FILE_NAME)

		with open(config_file, 'w') as f:
			json.dump(conf_data, f)

		for _ in range(0, len(inputs)):
			t_input = inputs[_]
			t_output = outputs[_]

			input_file_name = os.path.join(directory, 'in{}'.format(_))
			output_file_name = os.path.join(directory, 'out{}'.format(_))

			with open(input_file_name, 'w') as f:
				f.write(t_input.pre.get_text('\n'))

			with open(output_file_name, 'w') as f:
				f.write(t_output.pre.get_text('\n'))


	def download_tests_from_code(self, contest, problem):
		url = PROBLEM_URL.format(contest_code=contest, problem_code=problem)
		download_tests_from_url(url)

	def test(self, contest, problem, exe):
		directory = get_directory_from_codes(contest, problem)

		if not os.path.exists(directory):
			print('Tests don\'t exist. Download first.')
			return

		conf_data = None

		conf_file = os.path.join(directory, CONF_FILE_NAME)

		with open(conf_file, 'r') as f:
			conf_data = json.load(f)

		if not conf_data:
			print('configuration not valid or doesn\'t exist.')
			return

		for _ in range(conf_data[NO_OF_TESTS_KEY]):
			input_file_name = os.path.join(directory, f'in{_}')
			output_file_name = os.path.join(directory, f'out{_}')

			os.system(f'./{exe} < {input_file_name} > temp_out')

			with open('temp_out', 'r') as f_temp, open(output_file_name, 'r') as f_exp:
				for x, y in zip(f_temp, f_exp):
					x = x.strip()
					y = y.strip()

					if x != y:
						print(f'Error Occured at test {_+1}')
						return

			print(f'Test {_+1} passed.')


helper = CodeforcesCLI()