import json
import os
import pickle

from settings import config  # , logger
from utils.constants import LOCAL_CONF_FILE_NAME, REPOSITORY_DIRECTORY_NAME


# Global Config
def get_supported_languages_list():
    '''Returns a list of all the supported programming languages
    '''
    return config['languages'].keys()


def get_supported_editors_list():
    '''Returns a list of all the supported text editors
    '''
    return config['editors'].keys()


def language_supported(language):
    '''Returns True if a particular language is supported else False
    '''
    supported_languages = get_supported_languages_list()
    return language in supported_languages


# Local Config
def get_repository_path():
    '''Returns repository dir absolute path /<some-path>/.cfcli
    '''
    current_dir = os.getcwd()
    repository_dir = os.path.join(current_dir, REPOSITORY_DIRECTORY_NAME)

    return repository_dir


def get_local_conf_file_path():
    '''Returns absolute path of local_conf.json file: /<some-path>/.cfcli/local_conf.json
    '''
    repository_dir = get_repository_path()
    return os.path.join(repository_dir, LOCAL_CONF_FILE_NAME)


def get_contest_data_dir_path(create_if_doesnt_exist=False):
    '''Returns absolute path of directory containing data for set contest
    '''
    repository_dir = get_repository_path()
    contest_data_dir = os.path.join(repository_dir, 'data')

    if create_if_doesnt_exist and not os.path.exists(contest_data_dir):
        os.mkdir(contest_data_dir)

    return contest_data_dir


def get_contest_info_file_path(create_data_dir=False):
    '''Returns absolute path of .info file which contains serialized contest object
    '''
    contest_data_dir = get_contest_data_dir_path(create_if_doesnt_exist=create_data_dir)
    contest_data_file_path = os.path.join(contest_data_dir, 'contest.info')

    return contest_data_file_path


def get_local_config():
    '''parses local_conf.json file and returns a dictionary
    '''
    return json.load(open(get_local_conf_file_path(), 'r'))


def get_set_contest_code():
    local_config = get_local_config()
    return local_config['contestCode']


def get_set_language():
    local_config = get_local_config()
    return local_config['language']


def get_set_editor():
    local_config = get_local_config()
    return local_config['editor']


def dump_contest_object(contest, create_data_dir=False):
    '''serializes contest object and dumps it into the .info file
    '''
    contest_info_file_path = get_contest_info_file_path(create_data_dir=create_data_dir)
    pickle.dump(contest, open(contest_info_file_path, 'wb'))


def dump_test_data(name: str, value: str) -> str:
    '''Creates file with name 'name'
        and returns the absolute path of this file
    '''
    contest_data_dir = get_contest_data_dir_path()
    test_file_name = os.path.join(contest_data_dir, name)

    with open(test_file_name, 'w') as f:
        f.write(value)

    return test_file_name
