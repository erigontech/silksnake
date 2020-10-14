# -*- coding: utf-8 -*-
"""The key-value (KV) store."""

import abc

from typing import Iterator, NamedTuple

class Cursor(abc.ABC):
    """ This class represents a remote read-only cursor on the KV.
    """
    @abc.abstractmethod
    def with_prefix(self, prefix: bytes):
        """ Configure the cursor with the specified prefix."""
        raise NotImplementedError

    @abc.abstractmethod
    def enable_streaming(self, streaming: bool):
        """ Configure the cursor with the specified streaming flag."""
        raise NotImplementedError

    @abc.abstractmethod
    def seek(self, key: bytes) -> (bytes, bytes):
        """ Seek the value in the bucket associated to the specified key."""
        raise NotImplementedError

    @abc.abstractmethod
    def seek_exact(self, key: bytes) -> bytes:
        """ Seek the value in the bucket associated to the specified key, matching key exactly."""
        raise NotImplementedError

    @abc.abstractmethod
    def next(self) -> Iterator[NamedTuple('Pair', [('key', bytes), ('value', bytes)])]:
        """ Get key-value streaming iterator for the bucket bound to prefix."""
        raise NotImplementedError

class View(abc.ABC):
    """ This class represents a read-only view on the KV store.
    """
    @abc.abstractmethod
    def cursor(self, bucket_name: str) -> Cursor:
        """ Create a new cursor on the KV."""
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, bucket_name: str, key: bytes) -> (bytes, bytes):
        """ Get the value associated to the key in specified bucket."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_exact(self, bucket_name: str, key: bytes) -> bytes:
        """ Get the value associated to the key in specified bucket, checking exact key match."""
        raise NotImplementedError

class KV(abc.ABC):
    """ This class represents the KV store.
    """
    @abc.abstractmethod
    def view(self) -> View:
        """Returns a new view on the KV store."""
        raise NotImplementedError
