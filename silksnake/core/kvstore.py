# -*- coding: utf-8 -*-
"""The key-value (KV) store."""

import abc

from typing import Iterator, NamedTuple

class Cursor(abc.ABCMeta):
    """ This class represents a remote read-only cursor on the KV.
    """
    def with_prefix(cls, prefix: bytes):
        """ Configure the cursor with the specified prefix."""
        raise NotImplementedError

    def enable_streaming(cls, streaming: bool):
        """ Configure the cursor with the specified streaming flag."""
        raise NotImplementedError

    def seek(cls, key: bytes) -> (bytes, bytes):
        """ Seek the value in the bucket associated to the specified key."""
        raise NotImplementedError

    def seek_exact(cls, key: bytes) -> bytes:
        """ Seek the value in the bucket associated to the specified key, matching key exactly."""
        raise NotImplementedError

    def next(cls) -> Iterator[NamedTuple('Pair', [('key', bytes), ('value', bytes)])]:
        """ Get key-value streaming iterator for the bucket bound to prefix."""
        raise NotImplementedError

class View(abc.ABCMeta):
    """ This class represents a read-only view on the KV store.
    """
    @abc.abstractclassmethod
    def view(cls):
        """Returns a new view on the KV store."""
        raise NotImplementedError

    def cursor(cls, bucket_name: str) -> Cursor:
        """ Create a new cursor on the KV."""
        raise NotImplementedError

    def get(cls, bucket_name: str, key: bytes) -> (bytes, bytes):
        """ Get the value associated to the key in specified bucket."""
        raise NotImplementedError

    def get_exact(cls, bucket_name: str, key: bytes) -> bytes:
        """ Get the value associated to the key in specified bucket, checking exact key match."""
        raise NotImplementedError

class KV(abc.ABCMeta):
    """ This class represents the KV store.
    """
    @abc.abstractclassmethod
    def view(cls) -> View:
        """Returns a new view on the KV store."""
        raise NotImplementedError
