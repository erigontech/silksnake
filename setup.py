# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='silksnake',
    version='0.1.0',
    description='Python library to access turbo-geth/silkworm data remotely',
    long_description=readme,
    author='canepat',
    author_email='tullio.canepa@gmail.com',
    url='https://github.com/torquem-ch/silksnake',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
