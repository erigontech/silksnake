#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The kv_seek command line tool allows to query the turbo-geth/silkworm KV gRPC."""

import argparse

import context # pylint: disable=unused-import

from silksnake.core.remote import kv_remote

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('bucket', help='the bucket tag as string')
parser.add_argument('seek_key', help='the seek key as hex string without leading 0x')
parser.add_argument('-t', '--target', default='localhost:9090', help='the server location as string <address>:<port>')
args = parser.parse_args()

print('>: bucket:', args.bucket, 'seek_key:', args.seek_key)

remote_kv_client = kv_remote.new_remote_kv_client()
remote_kv = remote_kv_client.with_target(args.target).open()
key, value = remote_kv.view().get(args.bucket, bytes.fromhex(args.seek_key))
remote_kv.close()

print('<: key:', key.hex(), 'value:', value.hex())
