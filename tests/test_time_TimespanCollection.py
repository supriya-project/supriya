import itertools
import random

import pytest
import uqbar.io
from abjad import Timespan

import supriya.time

# from supriya.system import SupriyaValueObject
# class Timespan(SupriyaValueObject):
#
#    def __init__( start_offset=float('-inf'), stop_offset=float('inf')):
#        start_offset = float(start_offset)
#        stop_offset = float(stop_offset)
#
#    def __eq__( expr):
#        if not isinstance(expr, type():
#            return False
#        if not expr.start_offset == start_offset:
#            return False
#        if not expr.stop_offset == stop_offset:
#            return False
#        return True
#
#    def __hash__(:
#        return hash((type(, start_offset, stop_offset))


def make_expected_start_offsets(range_=10, timespans=None):
    if not timespans:
        timespans = make_timespans()
    actual_offsets = set()
    for timespan in timespans:
        actual_offsets.add(float(timespan.start_offset))
    actual_offsets = sorted(actual_offsets)
    print("    O:", actual_offsets)
    offsets = {}
    for offset in range(-1, range_ + 1):
        before = [_ for _ in actual_offsets if _ < offset]
        if before:
            before = before[-1]
        else:
            before = None
        after = [_ for _ in actual_offsets if _ > offset]
        if after:
            after = after[0]
        else:
            after = None
        offsets[offset] = (before, after)
    return offsets


def make_simultaneity_fixtures(range_=10, timespans=None):
    if not timespans:
        timespans = make_timespans()
    fixtures = {}
    for offset in range(range_):
        overlaps, starts, stops = [], [], []
        for timespan in timespans:
            if timespan.start_offset == offset:
                starts.append(timespan)
            elif timespan.stop_offset == offset:
                stops.append(timespan)
            elif timespan.start_offset < offset < timespan.stop_offset:
                overlaps.append(timespan)
        overlaps.sort()
        starts.sort()
        stops.sort()
        fixtures[offset] = (overlaps, starts, stops)
    return fixtures


def make_timespans():
    return [
        Timespan(0, 3),
        Timespan(1, 3),
        Timespan(1, 2),
        Timespan(2, 5),
        Timespan(6, 9),
    ]


def make_timespan_collection(accelerated, populated=True, timespans=None):
    if populated and not timespans:
        timespans = make_timespans()
    timespan_collection = supriya.time.TimespanCollection(
        timespans=timespans, accelerated=accelerated
    )
    if accelerated:
        assert isinstance(
            timespan_collection._driver, supriya.time.TimespanCollectionDriverEx
        )
    else:
        assert isinstance(
            timespan_collection._driver, supriya.time.TimespanCollectionDriver
        )
    return timespan_collection


def make_random_timespans(count=10, range_=10):
    indices = list(range(range_))
    timespans = []
    for _ in range(count):
        random.shuffle(indices)
        start_offset, stop_offset = sorted(indices[:2])
        timespan = Timespan(start_offset=start_offset, stop_offset=stop_offset)
        timespans.append(timespan)
    return timespans


def make_target_timespans(range_=10):
    indices = list(range(range_))
    timespans = []
    for pair in itertools.permutations(indices, 2):
        start_offset, stop_offset = sorted(pair)
        target_timespan = Timespan(start_offset=start_offset, stop_offset=stop_offset)
        timespans.append(target_timespan)
    return timespans


@pytest.mark.parametrize("accelerated", [True, False])
def test___contains__(accelerated):
    timespans = make_timespans()
    timespan_collection = make_timespan_collection(
        accelerated=accelerated, populated=True
    )
    assert timespans[0] in timespan_collection
    assert Timespan(-1, 100) not in timespan_collection
    timespan_collection.remove(timespans[-1])
    assert timespans[-1] not in timespan_collection


@pytest.mark.parametrize("accelerated", [True, False])
def test___getitem__(accelerated):
    timespan_collection = make_timespan_collection(
        accelerated=accelerated, populated=True
    )
    assert timespan_collection[-1] == Timespan(6, 9)
    assert [timespan for timespan in timespan_collection[:3]] == [
        Timespan(start_offset=0, stop_offset=3),
        Timespan(start_offset=1, stop_offset=2),
        Timespan(start_offset=1, stop_offset=3),
    ]


@pytest.mark.parametrize("accelerated", [True, False])
def test___init__(accelerated):
    make_timespan_collection(accelerated=accelerated, populated=False)
    make_timespan_collection(accelerated=accelerated, populated=True)


@pytest.mark.parametrize("accelerated", [True, False])
def test___iter__(accelerated):
    timespan_collection = make_timespan_collection(
        accelerated=accelerated, populated=True
    )
    assert [timespan for timespan in timespan_collection] == [
        Timespan(start_offset=0, stop_offset=3),
        Timespan(start_offset=1, stop_offset=2),
        Timespan(start_offset=1, stop_offset=3),
        Timespan(start_offset=2, stop_offset=5),
        Timespan(start_offset=6, stop_offset=9),
    ]
    iterator = iter(timespan_collection)
    assert next(iterator) == Timespan(start_offset=0, stop_offset=3)


@pytest.mark.parametrize("accelerated", [True, False])
def test___len__(accelerated):
    timespan_collection = make_timespan_collection(
        accelerated=accelerated, populated=False
    )
    assert len(timespan_collection) == 0
    timespan_collection = make_timespan_collection(
        accelerated=accelerated, populated=True
    )
    assert len(timespan_collection) == 5


@pytest.mark.parametrize("accelerated", [True, False])
def test___setitem__(accelerated):
    timespan_collection = make_timespan_collection(
        accelerated=accelerated, populated=True
    )
    timespan_collection[-1] = Timespan(-1, 4)
    assert [timespan for timespan in timespan_collection] == [
        Timespan(start_offset=-1, stop_offset=4),
        Timespan(start_offset=0, stop_offset=3),
        Timespan(start_offset=1, stop_offset=2),
        Timespan(start_offset=1, stop_offset=3),
        Timespan(start_offset=2, stop_offset=5),
    ]
    timespan_collection[:3] = [Timespan(100, 200)]
    assert [timespan for timespan in timespan_collection] == [
        Timespan(start_offset=1, stop_offset=3),
        Timespan(start_offset=2, stop_offset=5),
        Timespan(start_offset=100, stop_offset=200),
    ]


@pytest.mark.parametrize("accelerated", [True, False])
def test___sub__(accelerated):
    timespan_collection = make_timespan_collection(
        accelerated=accelerated,
        timespans=[Timespan(0, 16), Timespan(5, 12), Timespan(-2, 8)],
    )
    timespan = Timespan(5, 10)
    result = timespan_collection - timespan
    assert result[:] == [
        Timespan(-2, 5),
        Timespan(0, 5),
        Timespan(10, 12),
        Timespan(10, 16),
    ]


@pytest.mark.timeout(60)
@pytest.mark.parametrize("accelerated", [True, False])
def test_find_intersection_with_offset(accelerated):
    iterations = 10
    count, range_ = 10, 15
    for i in range(iterations):
        print("Iteration:", i)
        timespans = make_random_timespans(count=count, range_=range_)
        timespan_collection = make_timespan_collection(
            accelerated=accelerated, timespans=timespans
        )
        optimized = 0.0
        brute_force = 0.0
        for offset in range(range_):
            with uqbar.io.Timer() as timer:
                found_by_search = set(timespan_collection.find_intersection(offset))
                optimized += timer.elapsed_time
            with uqbar.io.Timer() as timer:
                found_by_brute_force = set()
                for _ in timespan_collection:
                    if _.start_offset <= offset < _.stop_offset:
                        found_by_brute_force.add(_)
                brute_force += timer.elapsed_time
            assert found_by_search == found_by_brute_force
        print(
            "D: {:0.6f}".format(optimized / brute_force),
            "O: {:0.6f}".format(optimized),
            "B: {:0.6f}".format(brute_force),
        )


@pytest.mark.timeout(120)
@pytest.mark.parametrize("accelerated", [True, False])
def test_find_intersection_with_timespan(accelerated):
    iterations = 10
    count, range_ = 10, 15
    target_timespans = make_target_timespans(range_=range_)
    for i in range(iterations):
        print("Iteration:", i)
        timespans = make_random_timespans(count=count, range_=range_)
        timespan_collection = make_timespan_collection(
            accelerated=accelerated, timespans=timespans
        )
        optimized = 0.0
        brute_force = 0.0
        for target_timespan in target_timespans:
            with uqbar.io.Timer() as timer:
                found_by_search = set(
                    timespan_collection.find_intersection(target_timespan)
                )
                optimized += timer.elapsed_time
            with uqbar.io.Timer() as timer:
                found_by_brute_force = set()
                for _ in timespan_collection:
                    if (
                        _.start_offset <= target_timespan.start_offset
                        and target_timespan.start_offset < _.stop_offset
                    ):
                        found_by_brute_force.add(_)
                    elif (
                        target_timespan.start_offset <= _.start_offset
                        and _.start_offset < target_timespan.stop_offset
                    ):
                        found_by_brute_force.add(_)
                brute_force += timer.elapsed_time
            assert found_by_search == found_by_brute_force
            print(
                "D: {:0.6f}".format(optimized / brute_force),
                "O: {:0.6f}".format(optimized),
                "B: {:0.6f}".format(brute_force),
            )


@pytest.mark.timeout(60)
@pytest.mark.parametrize("accelerated", [True, False])
def test_find_timespans_starting_at(accelerated):
    iterations = 100
    count, range_ = 10, 15
    for i in range(iterations):
        print("Iteration:", i)
        timespans = make_random_timespans(count=count, range_=range_)
        timespan_collection = make_timespan_collection(
            accelerated=accelerated, timespans=timespans
        )
        for offset in range(range_):
            found_by_search = set(
                timespan_collection.find_timespans_starting_at(offset)
            )
            found_by_brute_force = set()
            for _ in timespan_collection:
                if _.start_offset == offset:
                    found_by_brute_force.add(_)
            assert found_by_search == found_by_brute_force


@pytest.mark.timeout(60)
@pytest.mark.parametrize("accelerated", [True, False])
def test_find_timespans_stopping_at(accelerated):
    iterations = 100
    count, range_ = 10, 15
    for i in range(iterations):
        print("Iteration:", i)
        timespans = make_random_timespans(count=count, range_=range_)
        timespan_collection = make_timespan_collection(
            accelerated=accelerated, timespans=timespans
        )
        for offset in range(range_):
            found_by_search = set(
                timespan_collection.find_timespans_stopping_at(offset)
            )
            found_by_brute_force = set()
            for _ in timespan_collection:
                if _.stop_offset == offset:
                    found_by_brute_force.add(_)
            assert found_by_search == found_by_brute_force


@pytest.mark.timeout(60)
@pytest.mark.parametrize("accelerated", [True, False])
def test_get_simultaneity_at(accelerated):
    iterations = 100
    count, range_ = 10, 15
    for i in range(iterations):
        print("Iteration:", i)
        timespans = make_random_timespans(count=count, range_=range_)
        timespan_collection = make_timespan_collection(
            accelerated=accelerated, timespans=timespans
        )
        fixtures = make_simultaneity_fixtures(range_=range_, timespans=timespans)
        for offset in range(range_):
            overlaps, starts, stops = fixtures[offset]
            expected = supriya.time.TimespanSimultaneity(
                overlap_timespans=overlaps,
                start_offset=offset,
                start_timespans=starts,
                stop_timespans=stops,
                timespan_collection=timespan_collection,
            )
            actual = timespan_collection.get_simultaneity_at(offset)
            assert expected.timespan_collection is actual.timespan_collection
            assert expected.start_offset == actual.start_offset
            assert expected.start_timespans == actual.start_timespans
            assert expected.stop_timespans == actual.stop_timespans
            assert expected.overlap_timespans == actual.overlap_timespans


@pytest.mark.timeout(60)
@pytest.mark.parametrize("accelerated", [True, False])
def test_get_start_offset(accelerated):
    iterations = 100
    count, range_ = 10, 15
    for i in range(iterations):
        print("Iteration:", i)
        timespans = make_random_timespans(count=count, range_=range_)
        timespan_collection = make_timespan_collection(
            accelerated=accelerated, timespans=timespans
        )
        expected_offsets = make_expected_start_offsets(
            range_=range_, timespans=timespans
        )
        for timespan in sorted(timespans):
            print("    Timespan:", timespan)
        for offset in range(-1, range_ + 1):
            print("    Offset:", offset)
            print("        :", expected_offsets[offset])
            expected_before, expected_after = expected_offsets[offset]
            actual_before = timespan_collection.get_start_offset_before(offset)
            actual_after = timespan_collection.get_start_offset_after(offset)
            assert expected_before == actual_before, offset
            assert expected_after == actual_after, offset


@pytest.mark.parametrize("accelerated", [True, False])
def test_index(accelerated):
    timespans = make_timespans()
    timespan_collection = make_timespan_collection(
        accelerated=accelerated, populated=True
    )
    assert timespan_collection.index(timespans[0]) == 0
    assert timespan_collection.index(timespans[1]) == 2
    assert timespan_collection.index(timespans[2]) == 1
    assert timespan_collection.index(timespans[3]) == 3
    assert timespan_collection.index(timespans[4]) == 4
    with pytest.raises(ValueError):
        timespan = Timespan(-100, 100)
        timespan_collection.index(timespan)


@pytest.mark.parametrize("accelerated", [True, False])
def test_insert(accelerated):
    timespan_collection = make_timespan_collection(
        accelerated=accelerated, populated=False
    )
    timespan_collection.add(Timespan(1, 3))
    timespan_collection.update((Timespan(0, 4), Timespan(2, 6)))
    assert timespan_collection[:] == [
        Timespan(start_offset=0, stop_offset=4),
        Timespan(start_offset=1, stop_offset=3),
        Timespan(start_offset=2, stop_offset=6),
    ]


@pytest.mark.parametrize("accelerated", [True, False])
def test_iterate_simultaneities(accelerated):
    timespan_collection = make_timespan_collection(
        accelerated=accelerated, populated=True
    )
    simultaneities = list(timespan_collection.iterate_simultaneities())
    assert [x.start_offset for x in simultaneities] == [0, 1, 2, 6]
    simultaneities = list(timespan_collection.iterate_simultaneities(reverse=True))
    assert [x.start_offset for x in simultaneities] == [6, 2, 1, 0]


@pytest.mark.parametrize("accelerated", [True, False])
def test_remove(accelerated):
    timespans = make_timespans()
    timespan_collection = make_timespan_collection(
        accelerated=accelerated, populated=True
    )
    assert list(timespan_collection) == sorted(timespans)
    with pytest.raises(ValueError):
        timespan_collection.remove(timespans[1:-1])
    assert list(timespan_collection) == sorted(timespans)
    for timespan in timespan_collection[1:-1]:
        timespan_collection.remove(timespan)
    assert timespan_collection[:] == [
        Timespan(start_offset=0, stop_offset=3),
        Timespan(start_offset=6, stop_offset=9),
    ]


def test_get_offset_after():
    timespans = [
        Timespan(0, 3),
        Timespan(1, 3),
        Timespan(1, 2),
        Timespan(2, 5),
        Timespan(5, 10),
        Timespan(5, 12),
        Timespan(6, 9),
        Timespan(13, 15),
    ]
    expected = [
        (-2, 0.0),
        (-1, 0.0),
        (0, 1.0),
        (1, 2.0),
        (2, 3.0),
        (3, 5.0),
        (4, 5.0),
        (5, 6.0),
        (6, 9.0),
        (7, 9.0),
        (8, 9.0),
        (9, 10.0),
        (10, 12.0),
        (11, 12.0),
        (12, 13.0),
        (13, 15.0),
        (14, 15.0),
        (15, None),
        (16, None),
    ]
    for _ in range(10):
        timespan_collection = supriya.time.TimespanCollection(timespans)
        actual = [(i, timespan_collection.get_offset_after(i)) for i in range(-2, 17)]
        assert actual == expected
        random.shuffle(timespans)
