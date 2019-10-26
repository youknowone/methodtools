from __future__ import with_statement

import re
from setuptools import setup
import sys


def get_version():
    with open('methodtools.py') as f:
        source = f.read()
    m = re.search(r"__version__ = '([0-9\.]+)'", source)
    version = m.group(1)
    assert version
    return version


install_requires = [
    'wirerope==0.3.1',
]
tests_require = [
    'pytest>=3.0.2', 'pytest-cov',
]
docs_require = [
    'sphinx',
]

# functools32 support
if sys.version_info[0] == 2:
    tests_require.extend([
        'functools32>=3.2.3-2',
    ])

dev_require = tests_require + docs_require


def get_readme():
    try:
        with open('README.rst') as f:
            return f.read().strip()
    except IOError:
        return ''


setup(
    name='methodtools',
    version=get_version(),
    description='Expand standard functools to methods',
    long_description=get_readme(),
    author='Jeong YunWon',
    author_email='methodtools@youknowone.org',
    url='https://github.com/youknowone/methodtools',
    py_modules=['methodtools'],
    packages=(),
    package_data={},
    install_requires=install_requires,
    tests_require=tests_require + ['tox', 'tox-pyenv'],
    extras_require={
        'tests': tests_require,
        'docs': docs_require,
        'dev': dev_require,
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)  # noqa
