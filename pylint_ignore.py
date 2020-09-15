# -*- coding: utf-8 -*-
"""This module patches pylint for issue #2686 [https://github.com/PyCQA/pylint/issues/2686]."""

from pylint.utils import utils

class PylintIgnorePaths:
    """The PylintIgnorePaths class supports ignoring specified paths."""
    def __init__(self, *paths):
        self.paths = paths
        self.original_expand_modules = utils.expand_modules
        utils.expand_modules = self.patched_expand

    def patched_expand(self, *args, **kwargs):
        """Overwrites module expansion to ignore configured paths."""
        result, errors = self.original_expand_modules(*args, **kwargs)

        def keep_item(item):
            if any(1 for path in self.paths if item['path'].startswith(path)):
                return False

            return True

        result = list(filter(keep_item, result))

        return result, errors
