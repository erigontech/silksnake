# -*- coding: utf-8 -*-
"""The LMDB client."""

class DefaultBucketConfigsFunc: # pylint: disable=too-few-public-methods
    """ The DefaultBucketConfigsFunc class represents a functor for default bucket configuration.
    """
    def __call__(self, default_buckets):
        return default_buckets
