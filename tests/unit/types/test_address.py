# -*- coding: utf-8 -*-
"""The unit test for address module."""

import pytest

from silksnake.types.address import Address

# pylint: disable=line-too-long,no-self-use,unnecessary-lambda

class TestAddress:
    """ Unit test case for Address.
    """
    @pytest.mark.parametrize("hex_string,address_bytes,should_pass", [
        # Valid test list
        ('0x33ee33fc3e1aacdb75a1ad362489ac54f02d6d63', b'3\xee3\xfc>\x1a\xac\xdbu\xa1\xad6$\x89\xacT\xf0-mc', True),
        ('33ee33fc3e1aacdb75a1ad362489ac54f02d6d63', b'3\xee3\xfc>\x1a\xac\xdbu\xa1\xad6$\x89\xacT\xf0-mc', True),
        ('0033ee33fc3e1aacdb75a1ad362489ac54f02d6d63', b'3\xee3\xfc>\x1a\xac\xdbu\xa1\xad6$\x89\xacT\xf0-mc', True),
        ('FF33ee33fc3e1aacdb75a1ad362489ac54f02d6d63', b'3\xee3\xfc>\x1a\xac\xdbu\xa1\xad6$\x89\xacT\xf0-mc', True),

        # Invalid test list
        ('zz0x33ee33fc3e1aacdb75a1ad362489ac54f02d6d63', b'3\xee3\xfc>\x1a\xac\xdbu\xa1\xad6$\x89\xacT\xf0-mc', False),
        ('zz33ee33fc3e1aacdb75a1ad362489ac54f02d6d63', b'3\xee3\xfc>\x1a\xac\xdbu\xa1\xad6$\x89\xacT\xf0-mc', False),
        ('ee33fc3e1aacdb75a1ad362489ac54f02d6d63', b'\xee3\xfc>\x1a\xac\xdbu\xa1\xad6$\x89\xacT\xf0-mc', False),
        (None, b'\xee3\xfc>\x1a\xac\xdbu\xa1\xad6$\x89\xacT\xf0-mc', False),
    ])
    def test_from_hex(self, hex_string: str, address_bytes: bytes, should_pass: bool):
        """ Unit test for from_hex. """
        if should_pass:
            assert Address.from_hex(hex_string).bytes == address_bytes
        else:
            with pytest.raises((ValueError)):
                Address.from_hex(hex_string)
