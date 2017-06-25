import types
from abjad.tools import systemtools
from supriya.tools import patterntools
from supriya.tools import servertools


class TestCase(systemtools.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        self.pseudo_server = types.SimpleNamespace(
            audio_bus_allocator=servertools.BlockAllocator(),
            control_bus_allocator=servertools.BlockAllocator(),
            node_id_allocator=servertools.NodeIdAllocator(),
            )

    def test_iterate_inner_1(self):
        pattern = patterntools.Pbind(
            duration=1.0,
            frequency=patterntools.Pseq([111, 222, 333, 444, 555, 666]),
            )
        iterator = patterntools.RealtimeEventPlayer._iterate_inner(
            pattern=pattern,
            server=self.pseudo_server,
            timestamp=0.0,
            uuids={},
            )
        event_products = list(iterator)
        assert all(
            isinstance(_, patterntools.EventProduct)
            for _ in event_products
            )
        assert [_._get_sort_bundle() for _ in event_products] == [
            (0.0, (0, 0), False),
            (1.0, (0, 0), True),
            (1.0, (1, 0), False),
            (2.0, (1, 0), True),
            (2.0, (2, 0), False),
            (3.0, (2, 0), True),
            (3.0, (3, 0), False),
            (4.0, (3, 0), True),
            (4.0, (4, 0), False),
            (5.0, (4, 0), True),
            (5.0, (5, 0), False),
            (6.0, (5, 0), True),
            ]

    def test_iterate_inner_2(self):
        pattern = patterntools.Pbind(
            delta=0.25,
            duration=1.0,
            frequency=patterntools.Pseq([111, 222, 333, 444, 555, 666]),
            )
        iterator = patterntools.RealtimeEventPlayer._iterate_inner(
            pattern=pattern,
            server=self.pseudo_server,
            timestamp=0.0,
            uuids={},
            )
        event_products = list(iterator)
        assert all(
            isinstance(_, patterntools.EventProduct)
            for _ in event_products
            )
        assert [_._get_sort_bundle() for _ in event_products] == [
            (0.0, (0, 0), False),
            (0.25, (1, 0), False),
            (0.5, (2, 0), False),
            (0.75, (3, 0), False),
            (1.0, (0, 0), True),
            (1.0, (4, 0), False),
            (1.25, (1, 0), True),
            (1.25, (5, 0), False),
            (1.5, (2, 0), True),
            (1.75, (3, 0), True),
            (2.0, (4, 0), True),
            (2.25, (5, 0), True),
            ]

    def test_iterate_inner_3(self):
        pattern = patterntools.Pbind(
            duration=patterntools.Pseq([1.0, 2.0], None),
            frequency=patterntools.Pseq([111, 222, 333, 444, 555, 666]),
            )
        iterator = patterntools.RealtimeEventPlayer._iterate_inner(
            pattern=pattern,
            server=self.pseudo_server,
            timestamp=0.0,
            uuids={},
            )
        event_products = list(iterator)
        assert all(
            isinstance(_, patterntools.EventProduct)
            for _ in event_products
            )
        assert [_._get_sort_bundle() for _ in event_products] == [
            (0.0, (0, 0), False),
            (1.0, (0, 0), True),
            (1.0, (1, 0), False),
            (3.0, (1, 0), True),
            (3.0, (2, 0), False),
            (4.0, (2, 0), True),
            (4.0, (3, 0), False),
            (6.0, (3, 0), True),
            (6.0, (4, 0), False),
            (7.0, (4, 0), True),
            (7.0, (5, 0), False),
            (9.0, (5, 0), True),
            ]

    def test_iterate_inner_4(self):
        pattern = patterntools.Pbind(
            delta=1.0,
            duration=patterntools.Pseq([1.0, 2.0], None),
            frequency=patterntools.Pseq([111, 222, 333, 444, 555, 666]),
            )
        iterator = patterntools.RealtimeEventPlayer._iterate_inner(
            pattern=pattern,
            server=self.pseudo_server,
            timestamp=0.0,
            uuids={},
            )
        event_products = list(iterator)
        assert all(
            isinstance(_, patterntools.EventProduct)
            for _ in event_products
            )
        assert [_._get_sort_bundle() for _ in event_products] == [
            (0.0, (0, 0), False),
            (1.0, (0, 0), True),
            (1.0, (1, 0), False),
            (2.0, (2, 0), False),
            (3.0, (1, 0), True),
            (3.0, (2, 0), True),
            (3.0, (3, 0), False),
            (4.0, (4, 0), False),
            (5.0, (3, 0), True),
            (5.0, (4, 0), True),
            (5.0, (5, 0), False),
            (7.0, (5, 0), True),
            ]

    def test_iterate_inner_5(self):
        pattern = patterntools.Pbind(
            delta=patterntools.Pseq([1.0, 0.0], None),
            duration=2.0,
            frequency=patterntools.Pseq([111, 222, 333, 444, 555, 666]),
            )
        iterator = patterntools.RealtimeEventPlayer._iterate_inner(
            pattern=pattern,
            server=self.pseudo_server,
            timestamp=0.0,
            uuids={},
            )
        event_products = list(iterator)
        assert all(
            isinstance(_, patterntools.EventProduct)
            for _ in event_products
            )
        assert [_._get_sort_bundle() for _ in event_products] == [
            (0.0, (0, 0), False),
            (1.0, (1, 0), False),
            (1.0, (2, 0), False),
            (2.0, (0, 0), True),
            (2.0, (3, 0), False),
            (2.0, (4, 0), False),
            (3.0, (1, 0), True),
            (3.0, (2, 0), True),
            (3.0, (5, 0), False),
            (4.0, (3, 0), True),
            (4.0, (4, 0), True),
            (5.0, (5, 0), True),
            ]
