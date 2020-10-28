#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The bench_evm bench."""

import logging
import os
import signal
import sys

# pylint: disable=unused-argument

import context # pylint: disable=unused-import
import silkworm

def terminate_process(signal_number: int, frame):
    """ terminate_process """
    print()
    logging.info('%s: signal %d, terminating...', __file__, signal_number)
    sys.exit()

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)-15s %(message)s', level=logging.INFO)

    signal.signal(signal.SIGINT, terminate_process)
    signal.signal(signal.SIGQUIT, terminate_process)

    logging.info('%s: START - PID is %d', __file__, os.getpid())

    txn = silkworm.Transaction(0, 10000, 21000, None, 0, '', 1, 1, 1, None)
    print(txn)

    logging.info('%s: END', __file__)
