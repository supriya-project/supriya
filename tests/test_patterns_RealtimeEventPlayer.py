import supriya.patterns
import supriya.realtime


def test_iterate_inner_1(pseudo_server):
    pattern = supriya.patterns.Pbind(
        duration=1.0,
        frequency=supriya.patterns.Pseq([111, 222, 333, 444, 555, 666]),
        )
    iterator = supriya.patterns.RealtimeEventPlayer._iterate_inner(
        pattern=pattern,
        server=pseudo_server,
        timestamp=0.0,
        uuids={},
        )
    event_products = list(iterator)
    assert all(
        isinstance(_, supriya.patterns.EventProduct)
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


def test_iterate_inner_2(pseudo_server):
    pattern = supriya.patterns.Pbind(
        delta=0.25,
        duration=1.0,
        frequency=supriya.patterns.Pseq([111, 222, 333, 444, 555, 666]),
        )
    iterator = supriya.patterns.RealtimeEventPlayer._iterate_inner(
        pattern=pattern,
        server=pseudo_server,
        timestamp=0.0,
        uuids={},
        )
    event_products = list(iterator)
    assert all(
        isinstance(_, supriya.patterns.EventProduct)
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


def test_iterate_inner_3(pseudo_server):
    pattern = supriya.patterns.Pbind(
        duration=supriya.patterns.Pseq([1.0, 2.0], None),
        frequency=supriya.patterns.Pseq([111, 222, 333, 444, 555, 666]),
        )
    iterator = supriya.patterns.RealtimeEventPlayer._iterate_inner(
        pattern=pattern,
        server=pseudo_server,
        timestamp=0.0,
        uuids={},
        )
    event_products = list(iterator)
    assert all(
        isinstance(_, supriya.patterns.EventProduct)
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


def test_iterate_inner_4(pseudo_server):
    pattern = supriya.patterns.Pbind(
        delta=1.0,
        duration=supriya.patterns.Pseq([1.0, 2.0], None),
        frequency=supriya.patterns.Pseq([111, 222, 333, 444, 555, 666]),
        )
    iterator = supriya.patterns.RealtimeEventPlayer._iterate_inner(
        pattern=pattern,
        server=pseudo_server,
        timestamp=0.0,
        uuids={},
        )
    event_products = list(iterator)
    assert all(
        isinstance(_, supriya.patterns.EventProduct)
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


def test_iterate_inner_5(pseudo_server):
    pattern = supriya.patterns.Pbind(
        delta=supriya.patterns.Pseq([1.0, 0.0], None),
        duration=2.0,
        frequency=supriya.patterns.Pseq([111, 222, 333, 444, 555, 666]),
        )
    iterator = supriya.patterns.RealtimeEventPlayer._iterate_inner(
        pattern=pattern,
        server=pseudo_server,
        timestamp=0.0,
        uuids={},
        )
    event_products = list(iterator)
    assert all(
        isinstance(_, supriya.patterns.EventProduct)
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
