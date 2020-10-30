#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Setup the project dependencies."""

from glob import glob
from os import path
from setuptools import setup, find_packages

# pylint: disable=ungrouped-imports

# With setup_requires, this runs twice - once without setup_requires, and once
# with. The build only happens the second time.
try:
    from pybind11.setup_helpers import Pybind11Extension, build_ext
except ImportError:
    from setuptools import Extension as Pybind11Extension
    from setuptools.command.build_ext import build_ext

__version__ = '0.0.1'

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license_text = f.read()

include_dirs = ['silkworm', 'silkworm/evmone/evmc/include']
include_dirs.extend(glob(path.expanduser('~') + '/.hunter/**/Install/include', recursive=True))

sources = [
    #'silkworm/silkworm/execution/processor.cpp',
    #'silkworm/silkworm/state/intra_block_state.cpp',
]
sources.extend(glob('silksnake/bindings/*.cpp'))

library_dirs=['silkworm/build/', 'silkworm/build/cbor-cpp/','silkworm/build/libff/libff',  'silkworm/build/silkworm/']
library_dirs.extend(glob(path.expanduser('~') + '/.hunter/**/Install/lib', recursive=True))

setup(
    name='silksnake',
    version=__version__,
    description='Python library to access turbo-geth/silkworm data remotely',
    long_description=readme,
    author='canepat',
    author_email='',
    url='https://github.com/torquem-ch/silksnake',
    license=license_text,
    packages=find_packages(exclude=('tests', 'docs')),
    ext_modules=[
        Pybind11Extension(
            'silkworm',
            sources=sorted(sources), # Sorted source files for build reproducibility
            include_dirs=include_dirs,
            library_dirs=library_dirs,
            libraries=['cborcpp', 'cryptopp', 'evmone', 'ff', 'secp256k1', 'silkworm'],
            define_macros=[
                ('VERSION_INFO', __version__)
            ],
        )
    ],
    setup_requires=[
        'cbor2 >= 5.2.0',
        'eth-hash[pycryptodome] >= 0.2.0',
        'grpcio >= 1.33.1',
        'requests >= 2.24.0',
        'rlp >= 2.0.0',
    ],
    cmdclass={"build_ext": build_ext},
)
