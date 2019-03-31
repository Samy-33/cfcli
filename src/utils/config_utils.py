import os

from settings import config  # , logger
from utils.constants import REPOSITORY_DIRECTORY_NAME


def language_supported(language):
    supported_languages = config['languages'].keys()
    return language in supported_languages


def get_repository_path():
    current_dir = os.getcwd()
    repository_dir = os.path.join(current_dir, REPOSITORY_DIRECTORY_NAME)
    # logger.debug(f'Repository Dir --> {repository_dir}')

    return repository_dir


def get_contest_data_dir_path(create_if_doesnt_exist=False):
    repository_dir = get_repository_path()
    contest_data_dir = os.path.join(repository_dir, 'data')

    if create_if_doesnt_exist and not os.path.exists(contest_data_dir):
        os.mkdir(contest_data_dir)

    return contest_data_dir


def get_contest_info_file_path(create_data_dir=False):
    contest_data_dir = get_contest_data_dir_path(create_if_doesnt_exist=create_data_dir)
    contest_data_file_path = os.path.join(contest_data_dir, 'contest.info')

    return contest_data_file_path
