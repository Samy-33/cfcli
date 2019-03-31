from setuptools import setup

setup(
    name='CodeForces-CLI',
    version='0.0.1',
    py_modules=['cli'],
    install_requires=[
        'Click',
        'requests',
        'bs4'
    ],
    entry_points='''
        [console_scripts]
        cfcli=cli:cli
    '''
)
