import os
import glob

from setuptools import setup


def find_headers():
    for filename in glob.iglob('include/**/*.h', recursive=True):
        yield os.path.relpath(filename, os.path.dirname(__file__))


setup(
    name='py3c',
    version='1.0a1',
    description='Python compatibility headers',
    author='Petr Viktorin',
    author_email='encukou@gmail.com',
    url='https://github.com/encukou/py3c',
    headers=list(find_headers()),
    platforms='any')
