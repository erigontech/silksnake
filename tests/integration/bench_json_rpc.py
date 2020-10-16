#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The bench_json_rpc bench."""

import argparse
import logging
import os
import signal
import sys

import requests

import context # pylint: disable=unused-import

from silksnake.api import eth
from silksnake.remote.kv_remote import DEFAULT_TARGET

def terminate_process(signal_number: int, frame): # pylint: disable=unused-argument
    """ terminate_process """
    print()
    logging.info('%s: signal %d, terminating...', __file__, signal_number)
    sys.exit()

def json_rpc_get_storage_at(cmp_node_url: str, address_hex: str, location: int, block_number: int):
    """ request_eth_getStorageAt """
    response = requests.post(cmp_node_url, json={
        'json': '2.0',
        'method': 'eth_getStorageAt',
        'params': ['0x' + address_hex, hex(location), hex(block_number)],
        'id': 1
    })
    assert response.status_code == requests.codes['ok']
    return response.json()['result']

def bench_json_rpc(from_block_number: int, target: str = DEFAULT_TARGET, cmp_node_url: str = None):
    """ bench_json_rpc """
    eth_api = eth.EthereumAPI(target)
    latest_block_number = eth_api.block_number()

    logging.info('Working set is from_block_number: %d to latest_block_number: %d', from_block_number, latest_block_number)

    # Just an example to be moved in for loop
    storage_at = eth_api.get_storage_at('0x33ee33fc3e1aacdb75a1ad362489ac54f02d6d63', '0x00', '2000001')
    logging.info('TG API: storage at location 0x00 for 0x33ee...6d63 in block 2000001: %s', storage_at)

    if cmp_node_url is not None:
        result = json_rpc_get_storage_at(cmp_node_url, '33ee33fc3e1aacdb75a1ad362489ac54f02d6d63', 0, 2000001)
        logging.info('JSON RPC API: storage at location 0x00 for 0x33ee...6d63 in block 2000001: %s', result)
        assert result == storage_at

    storage_count = 0
    for _, block_number in enumerate(range(from_block_number, latest_block_number)):
        block = eth_api.get_block_by_number(block_number)
        print(f'\nblock_number: {block_number} #transaction: {len(block.body.transactions)}')
        for index, transaction in enumerate(block.body.transactions, 1):
            if transaction.to.hex() and transaction.gas_limit > 21000:
                storage_count += 1
                if storage_count % 10 == 0:
                    print(f'#{index:0{2}} to: {transaction.to.hex()}')
                    storage_count = 0
                    result = json_rpc_get_storage_at(cmp_node_url, transaction.to.hex(), 18, 2000001)
                    print(result)

    print()

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)-15s %(message)s', level=logging.INFO)

    signal.signal(signal.SIGINT, terminate_process)
    signal.signal(signal.SIGQUIT, terminate_process)

    logging.info('%s: START - PID is %d', __file__, os.getpid())

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('from_block_number', help='the start block number as integer')
    parser.add_argument('-t', '--target', default='localhost:9090', help='the Turbo node location as string <address>:<port>')
    parser.add_argument('-u', '--url', help='the Ethereum node location to compare as URL string or null if no compare')
    args = parser.parse_args()

    bench_json_rpc(int(args.from_block_number), args.target, args.url)

    logging.info('%s: END', __file__)
