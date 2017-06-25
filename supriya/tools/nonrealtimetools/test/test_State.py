from supriya.tools import nonrealtimetools
from nonrealtimetools_testbase import TestCase


class TestCase(TestCase):

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

        iterator = nonrealtimetools.State._iterate_nodes(root, nodes)
        assert list(iterator) == ['A', 'B', 'C', 'E', 'G', 'F', 'D']
