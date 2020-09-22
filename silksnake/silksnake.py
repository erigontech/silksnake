#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The silksnake main."""

__version__ = "0.0.1"

import argparse
import logging

from .remote.kv_remote import RemoteClient # pylint: disable=unused-import

# Processing command line arguments
parser = argparse.ArgumentParser()

# Options
parser.add_argument('-l', '--log', help='activate logging', dest='log', action='store_true')

args = parser.parse_args()

if args.log:
    logging.basicConfig()

if __name__ == '__main__':
    logging.info('Welcome in silksnake!')
