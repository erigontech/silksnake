# -*- coding: utf-8 -*-

"""The test sets for turbo-geth/silkworm KV remote."""

import json
import os

test_sets_filename = os.path.join(os.path.dirname(__file__), 'test_sets.json')
with open(test_sets_filename) as test_sets_file:
    test_sets = json.load(test_sets_file)
    seek_invalidTestSets = test_sets['seek_invalidTestSets']
    seek_validTestSets = test_sets['seek_validTestSets']
    seek_testSets = seek_invalidTestSets + seek_validTestSets
