# -*- coding: utf-8 -*-
"""The Recursive Length Prefix (RLP) encoding/decoding for logs."""

import rlp

from .sedes import address
from .sedes import RlpSerializable, uint32

class Log(RlpSerializable):
    """ RLP sedes for block logs.
    """
    fields = [
        ('address', address),
        ('topics', rlp.sedes.CountableList(uint32)),
        ('data', rlp.sedes.binary)
    ]
