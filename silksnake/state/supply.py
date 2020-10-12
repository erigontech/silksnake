# -*- coding: utf-8 -*-
"""The chain supply."""

from ..core import kvstore
from ..helpers.dbutils import tables
from ..rlp import sedes

ETH_SUPPLY_NOT_AVAILABLE = -1

def read_eth_supply(view: kvstore.View, block_number: int) -> int:
    """ read_eth_supply """
    encoded_block_number = sedes.encode_block_number(block_number)
    key, value = view.get(tables.ETH_SUPPLY_LABEL, encoded_block_number)
    if key != encoded_block_number:
        return ETH_SUPPLY_NOT_AVAILABLE
    supply = int.from_bytes(value, 'big')
    return supply
