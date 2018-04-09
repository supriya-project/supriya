import itertools
import pytest
import random
from abjad import Offset, Timespan
from abjad import timespantools
from supriya import timetools
from supriya import systemtools
from supriya.tools.timetools import (
    TimespanCollectionDriver,
    TimespanCollectionDriverEx,
    TimespanSimultaneity,
    )


class TestCase(systemtools.TestCase):

    accelerated = False

    def make_expected_start_offsets(self, range_=10, timespans=None):
        if not timespans:
            timespans = self.make_timespans()
        actual_offsets = set()
        for timespan in timespans:
            actual_offsets.add(float(timespan.start_offset))
        actual_offsets = sorted(actual_offsets)
        print('    O:', actual_offsets)
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

    def make_simultaneity_fixtures(self, range_=10, timespans=None):
        if not timespans:
            timespans = self.make_timespans()
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

    def make_timespans(self):
        return [
            timespantools.Timespan(0, 3),
            timespantools.Timespan(1, 3),
            timespantools.Timespan(1, 2),
            timespantools.Timespan(2, 5),
            timespantools.Timespan(6, 9),
            ]

    def make_timespan_collection(self, populated=True, timespans=None):
        if populated and not timespans:
            timespans = self.make_timespans()
        timespan_collection = timetools.TimespanCollection(
            timespans=timespans,
            accelerated=self.accelerated,
            )
        if self.accelerated:
            assert isinstance(
                timespan_collection._driver,
                TimespanCollectionDriverEx,
                )
        else:
            assert isinstance(
                timespan_collection._driver,
                TimespanCollectionDriver,
                )
        return timespan_collection

    def make_random_timespans(self, count=10, range_=10):
        indices = list(range(range_))
        timespans = []
        for _ in range(count):
            random.shuffle(indices)
            start_offset, stop_offset = sorted(indices[:2])
            timespan = timespantools.Timespan(
                start_offset=start_offset,
                stop_offset=stop_offset,
                )
            timespans.append(timespan)
        return timespans

    def make_target_timespans(self, range_=10):
        indices = list(range(range_))
        timespans = []
        for pair in itertools.permutations(indices, 2):
            start_offset, stop_offset = sorted(pair)
            target_timespan = timespantools.Timespan(
                start_offset=start_offset,
                stop_offset=stop_offset,
                )
            timespans.append(target_timespan)
        return timespans

    def test___contains__(self):
        timespans = self.make_timespans()
        timespan_collection = self.make_timespan_collection(populated=True)
        assert timespans[0] in timespan_collection
        assert timespantools.Timespan(-1, 100) not in timespan_collection
        timespan_collection.remove(timespans[-1])
        assert timespans[-1] not in timespan_collection

    def test___getitem__(self):
        timespan_collection = self.make_timespan_collection(populated=True)
        assert timespan_collection[-1] == timespantools.Timespan(6, 9)
        assert [timespan for timespan in timespan_collection[:3]] == [
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(3, 1)),
            Timespan(start_offset=Offset(1, 1), stop_offset=Offset(2, 1)),
            Timespan(start_offset=Offset(1, 1), stop_offset=Offset(3, 1)),
            ]

    def test___init__(self):
        self.make_timespan_collection(populated=False)
        self.make_timespan_collection(populated=True)

    def test___iter__(self):
        timespan_collection = self.make_timespan_collection(populated=True)
        assert [timespan for timespan in timespan_collection] == [
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(3, 1)),
            Timespan(start_offset=Offset(1, 1), stop_offset=Offset(2, 1)),
            Timespan(start_offset=Offset(1, 1), stop_offset=Offset(3, 1)),
            Timespan(start_offset=Offset(2, 1), stop_offset=Offset(5, 1)),
            Timespan(start_offset=Offset(6, 1), stop_offset=Offset(9, 1)),
            ]
        iterator = iter(timespan_collection)
        assert next(iterator) == \
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(3, 1))

    def test___len__(self):
        timespan_collection = self.make_timespan_collection(populated=False)
        assert len(timespan_collection) == 0
        timespan_collection = self.make_timespan_collection(populated=True)
        assert len(timespan_collection) == 5

    def test___setitem__(self):
        timespan_collection = self.make_timespan_collection(populated=True)
        timespan_collection[-1] = Timespan(-1, 4)
        assert [timespan for timespan in timespan_collection] == [
            Timespan(start_offset=Offset(-1, 1), stop_offset=Offset(4, 1)),
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(3, 1)),
            Timespan(start_offset=Offset(1, 1), stop_offset=Offset(2, 1)),
            Timespan(start_offset=Offset(1, 1), stop_offset=Offset(3, 1)),
            Timespan(start_offset=Offset(2, 1), stop_offset=Offset(5, 1)),
            ]
        timespan_collection[:3] = Timespan(100, 200)
        assert [timespan for timespan in timespan_collection] == [
            Timespan(start_offset=Offset(1, 1), stop_offset=Offset(3, 1)),
            Timespan(start_offset=Offset(2, 1), stop_offset=Offset(5, 1)),
            Timespan(start_offset=Offset(100, 1), stop_offset=Offset(200, 1)),
            ]

    def test___sub__(self):
        timespan_collection = self.make_timespan_collection(
            timespans=[
                timespantools.Timespan(0, 16),
                timespantools.Timespan(5, 12),
                timespantools.Timespan(-2, 8),
                ],
            )
        timespan = timespantools.Timespan(5, 10)
        result = timespan_collection - timespan
        assert result[:] == [
            timespantools.Timespan(-2, 5),
            timespantools.Timespan(0, 5),
            timespantools.Timespan(10, 12),
            timespantools.Timespan(10, 16),
            ]

    @pytest.mark.timeout(60)
    def test_find_intersection_with_offset(self):
        iterations = 100
        count, range_ = 10, 15
        for i in range(iterations):
            with self.subTest(i=i):
                timespans = self.make_random_timespans(
                    count=count, range_=range_)
                timespan_collection = self.make_timespan_collection(
                    timespans=timespans)
                for offset in range(range_):
                    found_by_search = set(
                        timespan_collection.find_intersection(offset))
                    found_by_brute_force = set()
                    for _ in timespan_collection:
                        if _.start_offset <= offset < _.stop_offset:
                            found_by_brute_force.add(_)
                    assert found_by_search == found_by_brute_force

    @pytest.mark.timeout(120)
    def test_find_intersection_with_timespan(self):
        iterations = 100
        count, range_ = 10, 15
        target_timespans = self.make_target_timespans(range_=range_)
        for i in range(iterations):
            with self.subTest(i=i):
                timespans = self.make_random_timespans(
                    count=count, range_=range_)
                timespan_collection = self.make_timespan_collection(
                    timespans=timespans)
                for target_timespan in target_timespans:
                    found_by_search = set(
                        timespan_collection.find_intersection(target_timespan))
                    found_by_brute_force = set()
                    for _ in timespan_collection:
                        if _.intersects_timespan(target_timespan):
                            found_by_brute_force.add(_)
                    assert found_by_search == found_by_brute_force

    @pytest.mark.timeout(60)
    def test_find_timespans_starting_at(self):
        iterations = 100
        count, range_ = 10, 15
        for i in range(iterations):
            with self.subTest(i=i):
                timespans = self.make_random_timespans(
                    count=count, range_=range_)
                timespan_collection = self.make_timespan_collection(
                    timespans=timespans)
                for offset in range(range_):
                    found_by_search = set(
                        timespan_collection.find_timespans_starting_at(offset))
                    found_by_brute_force = set()
                    for _ in timespan_collection:
                        if _.start_offset == offset:
                            found_by_brute_force.add(_)
                    assert found_by_search == found_by_brute_force

    @pytest.mark.timeout(60)
    def test_find_timespans_stopping_at(self):
        iterations = 100
        count, range_ = 10, 15
        for i in range(iterations):
            with self.subTest(i=i):
                timespans = self.make_random_timespans(
                    count=count, range_=range_)
                timespan_collection = self.make_timespan_collection(
                    timespans=timespans)
                for offset in range(range_):
                    found_by_search = set(
                        timespan_collection.find_timespans_stopping_at(offset))
                    found_by_brute_force = set()
                    for _ in timespan_collection:
                        if _.stop_offset == offset:
                            found_by_brute_force.add(_)
                    assert found_by_search == found_by_brute_force

    @pytest.mark.timeout(60)
    def test_get_simultaneity_at(self):
        iterations = 100
        count, range_ = 10, 15
        for i in range(iterations):
            with self.subTest(i=i):
                timespans = self.make_random_timespans(
                    count=count, range_=range_)
                timespan_collection = self.make_timespan_collection(
                    timespans=timespans)
                fixtures = self.make_simultaneity_fixtures(
                    range_=range_, timespans=timespans)
                for offset in range(range_):
                    overlaps, starts, stops = fixtures[offset]
                    expected = TimespanSimultaneity(
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
    def test_get_start_offset(self):
        iterations = 100
        count, range_ = 10, 15
        for i in range(iterations):
            with self.subTest(i=i):
                print('Iteration:', i)
                timespans = self.make_random_timespans(
                    count=count, range_=range_)
                timespan_collection = self.make_timespan_collection(
                    timespans=timespans)
                expected_offsets = self.make_expected_start_offsets(
                    range_=range_, timespans=timespans)
                for timespan in sorted(timespans):
                    print('    Timespan:', timespan)
                for offset in range(-1, range_ + 1):
                    print('    Offset:', offset)
                    print('        :', expected_offsets[offset])
                    expected_before, expected_after = expected_offsets[offset]
                    actual_before = \
                        timespan_collection.get_start_offset_before(offset)
                    actual_after = \
                        timespan_collection.get_start_offset_after(offset)
                    assert expected_before == actual_before, offset
                    assert expected_after == actual_after, offset

    def test_index(self):
        timespans = self.make_timespans()
        timespan_collection = self.make_timespan_collection(populated=True)
        assert timespan_collection.index(timespans[0]) == 0
        assert timespan_collection.index(timespans[1]) == 2
        assert timespan_collection.index(timespans[2]) == 1
        assert timespan_collection.index(timespans[3]) == 3
        assert timespan_collection.index(timespans[4]) == 4
        with self.assertRaises(ValueError):
            timespan = Timespan(-100, 100)
            timespan_collection.index(timespan)

    def test_insert(self):
        timespan_collection = self.make_timespan_collection(populated=False)
        timespan_collection.insert(timespantools.Timespan(1, 3))
        timespan_collection.insert((
            timespantools.Timespan(0, 4),
            timespantools.Timespan(2, 6),
            ))
        assert timespan_collection[:] == [
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(4, 1)),
            Timespan(start_offset=Offset(1, 1), stop_offset=Offset(3, 1)),
            Timespan(start_offset=Offset(2, 1), stop_offset=Offset(6, 1)),
            ]

    def test_iterate_simultaneities(self):
        timespan_collection = self.make_timespan_collection(populated=True)
        simultaneities = list(timespan_collection.iterate_simultaneities())
        assert [x.start_offset for x in simultaneities] == [0, 1, 2, 6]
        simultaneities = list(timespan_collection.iterate_simultaneities(
            reverse=True))
        assert [x.start_offset for x in simultaneities] == [6, 2, 1, 0]

    def test_remove(self):
        timespans = self.make_timespans()
        timespan_collection = self.make_timespan_collection(populated=True)
        timespan_collection.remove(timespans[1:-1])
        assert timespan_collection[:] == [
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(3, 1)),
            Timespan(start_offset=Offset(6, 1), stop_offset=Offset(9, 1)),
            ]
