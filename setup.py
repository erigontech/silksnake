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

library_dirs=['silkworm/build/', 'silkworm/build/cbor-cpp/','silkworm/build/libff/libff',  'silkworm/build/silkworm/']
library_dirs.extend(glob(path.expanduser('~') + '/.hunter/**/Install/lib', recursive=True))

libraries=[ # order matters!
    #'absl_bad_any_cast_impl',
    #'absl_bad_optional_access',
    #'absl_bad_variant_access',
    #'absl_city',
    #'absl_civil_time',
    #'absl_cord',
    #'absl_examine_stack',
    'absl_failure_signal_handler',
    #'absl_flags',
    #'absl_flags_config',
    #'absl_flags_internal',
    #'absl_flags_marshalling',
    #'absl_flags_parse',
    #'absl_flags_program_name',
    #'absl_flags_registry',
    #'absl_flags_usage',
    #'absl_flags_usage_internal',
    #'absl_graphcycles_internal',
    'absl_hash',
    'absl_hashtablez_sampler',
    #'absl_leak_check',
    #'absl_leak_check_disable',
    #'absl_log_severity',
    #'absl_periodic_sampler',
    #'absl_random_distributions',
    #'absl_random_internal_distribution_test_util',
    #'absl_random_internal_pool_urbg',
    #'absl_random_internal_randen',
    #'absl_random_internal_randen_hwaes',
    #'absl_random_internal_randen_hwaes_impl',
    #'absl_random_internal_randen_slow',
    #'absl_random_internal_seed_material',
    #'absl_random_seed_gen_exception',
    #'absl_random_seed_sequences',
    'absl_raw_hash_set',
    'absl_raw_logging_internal',
    'absl_scoped_set_env',
    'absl_stacktrace',
    #'absl_status',
    #'absl_str_format_internal',
    #'absl_strings',
    #'absl_strings_internal',
    'absl_synchronization',
    #'absl_throw_delegate',
    'absl_time',
    'absl_time_zone',
    'absl_exponential_biased',
    'absl_base',
    'absl_spinlock_wait',
    'absl_symbolize',
    'absl_demangle_internal',
    'absl_debugging_internal',
    'absl_dynamic_annotations',
    'absl_malloc_internal',
    'absl_int128',
    #'benchmark',
    #'benchmark_main',
    'boost_filesystem-mt-x64',
    'cborcpp',
    'cryptopp',
    'ethash',
    'evmone',
    'ff',
    'keccak',
    'lmdb',
    'secp256k1',
    'silkworm'
]

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
            sources=sorted(glob('silksnake/bindings/*.cpp')), # Sorted source files for build reproducibility
            include_dirs=include_dirs,
            library_dirs=library_dirs,
            libraries=libraries,
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
