# -*- coding: utf-8 -*-
"""The Turbo-Geth/Silkworm chai configuration."""

from ..helpers import hashing

MAINNET = 'mainnet'
ROPSTEN = 'ropsten'
RINKEBY = 'rinkeby'
GOERLI  = 'goerli'

MAINNET_GENESIS_HASH = hashing.hex_as_hash('0xd4e56740f876aef8c010b86a40d5f56745a118d0906a34e69aec8c0db1cb8fa3')
ROPSTEN_GENESIS_HASH = hashing.hex_as_hash('0x41941023680923e0fe4d74a34bdac8141f2540e3ae90623718e47d66d1ca4a2d')
RINKEBY_GENESIS_HASH = hashing.hex_as_hash('0x6341fd3daf94b748c72ced5a5b26028f2474f5f00d824504e4fa37a75767e177')
GOERLI_GENESIS_HASH  = hashing.hex_as_hash('0xbf7e331f7f7c1dd2e05159666b3bf8bc7a8a3a9eb1d518969eab529dd9b88c1a')

CHAIN_TABLE = {
    MAINNET : MAINNET_GENESIS_HASH,
    ROPSTEN : ROPSTEN_GENESIS_HASH,
    RINKEBY : RINKEBY_GENESIS_HASH,
    GOERLI  : GOERLI_GENESIS_HASH,
}
