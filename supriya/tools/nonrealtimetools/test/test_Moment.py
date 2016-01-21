# -*- encoding: utf-8 -*-
import unittest
from supriya.tools import nonrealtimetools


class TestCase(unittest.TestCase):

    def test_iterate_nodes(self):

        nodes = {
            'A': ['B', 'C', 'D'],
            'B': None,
            'C': ['E', 'F'],
            'D': None,
            'E': ['G'],
            'F': None,
            'G': None,
            }
        root = 'A'

        iterator = nonrealtimetools.Moment._iterate_nodes(root, nodes)
        assert list(iterator) == ['A', 'B', 'C', 'E', 'G', 'F', 'D']
