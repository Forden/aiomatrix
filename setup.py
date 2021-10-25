#!/usr/bin/env python3
import pathlib
import re
import sys

from setuptools import find_packages, setup

WORK_DIR = pathlib.Path(__file__).parent

# Check python version
MINIMAL_PY_VERSION = (3, 7)
if sys.version_info < MINIMAL_PY_VERSION:
    raise RuntimeError('aiomatrix works only with Python {}+'.format('.'.join(map(str, MINIMAL_PY_VERSION))))


def get_version():
    """
    Read version
    :return: str
    """
    txt = (WORK_DIR / 'aiomatrix' / '__init__.py').read_text('utf-8')
    try:
        return re.findall(r"^__version__ = '([^']+)'\r?$", txt, re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


def get_description():
    with open('README.rst', 'r', encoding='utf-8') as f:
        return f.read()


setup(
    name='aiomatrix-py',
    version=get_version(),
    packages=find_packages(exclude=('tests', 'tests.*', 'docs', 'examples.*')),
    url='https://github.com/Forden/aiomatrix',
    license='MIT',
    author='Forden',
    python_requires='>=3.7',
    description='Aiomatrix is a simple library for Matrix Client-Server API',
    long_description=get_description(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Programming Language :: Python',
        'Framework :: AsyncIO',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
        'aiohttp>=3.7.2,<4.0.0',
        'pydantic==1.8.2'
    ],
    include_package_data=False,
)
