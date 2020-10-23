#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The bench_json_rpc bench."""

import argparse
import logging
import os
import signal
import sys
from typing import Dict

import requests

import context # pylint: disable=unused-import

from silksnake.api import eth
from silksnake.helpers import hashing
from silksnake.remote.kv_remote import DEFAULT_TARGET
from silksnake.types import LATEST_BLOCK_NUMBER

# pylint: disable=unused-argument,too-many-return-statements,too-many-locals,too-many-nested-blocks,line-too-long

def terminate_process(signal_number: int, frame):
    """ terminate_process """
    print()
    logging.info('%s: signal %d, terminating...', __file__, signal_number)
    sys.exit()

def json_rpc_get_storage_at(node_url: str, address_hex: str, location: int, block_number: int):
    """ request_eth_getStorageAt """
    response = requests.post(node_url, json={
        'json': '2.0',
        'method': 'eth_getStorageAt',
        'params': ['0x' + address_hex, hex(location), hex(block_number)],
        'id': 1
    })
    assert response.status_code == requests.codes['ok']
    response_msg = response.json()
    if 'error' in response_msg:
        raise RuntimeError(response_msg['error'])
    return response_msg['result']

def json_rpc_storage_range_at(node_url: str, block_hash: str, tx_index: int, address: str, start_key: str, limit: int, req_id: int):
    """ request_eth_getStorageAt """
    response = requests.post(node_url, json={
        'json': '2.0',
        'method': 'debug_storageRangeAt',
        'params': ['0x' + block_hash, tx_index, '0x' + address, start_key, limit],
        'id': req_id
    })
    assert response.status_code == requests.codes['ok']
    response_msg = response.json()
    if 'error' in response_msg:
        raise RuntimeError(response_msg['error'])
    return response_msg['result']

def compare_storage_ranges(json_state_map: Dict[str, Dict[str, str]], silksnake_state_map: Dict[str, Dict[str, str]]) -> bool:
    """ compare_storage_ranges """
    if len(json_state_map) != len(silksnake_state_map):
        logging.error('Map size mismatch: json_state_map %d silksnake_state_map %d', len(json_state_map), len(silksnake_state_map))
        return False
    for hashed_key1, entry1 in json_state_map.items():
        if not hashed_key1 in silksnake_state_map:
            logging.error('Hashed key %s not present in silksnake_state_map', hashed_key1)
            return False
        key1 = entry1['key']
        if key1 is None:
            logging.error('Key null for hashed key %s', hashed_key1)
            return False
        if hashed_key1 != hashing.hex_to_hash_str(key1):
            logging.error('Hashed key %s does not match key %s', hashed_key1, key1)
            return False
        entry2 = silksnake_state_map[hashed_key1]
        if entry1['value'] != entry2['value']:
            logging.error('Different value for %s [%s]: %s %s', hashed_key1, key1, entry1['value'], entry2['value'])
            return False
    for hashed_key2, entry2 in silksnake_state_map.items():
        if not hashed_key2 in json_state_map:
            logging.error('Hashed key %s not present in json_state_map', hashed_key2)
            return False
        key2 = entry2['key']
        if hashed_key2 != hashing.hex_to_hash_str(key2):
            logging.error('Hashed key %s does not match key %s', hashed_key2, key2)
            return False
    return True

def print_storage_ranges(json_state_map: Dict[str, Dict[str, str]], silksnake_state_map: Dict[str, Dict[str, str]]) -> bool:
    """ print_storage_ranges """
    print('json_state_map dump:')
    for key, entry in json_state_map.items():
        print(f'{key}: {entry}')
    print('silksnake_state_map dump:')
    for key, entry in silksnake_state_map.items():
        print(f'{key}: {entry}')

def bench_json_rpc(block_number_from: int, block_number_to: int, target: str = DEFAULT_TARGET, cmp_node_url: str = None):
    """ bench_json_rpc """
    assert block_number_from <= block_number_to, f'{block_number_from} greater than {block_number_to}'

    eth_api = eth.EthereumAPI(target)

    if block_number_from == LATEST_BLOCK_NUMBER:
        block_number_from = eth_api.block_number()
    if block_number_to == LATEST_BLOCK_NUMBER:
        block_number_to = eth_api.block_number()

    logging.info('Working set is block_number_from: %d to block_number_to: %d', block_number_from, block_number_to)

    # Just an example to be moved in for loop
    storage_at = eth_api.get_storage_at('0x33ee33fc3e1aacdb75a1ad362489ac54f02d6d63', '0x00', 2000001)
    logging.info('TG API: storage at location 0x00 for 0x33ee...6d63 in block 2000001: %s', storage_at)

    if cmp_node_url is not None:
        result = json_rpc_get_storage_at(cmp_node_url, '33ee33fc3e1aacdb75a1ad362489ac54f02d6d63', 0, 2000001)
        logging.info('JSON RPC API: storage at location 0x00 for 0x33ee...6d63 in block 2000001: %s', result)
        assert result == storage_at

    storage_count = 0
    req_id = 0
    for _, block_number in enumerate(range(block_number_from, block_number_to+1)):
        block = eth_api.get_block_by_number(block_number)
        logging.info('Processing block_number: #%d with #transaction: %d', block_number, len(block.body.transactions))
        for index, transaction in enumerate(block.body.transactions):
            if transaction.to.hex() and transaction.gas_limit > 21000:
                logging.info('Processing non-trivial transaction: #%d to: 0x%s', index, transaction.to.hex())
                if storage_count % 10 == 0:
                    storage_count += 1
                    next_key = '0x' + (32 * b'\x00').hex()
                    json_state_map = {}
                    silksnake_state_map = {}
                    while next_key:
                        req_id += 1
                        logging.info('Processing next_key: %s req_id: %s', next_key, req_id)
                        rng = json_rpc_storage_range_at(cmp_node_url, block.hash.hex(), index, transaction.to.hex(), next_key, 1024, req_id)
                        for hashed_key, entry in rng['storage'].items():
                            key = entry['key']
                            json_state_map[hashed_key] = entry
                            if key is None:
                                logging.info('Null key: hashed_key %s entry: %s', hashed_key, entry)
                            value = eth_api.get_storage_at('0x' + transaction.to.hex(), key, block_number)
                            silksnake_state_map[hashed_key] = {'key': key, 'value': value}
                        next_key = rng['nextKey']
                    if not compare_storage_ranges(json_state_map, silksnake_state_map):
                        print_storage_ranges(json_state_map, silksnake_state_map)
                        return

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)-15s %(message)s', level=logging.INFO)

    signal.signal(signal.SIGINT, terminate_process)
    signal.signal(signal.SIGQUIT, terminate_process)

    logging.info('%s: START - PID is %d', __file__, os.getpid())

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-s', '--block_number_from', default=LATEST_BLOCK_NUMBER, help='the start block number as integer (less than or equal to end)')
    parser.add_argument('-e', '--block_number_to', default=LATEST_BLOCK_NUMBER, help='the end block number as integer (greater than or equal to start)')
    parser.add_argument('-t', '--target', default='localhost:9090', help='the Turbo node location as string <address>:<port>')
    parser.add_argument('-u', '--url', help='the Ethereum node location to compare as URL string or null if no compare')
    args = parser.parse_args()

    bench_json_rpc(int(args.block_number_from), int(args.block_number_to), args.target, args.url)

    logging.info('%s: END', __file__)
