#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The bench_tools bench."""

import argparse
import logging
import os
import runpy
import signal
import sys

import context # pylint: disable=unused-import

module_command_list = [
    ['tools.kv_seek_account_history'    , 'fe09353b5740a2255ba62879512a94e8bf53f7f4', '2000001'],
    ['tools.kv_seek_block_body'         , '2000001'],
    ['tools.kv_seek_block_body'         , '2000001', '-c', '3'],
    ['tools.kv_seek_block_header'       , '2000001'],
    ['tools.kv_seek_block_header'       , '2000001', '-c', '2'],
    ['tools.kv_seek_block_number'       , 'e42335922909e0d371ca5e0aeb78afacfb9ff7e073304f7b9da88344dfb15550'],
    ['tools.kv_seek_block_receipt'      , '3384025'],
    ['tools.kv_seek_block_receipt'      , '3384025', '-c', '4'],
    ['tools.kv_seek_plain_change_sets'  , '2000000'],
    ['tools.kv_seek_plain_change_sets'  , '2000000', '-c', '1'],
    ['tools.kv_seek_plain_contract_code', '33ee33fc3e1aacdb75a1ad362489ac54f02d6d63', '-i', '1'],
    ['tools.kv_seek_plain_state'        , '256b4f8185caa65ea98764e8ea2fd9cd4a5993e6', '-l', '0x02'],
    ['tools.kv_seek_tx_senders'         , '3384025'],
    ['tools.kv_seek_tx_senders'         , '3384025', '-c', '2'],
    ['tools.kv_seek'                    , 'b', '000000000033a2db'],

    ['tools.silksnake_execute_block'       , 'goerli', '3608234', '-g', '8800000'],
    ['tools.silksnake_execute_block'       , 'goerli', '3608233'],
    ['tools.silksnake_execute_transaction' , 'goerli', '0x2bc0dd89423d726a02f1f5cf18a3eea9db68c1abd7239ef5ca62477818c85675'],
    ['tools.silksnake_execute_transaction' , 'goerli', '0x842e6b4b3238a32bd2d68fd4d71edd2651c6a507f20d9fa84e4b22a8bd60df4f'],
]

ext_module_command_list = [
    ['tools.kv_seek_eth_supply'         , '3384025'], # requires TG eth-supply extension module
    ['tools.kv_seek_eth_supply'         , '3384025', '-c', '2'], # requires TG eth-supply extension module
]

def terminate_process(signal_number: int, frame): # pylint: disable=unused-argument
    """ terminate_process """
    print()
    logging.info('%s: signal %d, terminating...', __file__, signal_number)
    sys.exit()

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)-15s %(message)s', level=logging.INFO)

    signal.signal(signal.SIGINT, terminate_process)
    signal.signal(signal.SIGQUIT, terminate_process)

    logging.info('%s: START - PID is %d', __file__, os.getpid())

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-ext', action='store_true', help='flag indicating that extended modules should be included')
    args = parser.parse_args()

    if args.ext:
        module_command_list.extend(ext_module_command_list)

    for index, module_command in enumerate(module_command_list):
        module_name = module_command[0]
        module_args = module_command[1:]
        print('$ ' + module_name, ' '.join(module_args))
        sys.argv[1:] = module_args
        runpy.run_module(module_name, run_name='__main__')
        if index < len(module_command_list) - 1:
            print()

    logging.info('%s: END', __file__)
