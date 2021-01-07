import os
import glob

from setuptools import setup


def find_headers():
    path = os.path.join(os.path.dirname(__file__), 'include')
    for root, dirs, files in os.walk(path):
        for filename in files:
            if filename.endswith('.h'):
                yield os.path.join(root, filename)

# Static information is in setup.cfg.
setup(headers=list(find_headers()))
