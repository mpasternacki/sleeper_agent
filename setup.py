from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages, Extension

setup(
    name = 'sleeper_agent',
    version = '0.0.1',
    description = 'Entry points for live state inspection',
    author = 'Maciej Pasternacki',
    author_email = 'maciej@pasternacki.net',
    license = 'BSD 3 Clause License',
    url = 'https://github.com/mpasternacki/sleeper_agent',
    py_modules = [ 'sleeper_agent' ],
    ext_modules = [ Extension('_sleeper_agent_activation',
                              sources = ['_sleeper_agent_activation.c']) ],
    tests_require = 'nose',
    )
