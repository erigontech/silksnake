#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The bench_simple_monitor bench."""

import logging
import os
import signal
import sys
import time

import context # pylint: disable=unused-import

from silksnake.api import local

def terminate_process(signal_number: int, frame): # pylint: disable=unused-argument
    """ terminate_process """
    print()
    logging.info('%s: signal %d, terminating...', __file__, signal_number)
    sys.exit()

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)-15s %(message)s', level=logging.INFO)

    signal.signal(signal.SIGINT, terminate_process)
    signal.signal(signal.SIGQUIT, terminate_process)

    logging.info('%s: PID is %d', __file__, os.getpid())

    while True:
        syncing = local.eth_syncing()
        if syncing:
            highest_block, current_block = syncing
            logging.info('syncing: SYNCING [%s / %s]', current_block, highest_block)
        else:
            logging.info('syncing: SYNCED')
        latest_block_number = local.eth_blockNumber()
        logging.info('latest block: %d', latest_block_number)
        latest_block1 = local.eth_getBlockByNumber(latest_block_number)
        logging.info('latest block by number: %s', latest_block1 if latest_block1 else 'NOT AVAILABLE')
        if latest_block1:
            latest_block2 = local.eth_getBlockByHash(latest_block1.header.hash)
            logging.info('latest block by hash: %s', latest_block2)
        eth_supply = local.turbo_getSupply(latest_block_number)
        logging.info('latest ETH supply: %s', 'NOT YET AVAILABLE' if eth_supply < 0 else str(eth_supply))
        logging.info('waiting 5 sec...')
        time.sleep(5)
