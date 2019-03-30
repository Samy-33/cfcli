from settings import config


def language_supported(language):
    supported_languages = config['languages'].keys()
    return language in supported_languages