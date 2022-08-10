import itertools
import random

import pytest
import uqbar.io

from supriya.intervals import (
    Interval,
    IntervalTree,
    IntervalTreeDriver,
    IntervalTreeDriverEx,
    Moment,
)


def make_expected_start_offsets(range_=10, intervals=None):
    if not intervals:
        intervals = make_intervals()
    actual_offsets = set()
    for interval in intervals:
        actual_offsets.add(float(interval.start_offset))
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


def make_moment_fixtures(range_=10, intervals=None):
    if not intervals:
        intervals = make_intervals()
    fixtures = {}
    for offset in range(range_):
        overlaps, starts, stops = [], [], []
        for interval in intervals:
            if interval.start_offset == offset:
                starts.append(interval)
            elif interval.stop_offset == offset:
                stops.append(interval)
            elif interval.start_offset < offset < interval.stop_offset:
                overlaps.append(interval)
        overlaps.sort()
        starts.sort()
        stops.sort()
        fixtures[offset] = (overlaps, starts, stops)
    return fixtures


def make_intervals():
    return [
        Interval(0, 3),
        Interval(1, 3),
        Interval(1, 2),
        Interval(2, 5),
        Interval(6, 9),
    ]


def make_interval_tree(accelerated, populated=True, intervals=None):
    if populated and not intervals:
        intervals = make_intervals()
    interval_tree = IntervalTree(intervals=intervals, accelerated=accelerated)
    if accelerated:
        assert isinstance(interval_tree._driver, IntervalTreeDriverEx)
    else:
        assert isinstance(interval_tree._driver, IntervalTreeDriver)
    return interval_tree


def make_random_intervals(count=10, range_=10):
    indices = list(range(range_))
    intervals = []
    for _ in range(count):
        random.shuffle(indices)
        start_offset, stop_offset = sorted(indices[:2])
        interval = Interval(start_offset=start_offset, stop_offset=stop_offset)
        intervals.append(interval)
    return intervals


def make_target_intervals(range_=10):
    indices = list(range(range_))
    intervals = []
    for pair in itertools.permutations(indices, 2):
        start_offset, stop_offset = sorted(pair)
        target_interval = Interval(start_offset=start_offset, stop_offset=stop_offset)
        intervals.append(target_interval)
    return intervals


@pytest.mark.parametrize("accelerated", [True, False])
def test___contains__(accelerated):
    intervals = make_intervals()
    interval_tree = make_interval_tree(accelerated=accelerated, populated=True)
    assert intervals[0] in interval_tree
    assert Interval(-1, 100) not in interval_tree
    interval_tree.remove(intervals[-1])
    assert intervals[-1] not in interval_tree


@pytest.mark.parametrize("accelerated", [True, False])
def test___getitem__(accelerated):
    interval_tree = make_interval_tree(accelerated=accelerated, populated=True)
    assert interval_tree[-1] == Interval(6, 9)
    assert [interval for interval in interval_tree[:3]] == [
        Interval(start_offset=0, stop_offset=3),
        Interval(start_offset=1, stop_offset=2),
        Interval(start_offset=1, stop_offset=3),
    ]


@pytest.mark.parametrize("accelerated", [True, False])
def test___init__(accelerated):
    make_interval_tree(accelerated=accelerated, populated=False)
    make_interval_tree(accelerated=accelerated, populated=True)


@pytest.mark.parametrize("accelerated", [True, False])
def test___iter__(accelerated):
    interval_tree = make_interval_tree(accelerated=accelerated, populated=True)
    assert [interval for interval in interval_tree] == [
        Interval(start_offset=0, stop_offset=3),
        Interval(start_offset=1, stop_offset=2),
        Interval(start_offset=1, stop_offset=3),
        Interval(start_offset=2, stop_offset=5),
        Interval(start_offset=6, stop_offset=9),
    ]
    iterator = iter(interval_tree)
    assert next(iterator) == Interval(start_offset=0, stop_offset=3)


@pytest.mark.parametrize("accelerated", [True, False])
def test___len__(accelerated):
    interval_tree = make_interval_tree(accelerated=accelerated, populated=False)
    assert len(interval_tree) == 0
    interval_tree = make_interval_tree(accelerated=accelerated, populated=True)
    assert len(interval_tree) == 5


@pytest.mark.parametrize("accelerated", [True, False])
def test___setitem__(accelerated):
    interval_tree = make_interval_tree(accelerated=accelerated, populated=True)
    interval_tree[-1] = Interval(-1, 4)
    assert [interval for interval in interval_tree] == [
        Interval(start_offset=-1, stop_offset=4),
        Interval(start_offset=0, stop_offset=3),
        Interval(start_offset=1, stop_offset=2),
        Interval(start_offset=1, stop_offset=3),
        Interval(start_offset=2, stop_offset=5),
    ]
    interval_tree[:3] = [Interval(100, 200)]
    assert [interval for interval in interval_tree] == [
        Interval(start_offset=1, stop_offset=3),
        Interval(start_offset=2, stop_offset=5),
        Interval(start_offset=100, stop_offset=200),
    ]


@pytest.mark.parametrize("accelerated", [True, False])
def test___sub__(accelerated):
    interval_tree = make_interval_tree(
        accelerated=accelerated,
        intervals=[Interval(0, 16), Interval(5, 12), Interval(-2, 8)],
    )
    interval = Interval(5, 10)
    result = interval_tree - interval
    assert result[:] == [
        Interval(-2, 5),
        Interval(0, 5),
        Interval(10, 12),
        Interval(10, 16),
    ]


@pytest.mark.parametrize("accelerated", [True, False])
def test_find_intersection_with_offset(accelerated):
    iterations = 10
    count, range_ = 10, 15
    for i in range(iterations):
        print("Iteration:", i)
        intervals = make_random_intervals(count=count, range_=range_)
        interval_tree = make_interval_tree(accelerated=accelerated, intervals=intervals)
        optimized = 0.0
        brute_force = 0.0
        for offset in range(range_):
            with uqbar.io.Timer() as timer:
                found_by_search = set(interval_tree.find_intersection(offset))
                optimized += timer.elapsed_time
            with uqbar.io.Timer() as timer:
                found_by_brute_force = set()
                for _ in interval_tree:
                    if _.start_offset <= offset < _.stop_offset:
                        found_by_brute_force.add(_)
                brute_force += timer.elapsed_time
            assert found_by_search == found_by_brute_force
        factor = "{:0.6f}".format(optimized / brute_force) if brute_force else "NaN"
        print(f"D: {factor} O: {optimized} B: {brute_force}")


@pytest.mark.parametrize("accelerated", [True, False])
def test_find_intersection_with_interval(accelerated):
    iterations = 10
    count, range_ = 10, 15
    target_intervals = make_target_intervals(range_=range_)
    for i in range(iterations):
        print("Iteration:", i)
        intervals = make_random_intervals(count=count, range_=range_)
        interval_tree = make_interval_tree(accelerated=accelerated, intervals=intervals)
        optimized = 0.0
        brute_force = 0.0
        for target_interval in target_intervals:
            with uqbar.io.Timer() as timer:
                found_by_search = set(interval_tree.find_intersection(target_interval))
                optimized += timer.elapsed_time
            with uqbar.io.Timer() as timer:
                found_by_brute_force = set()
                for _ in interval_tree:
                    if (
                        _.start_offset <= target_interval.start_offset
                        and target_interval.start_offset < _.stop_offset
                    ):
                        found_by_brute_force.add(_)
                    elif (
                        target_interval.start_offset <= _.start_offset
                        and _.start_offset < target_interval.stop_offset
                    ):
                        found_by_brute_force.add(_)
                brute_force += timer.elapsed_time
            assert found_by_search == found_by_brute_force
        factor = "{:0.6f}".format(optimized / brute_force) if brute_force else "NaN"
        print(f"D: {factor} O: {optimized} B: {brute_force}")


@pytest.mark.parametrize("accelerated", [True, False])
def test_find_intervals_starting_at(accelerated):
    iterations = 100
    count, range_ = 10, 15
    for i in range(iterations):
        print("Iteration:", i)
        intervals = make_random_intervals(count=count, range_=range_)
        interval_tree = make_interval_tree(accelerated=accelerated, intervals=intervals)
        for offset in range(range_):
            found_by_search = set(interval_tree.find_intervals_starting_at(offset))
            found_by_brute_force = set()
            for _ in interval_tree:
                if _.start_offset == offset:
                    found_by_brute_force.add(_)
            assert found_by_search == found_by_brute_force


@pytest.mark.parametrize("accelerated", [True, False])
def test_find_intervals_stopping_at(accelerated):
    iterations = 100
    count, range_ = 10, 15
    for i in range(iterations):
        print("Iteration:", i)
        intervals = make_random_intervals(count=count, range_=range_)
        interval_tree = make_interval_tree(accelerated=accelerated, intervals=intervals)
        for offset in range(range_):
            found_by_search = set(interval_tree.find_intervals_stopping_at(offset))
            found_by_brute_force = set()
            for _ in interval_tree:
                if _.stop_offset == offset:
                    found_by_brute_force.add(_)
            assert found_by_search == found_by_brute_force


@pytest.mark.parametrize("accelerated", [True, False])
def test_get_moment_at(accelerated):
    iterations = 100
    count, range_ = 10, 15
    for i in range(iterations):
        print("Iteration:", i)
        intervals = make_random_intervals(count=count, range_=range_)
        interval_tree = make_interval_tree(accelerated=accelerated, intervals=intervals)
        fixtures = make_moment_fixtures(range_=range_, intervals=intervals)
        for offset in range(range_):
            overlaps, starts, stops = fixtures[offset]
            expected = Moment(
                overlap_intervals=overlaps,
                start_offset=offset,
                start_intervals=starts,
                stop_intervals=stops,
                interval_tree=interval_tree,
            )
            actual = interval_tree.get_moment_at(offset)
            assert expected.interval_tree is actual.interval_tree
            assert expected.start_offset == actual.start_offset
            assert expected.start_intervals == actual.start_intervals
            assert expected.stop_intervals == actual.stop_intervals
            assert expected.overlap_intervals == actual.overlap_intervals


@pytest.mark.parametrize("accelerated", [True, False])
def test_get_start_offset(accelerated):
    iterations = 100
    count, range_ = 10, 15
    for i in range(iterations):
        print("Iteration:", i)
        intervals = make_random_intervals(count=count, range_=range_)
        interval_tree = make_interval_tree(accelerated=accelerated, intervals=intervals)
        expected_offsets = make_expected_start_offsets(
            range_=range_, intervals=intervals
        )
        for interval in sorted(intervals):
            print("    Interval:", interval)
        for offset in range(-1, range_ + 1):
            print("    Offset:", offset)
            print("        :", expected_offsets[offset])
            expected_before, expected_after = expected_offsets[offset]
            actual_before = interval_tree.get_start_offset_before(offset)
            actual_after = interval_tree.get_start_offset_after(offset)
            assert expected_before == actual_before, offset
            assert expected_after == actual_after, offset


@pytest.mark.parametrize("accelerated", [True, False])
def test_index(accelerated):
    intervals = make_intervals()
    interval_tree = make_interval_tree(accelerated=accelerated, populated=True)
    assert interval_tree.index(intervals[0]) == 0
    assert interval_tree.index(intervals[1]) == 2
    assert interval_tree.index(intervals[2]) == 1
    assert interval_tree.index(intervals[3]) == 3
    assert interval_tree.index(intervals[4]) == 4
    with pytest.raises(ValueError):
        interval = Interval(-100, 100)
        interval_tree.index(interval)


@pytest.mark.parametrize("accelerated", [True, False])
def test_insert(accelerated):
    interval_tree = make_interval_tree(accelerated=accelerated, populated=False)
    interval_tree.add(Interval(1, 3))
    interval_tree.update((Interval(0, 4), Interval(2, 6)))
    assert interval_tree[:] == [
        Interval(start_offset=0, stop_offset=4),
        Interval(start_offset=1, stop_offset=3),
        Interval(start_offset=2, stop_offset=6),
    ]


@pytest.mark.parametrize("accelerated", [True, False])
def test_iterate_moments(accelerated):
    interval_tree = make_interval_tree(accelerated=accelerated, populated=True)
    moments = list(interval_tree.iterate_moments())
    assert [x.start_offset for x in moments] == [0, 1, 2, 6]
    moments = list(interval_tree.iterate_moments(reverse=True))
    assert [x.start_offset for x in moments] == [6, 2, 1, 0]


@pytest.mark.parametrize("accelerated", [True, False])
def test_remove(accelerated):
    intervals = make_intervals()
    interval_tree = make_interval_tree(accelerated=accelerated, populated=True)
    assert list(interval_tree) == sorted(intervals)
    with pytest.raises(ValueError):
        interval_tree.remove(intervals[1:-1])
    assert list(interval_tree) == sorted(intervals)
    for interval in interval_tree[1:-1]:
        interval_tree.remove(interval)
    assert interval_tree[:] == [
        Interval(start_offset=0, stop_offset=3),
        Interval(start_offset=6, stop_offset=9),
    ]


def test_get_offset_after():
    intervals = [
        Interval(0, 3),
        Interval(1, 3),
        Interval(1, 2),
        Interval(2, 5),
        Interval(5, 10),
        Interval(5, 12),
        Interval(6, 9),
        Interval(13, 15),
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
        interval_tree = IntervalTree(intervals)
        actual = [(i, interval_tree.get_offset_after(i)) for i in range(-2, 17)]
        assert actual == expected
        random.shuffle(intervals)
