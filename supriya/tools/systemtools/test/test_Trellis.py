# -*- encoding: utf-8 -*-
import unittest
from supriya.tools import systemtools


class TestCase(unittest.TestCase):

    def test___contains__(self):
        trellis = systemtools.Trellis()
        assert 'A' not in trellis
        assert 'B' not in trellis
        trellis.add('A')
        assert 'A' in trellis
        assert 'B' not in trellis
        trellis.add('B', parent='A')
        assert 'A' in trellis
        assert 'B' in trellis
        trellis.remove('A')
        assert 'A' not in trellis
        assert 'B' in trellis
        trellis.remove('B')
        assert 'A' not in trellis
        assert 'B' not in trellis

    def test___eq__(self):
        trellis_one = systemtools.Trellis()
        trellis_two = systemtools.Trellis()
        trellis_three = systemtools.Trellis()
        assert trellis_one == trellis_two
        assert trellis_one != 'foo'
        trellis_one.add('A', parent='B')
        trellis_one.add('C', parent='B')
        assert trellis_one != trellis_two
        trellis_two.add('C', parent='B')
        trellis_two.add('A', parent='B')
        assert trellis_one != trellis_two
        trellis_three.add('C', parent='B')
        trellis_three.add('A', parent='B')
        assert trellis_two == trellis_three

    def test___getitem__(self):
        trellis = systemtools.Trellis()
        trellis.add('B', parent='A')
        trellis.add('C', parent='A')
        trellis.add('D', parent='A')
        trellis.add('D', parent='B')
        assert trellis['A'] == (frozenset([]), frozenset(['B', 'C', 'D']))
        assert trellis['B'] == (frozenset(['A']), frozenset(['D']))
        assert trellis['C'] == (frozenset(['A']), frozenset([]))
        assert trellis['D'] == (frozenset(['A', 'B']), frozenset([]))

    def test___iter__(self):
        trellis = systemtools.Trellis()
        trellis.add('A')
        trellis.add('B', parent='A')
        trellis.add('C', parent='A')
        trellis.add('D', parent='B')
        trellis.add('D', parent='C')
        trellis.add('E', parent='A')
        assert list(trellis) == ['D', 'B', 'C', 'E', 'A']
        assert list(trellis) == ['D', 'B', 'C', 'E', 'A']  # non-destructive
        trellis.remove('A')
        assert list(trellis) == ['D', 'B', 'C', 'E']
        trellis.remove('C')
        assert list(trellis) == ['D', 'B', 'E']

    def test___len__(self):
        trellis = systemtools.Trellis()
        assert len(trellis) == 0
        trellis.add('A')
        assert len(trellis) == 1
        trellis.add('B', parent='A')
        assert len(trellis) == 2
        trellis.add('C', parent='A')
        assert len(trellis) == 3
        trellis.remove('A')
        assert len(trellis) == 2
        trellis.remove('B')
        assert len(trellis) == 1
        trellis.remove('C')
        assert len(trellis) == 0

    def test_add(self):
        trellis = systemtools.Trellis()
        trellis.add('A')
        assert 'A' in trellis
        trellis.add('B', parent='C')
        assert 'B' in trellis
        assert 'C' in trellis
        trellis.add('B', parent='A')
        assert 'A' in trellis
        assert 'B' in trellis
        assert 'C' in trellis

    def test_children(self):
        trellis = systemtools.Trellis()
        trellis.add('B', parent='A')
        trellis.add('C', parent='A')
        trellis.add('D')
        trellis.add('E', parent='A')
        trellis.add('E', parent='D')
        assert trellis.children('A') == frozenset(['B', 'C', 'E'])
        assert trellis.children('B') == frozenset([])
        assert trellis.children('C') == frozenset([])
        assert trellis.children('D') == frozenset(['E'])
        assert trellis.children('E') == frozenset([])

    def test_copy(self):
        trellis_one = systemtools.Trellis()
        trellis_one.add('A', parent='B')
        trellis_one.add('C', parent='B')
        trellis_two = trellis_one.copy()
        assert trellis_one == trellis_two
        assert trellis_one is not trellis_two
        trellis_one.remove('B')
        assert trellis_one != trellis_two

    def test_is_acyclic(self):
        trellis = systemtools.Trellis()
        assert trellis.is_acyclic()
        trellis.add('A')
        assert trellis.is_acyclic()
        trellis.add('B', parent='A')
        assert trellis.is_acyclic()
        trellis.add('C', parent='B')
        assert trellis.is_acyclic()
        trellis.add('A', parent='C')
        assert not trellis.is_acyclic()
        trellis.remove('B')
        assert trellis.is_acyclic()

    def test_parents(self):
        trellis = systemtools.Trellis()
        trellis.add('B', parent='A')
        trellis.add('C', parent='A')
        trellis.add('D')
        trellis.add('E', parent='A')
        trellis.add('E', parent='D')
        assert trellis.parents('A') == frozenset([])
        assert trellis.parents('B') == frozenset(['A'])
        assert trellis.parents('C') == frozenset(['A'])
        assert trellis.parents('D') == frozenset([])
        assert trellis.parents('E') == frozenset(['A', 'D'])

    def test_remove(self):
        trellis = systemtools.Trellis()
        with self.assertRaises(ValueError):
            trellis.remove('A')
        assert 'A' not in trellis
        trellis.add('A')
        assert 'A' in trellis
        trellis.remove('A')
        assert 'A' not in trellis
