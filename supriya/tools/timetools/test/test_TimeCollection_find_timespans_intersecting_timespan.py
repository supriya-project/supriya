# -*- encoding: utf-8 -*-
import pytest
import random
from abjad.tools import sequencetools
from abjad.tools import timespantools
from supriya import timetools


pairs = []
for _ in range(3):
    timespan_collection = timetools.TimespanCollection()
    start_offset = 0
    for _ in range(5):
        duration = random.randint(1, 5)
        stop_offset = start_offset + duration
        timespan = timespantools.Timespan(
            start_offset=start_offset,
            stop_offset=stop_offset,
            )
        timespan_collection.insert(timespan)
        start_offset += stop_offset
    start_offset = int(timespan_collection.start_offset - 1)
    stop_offset = int(timespan_collection.stop_offset + 1)
    indices = tuple(range(start_offset, stop_offset + 1))
    for pair in \
        sequencetools.yield_all_unordered_pairs_of_sequence(indices):
        start_offset, stop_offset = sorted(pair)
        target_timespan = timespantools.Timespan(
            start_offset=start_offset,
            stop_offset=stop_offset,
            )
        pairs.append((timespan_collection, target_timespan))


@pytest.mark.parametrize('pair', pairs)
def test_TimeCollection_find_timespans_intersecting_timespan_01(pair):
    r'''Non-overlapping.'''
    found_by_search = set(
        timespan_collection.find_timespans_intersecting_timespan(
            target_timespan))
    found_by_brute_force = set()
    for _ in timespan_collection:
        if _.intersects_timespan(target_timespan):
            found_by_brute_force.add(_)
    if not found_by_search == found_by_brute_force:
        print(format(timespan_collection))
        print(target_timespan)
        print(found_by_search)
        print(found_by_brute_force)
        raise AssertionError


pairs = []
for _ in range(3):
    timespan_collection = timetools.TimespanCollection()
    for _ in range(5):
        offset_a = random.randint(1, 9)
        offset_b = random.randint(1, 9)
        while offset_b == offset_a:
            offset_b = random.randint(1, 9)
        start_offset, stop_offset = sorted([offset_a, offset_b])
        timespan = timespantools.Timespan(
            start_offset=start_offset,
            stop_offset=stop_offset,
            )
        timespan_collection.insert(timespan)
    start_offset = int(timespan_collection.start_offset - 1)
    stop_offset = int(timespan_collection.stop_offset + 1)
    indices = tuple(range(start_offset, stop_offset + 1))
    for pair in \
        sequencetools.yield_all_unordered_pairs_of_sequence(indices):
        start_offset, stop_offset = sorted(pair)
        target_timespan = timespantools.Timespan(
            start_offset=start_offset,
            stop_offset=stop_offset,
            )
        pairs.append((timespan_collection, target_timespan))


@pytest.mark.parametrize('pair', pairs)
def test_TimeCollection_find_timespans_intersecting_timespan_02(pair):
    r'''Non-overlapping.'''
    found_by_search = set(
        timespan_collection.find_timespans_intersecting_timespan(
            target_timespan))
    found_by_brute_force = set()
    for _ in timespan_collection:
        if _.intersects_timespan(target_timespan):
            found_by_brute_force.add(_)
    if not found_by_search == found_by_brute_force:
        print(format(timespan_collection))
        print(target_timespan)
        print(found_by_search)
        print(found_by_brute_force)
        raise AssertionError