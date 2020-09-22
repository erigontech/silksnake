# -*- coding: utf-8 -*-
"""Setup the project dependencies."""

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license_text = f.read()

setup(
    name='silksnake',
    version='0.0.1',
    description='Python library to access turbo-geth/silkworm data remotely',
    long_description=readme,
    author='canepat',
    author_email='',
    url='https://github.com/torquem-ch/silksnake',
    license=license_text,
    packages=find_packages(exclude=('tests', 'docs'))
)
