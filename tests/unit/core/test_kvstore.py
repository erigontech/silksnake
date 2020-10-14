# -*- coding: utf-8 -*-
"""The unit test for kvstore module."""

import pytest

from silksnake.core import kvstore

# pylint: disable=abstract-class-instantiated

def test_cursor():
    """ Unit test for Cursor."""
    kvstore.Cursor.__abstractmethods__ = frozenset()
    cursor = kvstore.Cursor()
    with pytest.raises(NotImplementedError):
        cursor.with_prefix('')
    with pytest.raises(NotImplementedError):
        cursor.enable_streaming(True)
    with pytest.raises(NotImplementedError):
        cursor.seek(b'')
    with pytest.raises(NotImplementedError):
        cursor.seek_exact(b'')
    with pytest.raises(NotImplementedError):
        cursor.next()

def test_view():
    """ Unit test for View."""
    kvstore.View.__abstractmethods__ = frozenset()
    view = kvstore.View()
    with pytest.raises(NotImplementedError):
        view.cursor('h')
    with pytest.raises(NotImplementedError):
        view.get('h', b'')
    with pytest.raises(NotImplementedError):
        view.get_exact('h', b'')

def test_kv():
    """ Unit test for KV."""
    kvstore.KV.__abstractmethods__ = frozenset()
    with pytest.raises(NotImplementedError):
        kvstore.KV().view()
