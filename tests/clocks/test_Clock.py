import os
import platform
import random
import statistics
import time
from typing import Generator

import pytest
from pytest_mock import MockerFixture

from supriya.clocks import CallbackEvent, Clock, ClockContext, TimeUnit

repeat_count = 5


@pytest.fixture
def clock(mocker: MockerFixture) -> Generator[Clock, None, None]:
    clock = Clock()
    clock.slop = 0.001
    mock = mocker.patch.object(Clock, "_get_current_time")
    mock.return_value = 0.0
    yield clock
    clock.stop()


def callback(
    context: ClockContext,
    store: list[ClockContext],
    *,
    blow_up_at: int | None = None,
    delta: float = 0.25,
    limit: int | None = 4,
    time_unit: TimeUnit = TimeUnit.BEATS,
) -> tuple[float, TimeUnit] | None:
    assert isinstance(context.event, CallbackEvent)
    if context.event.invocations == blow_up_at:
        raise Exception
    store.append(context)
    if limit is None:
        return delta, time_unit
    elif context.event.invocations < limit:
        return delta, time_unit
    return None


def set_time_and_check(
    time_to_advance: float, clock: Clock, store: list[ClockContext]
) -> list[tuple[list[float | str], list[float | int], list[float | int]]]:
    clock._get_current_time.return_value = time_to_advance  # type: ignore
    multiplier = 4
    if platform.system() == "Windows":
        multiplier = 40  # Windows CI is really slow
    time.sleep(clock.slop * multiplier)
    return [
        (
            [
                "{}/{}".format(*context.current_moment.time_signature),
                context.current_moment.beats_per_minute,
            ],
            [
                context.current_moment.measure,
                round(context.current_moment.measure_offset, 10),
                context.current_moment.offset,
                context.current_moment.seconds,
            ],
            [
                context.desired_moment.measure,
                round(context.desired_moment.measure_offset, 10),
                context.desired_moment.offset,
                context.desired_moment.seconds,
            ],
        )
        for context in store
    ]


def calculate_skew(store: list[ClockContext]) -> dict[str, float]:
    skews = [
        abs(context.current_moment.seconds - context.desired_moment.seconds)
        for context in store
    ]
    return {
        "min": min(skews),
        "mean": statistics.mean(skews),
        "median": statistics.median(skews),
        "stdev": statistics.stdev(skews),
        "max": max(skews),
    }


@pytest.mark.parametrize(
    "schedule,start_clock_first,expected",
    [
        (True, True, [0.0, 0.25, 0.5, 0.75, 1.0]),
        (True, False, [0.0, 0.25, 0.5, 0.75, 1.0]),
        (False, True, [0.25, 0.5, 0.75, 1.0, 1.25]),
        (False, False, [0.0, 0.25, 0.5, 0.75, 1.0]),
    ],
)
def test_realtime_01(
    schedule: bool, start_clock_first: bool, expected: list[float]
) -> None:
    """
    Start clock, then schedule
    """
    store: list[ClockContext] = []
    clock = Clock()
    assert not clock.is_running
    assert clock.beats_per_minute == 120
    if start_clock_first:
        clock.start()
        assert clock.is_running
        assert clock.beats_per_minute == 120
    if schedule:
        clock.schedule(callback, schedule_at=0.0, args=[store])
    else:
        clock.cue(callback, quantization="1/4", args=[store])
    if not start_clock_first:
        clock.start()
        assert clock.is_running
        assert clock.beats_per_minute == 120
    time.sleep(4)
    clock.stop()
    assert not clock.is_running
    assert clock.beats_per_minute == 120
    assert len(store) == 5
    actual = [context.desired_moment.offset for context in store]
    assert actual == expected


@pytest.mark.parametrize(
    "limit,bpm_schedule,expected",
    [
        (2, [(0.375, 240)], [(0.0, 0.0), (0.25, 0.4375), (0.5, 0.6875)]),
        (2, [(0.5, 240)], [(0.0, 0.0), (0.25, 0.5), (0.5, 0.75)]),
    ],
)
def test_realtime_02(
    limit: int,
    bpm_schedule: list[tuple[float, float]],
    expected: list[tuple[float, float]],
) -> None:
    store: list[ClockContext] = []
    clock = Clock()
    clock.cue(callback, quantization="1/4", args=[store], kwargs=dict(limit=limit))
    for schedule_at, beats_per_minute in bpm_schedule:
        clock.schedule_change(
            beats_per_minute=beats_per_minute,
            schedule_at=schedule_at,
            time_unit=TimeUnit.SECONDS,
        )
    clock.start()
    time.sleep(2)
    clock.stop()
    actual = [
        (
            context.desired_moment.offset,
            context.desired_moment.seconds - clock._state.initial_seconds,
        )
        for context in store
    ]
    assert actual == expected


@pytest.mark.flaky(reruns=5)
def test_basic(clock: Clock) -> None:
    store: list[ClockContext] = []
    clock.start()
    clock.schedule(callback, schedule_at=0.0, args=[store])
    assert set_time_and_check(0.0, clock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0])
    ]
    assert set_time_and_check(0.5, clock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
    ]
    assert set_time_and_check(1.0, clock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [1, 0.5, 0.5, 1.0]),
    ]
    assert set_time_and_check(1.5, clock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [1, 0.5, 0.5, 1.0]),
        (["4/4", 120.0], [1, 0.75, 0.75, 1.5], [1, 0.75, 0.75, 1.5]),
    ]
    assert set_time_and_check(2.0, clock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [1, 0.5, 0.5, 1.0]),
        (["4/4", 120.0], [1, 0.75, 0.75, 1.5], [1, 0.75, 0.75, 1.5]),
        (["4/4", 120.0], [2, 0.0, 1.0, 2.0], [2, 0.0, 1.0, 2.0]),
    ]


@pytest.mark.flaky(reruns=5)
def test_two_procedures(clock: Clock) -> None:
    store_one: list[ClockContext] = []
    store_two: list[ClockContext] = []
    clock.start()
    clock.schedule(callback, schedule_at=0.0, args=[store_one])
    clock.schedule(callback, schedule_at=0.1, args=[store_two], kwargs={"delta": 0.3})
    assert set_time_and_check(0.0, clock, store_one) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0])
    ]
    assert set_time_and_check(0.0, clock, store_two) == []
    assert set_time_and_check(0.5, clock, store_one) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
    ]
    assert set_time_and_check(0.5, clock, store_two) == [
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.1, 0.1, 0.2])
    ]
    assert set_time_and_check(1.0, clock, store_one) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [1, 0.5, 0.5, 1.0]),
    ]
    assert set_time_and_check(1.0, clock, store_two) == [
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.1, 0.1, 0.2]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [1, 0.4, 0.4, 0.8]),
    ]
    assert set_time_and_check(1.5, clock, store_one) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [1, 0.5, 0.5, 1.0]),
        (["4/4", 120.0], [1, 0.75, 0.75, 1.5], [1, 0.75, 0.75, 1.5]),
    ]
    assert set_time_and_check(1.5, clock, store_two) == [
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.1, 0.1, 0.2]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [1, 0.4, 0.4, 0.8]),
        (["4/4", 120.0], [1, 0.75, 0.75, 1.5], [1, 0.7, 0.7, 1.4]),
    ]
    assert set_time_and_check(2.0, clock, store_one) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [1, 0.5, 0.5, 1.0]),
        (["4/4", 120.0], [1, 0.75, 0.75, 1.5], [1, 0.75, 0.75, 1.5]),
        (["4/4", 120.0], [2, 0.0, 1.0, 2.0], [2, 0.0, 1.0, 2.0]),
    ]
    assert set_time_and_check(2.0, clock, store_two) == [
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.1, 0.1, 0.2]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [1, 0.4, 0.4, 0.8]),
        (["4/4", 120.0], [1, 0.75, 0.75, 1.5], [1, 0.7, 0.7, 1.4]),
        (["4/4", 120.0], [2, 0.0, 1.0, 2.0], [2, 0.0, 1.0, 2.0]),
    ]


@pytest.mark.flaky(reruns=5)
def test_exception(clock: Clock) -> None:
    store: list[ClockContext] = []
    clock.start()
    clock.schedule(callback, schedule_at=0.0, args=[store], kwargs={"blow_up_at": 2})
    assert set_time_and_check(0.0, clock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0])
    ]
    assert set_time_and_check(0.5, clock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
    ]
    assert set_time_and_check(1.0, clock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
    ]
    assert set_time_and_check(1.5, clock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
    ]
    assert set_time_and_check(2.0, clock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
    ]


@pytest.mark.flaky(reruns=5)
def test_change_tempo(clock: Clock) -> None:
    store: list[ClockContext] = []
    clock.schedule(callback, schedule_at=0.0, args=[store])
    clock.start()
    assert set_time_and_check(0.0, clock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0])
    ]
    assert set_time_and_check(0.5, clock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
    ]
    clock.change(beats_per_minute=60)
    assert set_time_and_check(1.0, clock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
    ]
    assert set_time_and_check(1.5, clock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
        (["4/4", 60.0], [1, 0.5, 0.5, 1.5], [1, 0.5, 0.5, 1.5]),
    ]
    assert set_time_and_check(2.0, clock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
        (["4/4", 60.0], [1, 0.5, 0.5, 1.5], [1, 0.5, 0.5, 1.5]),
    ]


@pytest.mark.flaky(reruns=5)
def test_schedule_tempo_change(clock: Clock) -> None:
    store: list[ClockContext] = []
    clock.schedule(callback, schedule_at=0.0, args=[store])
    clock.schedule_change(schedule_at=0.5, beats_per_minute=60)
    clock.start()
    assert set_time_and_check(0.0, clock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0])
    ]
    assert set_time_and_check(0.5, clock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
    ]
    assert set_time_and_check(1.0, clock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
        (["4/4", 60.0], [1, 0.5, 0.5, 1.0], [1, 0.5, 0.5, 1.0]),
    ]
    assert set_time_and_check(1.5, clock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
        (["4/4", 60.0], [1, 0.5, 0.5, 1.0], [1, 0.5, 0.5, 1.0]),
    ]
    assert set_time_and_check(2.0, clock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
        (["4/4", 60.0], [1, 0.5, 0.5, 1.0], [1, 0.5, 0.5, 1.0]),
        (["4/4", 60.0], [1, 0.75, 0.75, 2.0], [1, 0.75, 0.75, 2.0]),
    ]
    assert set_time_and_check(2.5, clock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
        (["4/4", 60.0], [1, 0.5, 0.5, 1.0], [1, 0.5, 0.5, 1.0]),
        (["4/4", 60.0], [1, 0.75, 0.75, 2.0], [1, 0.75, 0.75, 2.0]),
    ]


@pytest.mark.flaky(reruns=5)
def test_cue_basic(clock: Clock) -> None:
    store: list[ClockContext] = []
    clock.start()
    clock.cue(callback, quantization=None, args=[store], kwargs={"limit": 0})
    assert set_time_and_check(0.0, clock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0])
    ]
    assert set_time_and_check(0.125, clock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0])
    ]
    clock.cue(callback, quantization="1/4", args=[store], kwargs={"limit": 0})
    clock.cue(callback, quantization="1M", args=[store], kwargs={"limit": 0})
    clock.cue(callback, quantization="1/2T", args=[store], kwargs={"limit": 0})
    assert set_time_and_check(0.5, clock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
    ]
    assert set_time_and_check(0.75, clock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
        (
            ["4/4", 120.0],
            [1, 0.375, 0.375, 0.75],
            [1, 0.3333333333, 0.3333333333333333, 0.6666666666666666],
        ),
    ]
    clock.cue(callback, quantization="1/2T", args=[store], kwargs={"limit": 0})
    assert set_time_and_check(1.0, clock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
        (
            ["4/4", 120.0],
            [1, 0.375, 0.375, 0.75],
            [1, 0.3333333333, 0.3333333333333333, 0.6666666666666666],
        ),
    ]
    assert set_time_and_check(1.5, clock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
        (
            ["4/4", 120.0],
            [1, 0.375, 0.375, 0.75],
            [1, 0.3333333333, 0.3333333333333333, 0.6666666666666666],
        ),
        (
            ["4/4", 120.0],
            [1, 0.75, 0.75, 1.5],
            [1, 0.6666666667, 0.6666666666666666, 1.3333333333333333],
        ),
    ]
    assert set_time_and_check(2.0, clock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
        (
            ["4/4", 120.0],
            [1, 0.375, 0.375, 0.75],
            [1, 0.3333333333, 0.3333333333333333, 0.6666666666666666],
        ),
        (
            ["4/4", 120.0],
            [1, 0.75, 0.75, 1.5],
            [1, 0.6666666667, 0.6666666666666666, 1.3333333333333333],
        ),
        (["4/4", 120.0], [2, 0.0, 1.0, 2.0], [2, 0.0, 1.0, 2.0]),
    ]


@pytest.mark.flaky(reruns=5)
def test_cue_measures(clock: Clock) -> None:
    """
    Measure-wise cueing aligns to offset 0.0
    """
    store: list[ClockContext] = []
    clock.start()
    clock.cue(callback, quantization="1M", args=[store], kwargs={"limit": 0})
    assert set_time_and_check(0.0, clock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0])
    ]
    assert set_time_and_check(0.5, clock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0])
    ]
    clock.cue(callback, quantization="1M", args=[store], kwargs={"limit": 0})
    assert set_time_and_check(2.0, clock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [2, 0.0, 1.0, 2.0], [2, 0.0, 1.0, 2.0]),
    ]


@pytest.mark.flaky(reruns=5)
def test_cue_and_reschedule(clock: Clock) -> None:
    store: list[ClockContext] = []
    clock.start()
    assert set_time_and_check(0.25, clock, store) == []
    clock.cue(callback, quantization="1M", args=[store], kwargs={"limit": 0})
    clock.cue(callback, quantization="2M", args=[store], kwargs={"limit": 0})
    clock.schedule_change(schedule_at=1.0, time_signature=(5, 4))
    assert set_time_and_check(0.5, clock, store) == []
    assert set_time_and_check(1.0, clock, store) == []
    assert set_time_and_check(1.5, clock, store) == []
    assert set_time_and_check(2.0, clock, store) == [
        (["5/4", 120.0], [2, 0.0, 1.0, 2.0], [2, 0.0, 1.0, 2.0])
    ]
    assert set_time_and_check(2.5, clock, store) == [
        (["5/4", 120.0], [2, 0.0, 1.0, 2.0], [2, 0.0, 1.0, 2.0])
    ]
    assert set_time_and_check(3.0, clock, store) == [
        (["5/4", 120.0], [2, 0.0, 1.0, 2.0], [2, 0.0, 1.0, 2.0])
    ]
    assert set_time_and_check(3.5, clock, store) == [
        (["5/4", 120.0], [2, 0.0, 1.0, 2.0], [2, 0.0, 1.0, 2.0])
    ]
    assert set_time_and_check(4.0, clock, store) == [
        (["5/4", 120.0], [2, 0.0, 1.0, 2.0], [2, 0.0, 1.0, 2.0])
    ]
    assert set_time_and_check(4.5, clock, store) == [
        (["5/4", 120.0], [2, 0.0, 1.0, 2.0], [2, 0.0, 1.0, 2.0]),
        (["5/4", 120.0], [3, 0.0, 2.25, 4.5], [3, 0.0, 2.25, 4.5]),
    ]


@pytest.mark.flaky(reruns=5)
def test_reschedule_earlier(clock: Clock) -> None:
    store: list[ClockContext] = []
    clock.start()
    assert set_time_and_check(0.5, clock, store) == []
    event_id = clock.cue(callback, quantization="1M", args=[store], kwargs={"limit": 0})
    time.sleep(clock.slop * 2)
    assert (event := clock._peek()) is not None and event.seconds == 2.0
    clock.reschedule(event_id, schedule_at=0.5)
    time.sleep(clock.slop * 2)
    assert (event := clock._peek()) is not None and event.seconds == 1.0
    assert set_time_and_check(2.0, clock, store) == [
        (["4/4", 120.0], [2, 0.0, 1.0, 2.0], [1, 0.5, 0.5, 1.0])
    ]


@pytest.mark.flaky(reruns=5)
def test_reschedule_later(clock: Clock) -> None:
    store: list[ClockContext] = []
    clock.start()
    assert set_time_and_check(0.5, clock, store) == []
    event_id = clock.cue(callback, quantization="1M", args=[store], kwargs={"limit": 0})
    time.sleep(clock.slop * 2)
    assert (event := clock._peek()) is not None and event.seconds == 2.0
    clock.reschedule(event_id, schedule_at=1.5)
    time.sleep(clock.slop * 2)
    assert (event := clock._peek()) is not None and event.seconds == 3.0
    assert set_time_and_check(3.0, clock, store) == [
        (["4/4", 120.0], [2, 0.5, 1.5, 3.0], [2, 0.5, 1.5, 3.0])
    ]


def test_change_tempo_not_running(clock: Clock) -> None:
    assert clock.beats_per_minute == 120
    assert clock.time_signature == (4, 4)
    clock.change(beats_per_minute=135, time_signature=(3, 4))
    assert clock.beats_per_minute == 135
    assert clock.time_signature == (3, 4)


@pytest.mark.flaky(reruns=5)
def test_change_time_signature_on_downbeat(clock: Clock) -> None:
    store: list[ClockContext] = []
    clock.change(beats_per_minute=240)
    clock.schedule(
        callback,
        schedule_at=0.0,
        args=[store],
        kwargs={"delta": 1, "time_unit": TimeUnit.MEASURES},
    )
    clock.start()
    assert set_time_and_check(0.0, clock, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0])
    ]
    clock.schedule_change(schedule_at=2, time_signature=(3, 4))
    assert set_time_and_check(1.0, clock, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [2, 0.0, 1.0, 1.0]),
    ]
    assert set_time_and_check(2.0, clock, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [2, 0.0, 1.0, 1.0]),
        (["3/4", 240], [3, 0.0, 2.0, 2.0], [3, 0.0, 2.0, 2.0]),
    ]
    assert set_time_and_check(3.0, clock, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [2, 0.0, 1.0, 1.0]),
        (["3/4", 240], [3, 0.0, 2.0, 2.0], [3, 0.0, 2.0, 2.0]),
        (["3/4", 240], [4, 0.25, 3.0, 3.0], [4, 0.0, 2.75, 2.75]),
    ]


@pytest.mark.flaky(reruns=5)
def test_change_time_signature_on_downbeat_laggy(clock: Clock) -> None:
    store: list[ClockContext] = []
    clock.change(beats_per_minute=240)
    clock.schedule(
        callback,
        schedule_at=0.0,
        args=[store],
        kwargs={"delta": 1, "time_unit": TimeUnit.MEASURES},
    )
    clock.start()
    assert set_time_and_check(0.0, clock, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0])
    ]
    clock.schedule_change(schedule_at=2, time_signature=(3, 4))
    assert set_time_and_check(3.0, clock, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 240], [4, 0.0, 3.0, 3.0], [2, 0.0, 1.0, 1.0]),
        (["3/4", 240], [4, 0.25, 3.0, 3.0], [3, 0.0, 2.0, 2.0]),
        (["3/4", 240], [4, 0.25, 3.0, 3.0], [4, 0.0, 2.75, 2.75]),
    ]


@pytest.mark.flaky(reruns=5)
def test_change_time_signature_late(clock: Clock) -> None:
    store: list[ClockContext] = []
    clock.change(beats_per_minute=240)
    clock.schedule(
        callback,
        schedule_at=0.0,
        args=[store],
        kwargs={"delta": 1, "time_unit": TimeUnit.MEASURES},
    )
    clock.start()
    assert set_time_and_check(0.0, clock, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0])
    ]
    clock.schedule_change(schedule_at=1.875, time_signature=(3, 4))
    assert set_time_and_check(1.0, clock, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [2, 0.0, 1.0, 1.0]),
    ]
    assert set_time_and_check(2.0, clock, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [2, 0.0, 1.0, 1.0]),
        (["3/4", 240], [3, 0.125, 2.0, 2.0], [3, 0.0, 1.875, 1.875]),
    ]
    assert set_time_and_check(3.0, clock, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [2, 0.0, 1.0, 1.0]),
        (["3/4", 240], [3, 0.125, 2.0, 2.0], [3, 0.0, 1.875, 1.875]),
        (["3/4", 240], [4, 0.375, 3.0, 3.0], [4, 0.0, 2.625, 2.625]),
    ]


@pytest.mark.flaky(reruns=5)
def test_change_time_signature_late_laggy(clock: Clock) -> None:
    store: list[ClockContext] = []
    clock.change(beats_per_minute=240)
    clock.schedule(
        callback,
        schedule_at=0.0,
        args=[store],
        kwargs={"delta": 1, "time_unit": TimeUnit.MEASURES},
    )
    clock.start()
    assert set_time_and_check(0.0, clock, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0])
    ]
    clock.schedule_change(schedule_at=1.875, time_signature=(3, 4))
    assert set_time_and_check(3.0, clock, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 240], [4, 0.0, 3.0, 3.0], [2, 0.0, 1.0, 1.0]),
        (["3/4", 240], [4, 0.375, 3.0, 3.0], [3, 0.0, 1.875, 1.875]),
        (["3/4", 240], [4, 0.375, 3.0, 3.0], [4, 0.0, 2.625, 2.625]),
    ]


@pytest.mark.flaky(reruns=5)
def test_change_time_signature_early(clock: Clock) -> None:
    store: list[ClockContext] = []
    clock.change(beats_per_minute=240)
    clock.schedule(
        callback,
        schedule_at=0.0,
        args=[store],
        kwargs={"delta": 1, "time_unit": TimeUnit.MEASURES},
    )
    clock.start()
    assert set_time_and_check(0.0, clock, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0])
    ]
    clock.schedule_change(schedule_at=1.125, time_signature=(5, 4))
    assert set_time_and_check(1.0, clock, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [2, 0.0, 1.0, 1.0]),
    ]
    assert clock.time_signature == (4, 4)
    assert set_time_and_check(2.0, clock, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [2, 0.0, 1.0, 1.0]),
    ]
    assert clock.time_signature == (5, 4)
    assert set_time_and_check(3.0, clock, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [2, 0.0, 1.0, 1.0]),
        (["5/4", 240], [3, 0.75, 3.0, 3.0], [3, 0.0, 2.25, 2.25]),
    ]


@pytest.mark.flaky(reruns=5)
def test_change_time_signature_early_laggy(clock: Clock) -> None:
    store: list[ClockContext] = []
    clock.change(beats_per_minute=240)
    clock.schedule(
        callback,
        schedule_at=0.0,
        args=[store],
        kwargs={"delta": 1, "time_unit": TimeUnit.MEASURES},
    )
    clock.start()
    assert set_time_and_check(0.0, clock, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0])
    ]
    clock.schedule_change(schedule_at=1.125, time_signature=(5, 4))
    assert set_time_and_check(3.0, clock, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 240], [4, 0.0, 3.0, 3.0], [2, 0.0, 1.0, 1.0]),
        (["5/4", 240], [3, 0.75, 3.0, 3.0], [3, 0.0, 2.25, 2.25]),  # time travel
    ]


@pytest.mark.flaky(reruns=5)
def test_change_time_signature_shrinking(clock: Clock) -> None:
    """
    When shifting to a smaller time signature, if the desired measure offset is
    within that smaller time signature, maintain the desired measure and
    measure offset.
    """
    store: list[ClockContext] = []
    clock.change(beats_per_minute=240)
    clock.schedule(callback, schedule_at=0.0, args=[store], kwargs={"limit": 12})
    clock.schedule_change(schedule_at=1.125, time_signature=(2, 4))
    clock.start()
    assert set_time_and_check(1.0, clock, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [1, 0.25, 0.25, 0.25]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [1, 0.5, 0.5, 0.5]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [1, 0.75, 0.75, 0.75]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [2, 0.0, 1.0, 1.0]),
    ]
    assert set_time_and_check(1.25, clock, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [1, 0.25, 0.25, 0.25]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [1, 0.5, 0.5, 0.5]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [1, 0.75, 0.75, 0.75]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [2, 0.0, 1.0, 1.0]),
        (["2/4", 240], [2, 0.25, 1.25, 1.25], [2, 0.25, 1.25, 1.25]),
    ]
    assert set_time_and_check(1.5, clock, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [1, 0.25, 0.25, 0.25]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [1, 0.5, 0.5, 0.5]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [1, 0.75, 0.75, 0.75]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [2, 0.0, 1.0, 1.0]),
        (["2/4", 240], [2, 0.25, 1.25, 1.25], [2, 0.25, 1.25, 1.25]),
        (["2/4", 240], [3, 0.0, 1.5, 1.5], [3, 0.0, 1.5, 1.5]),
    ]


@pytest.mark.flaky(reruns=5)
def test_schedule_measure_relative(clock: Clock) -> None:
    store: list[ClockContext] = []
    clock.change(beats_per_minute=240)
    clock.schedule(
        callback,
        schedule_at=3,
        time_unit=TimeUnit.MEASURES,
        args=[store],
        kwargs={"limit": 0},
    )
    clock.start()
    assert set_time_and_check(0.0, clock, store) == []
    assert set_time_and_check(4.0, clock, store) == [
        (["4/4", 240], [5, 0.0, 4.0, 4.0], [3, 0.0, 2.0, 2.0])
    ]


@pytest.mark.flaky(reruns=5)
def test_schedule_seconds_relative(clock: Clock) -> None:
    store: list[ClockContext] = []
    clock.change(beats_per_minute=240)
    clock.schedule(
        callback,
        schedule_at=1.234,
        time_unit=TimeUnit.SECONDS,
        args=[store],
        kwargs={"limit": 0},
    )
    clock.start()
    assert set_time_and_check(0.0, clock, store) == []
    assert set_time_and_check(4.0, clock, store) == [
        (["4/4", 240], [5, 0.0, 4.0, 4.0], [2, 0.234, 1.234, 1.234])
    ]


def test_cancel_invalid(clock: Clock) -> None:
    clock.start()
    assert clock.cancel(1) is None


def test_slop(clock: Clock) -> None:
    assert clock.slop == 0.001
    clock.slop = 0.1
    assert clock.slop == 0.1
    with pytest.raises(ValueError):
        clock.slop = 0
    with pytest.raises(ValueError):
        clock.slop = -1.0


def test_start_and_restart(clock: Clock) -> None:
    assert not clock.is_running
    clock.start()
    assert clock.is_running
    with pytest.raises(RuntimeError):
        clock.start()
    assert clock.is_running


def test_stop_and_restop(clock: Clock) -> None:
    assert not clock.is_running
    clock.start()
    assert clock.is_running
    clock.stop()
    assert not clock.is_running
    clock.stop()
    assert not clock.is_running


@pytest.mark.flaky(reruns=5)
def test_clock_skew() -> None:
    clock = Clock()
    clock.slop = 0.0001
    all_stats = []
    for _ in range(5):
        store: list[ClockContext] = []
        for _ in range(20):
            delta = random.random() / 100
            clock.schedule(
                callback,
                schedule_at=random.random(),
                args=[store],
                kwargs={"limit": 50, "delta": delta, "time_unit": TimeUnit.SECONDS},
            )
        clock.start()
        time.sleep(2.5)
        clock.stop()
        stats = calculate_skew(store)
        all_stats.append(stats)
    multiplier = 1.5
    if os.environ.get("CI"):
        if platform.system() == "Darwin":
            multiplier = 7.0  # GHA's OSX runner is slow!
        elif platform.system() == "Windows":
            multiplier = 75.0  # GHA's Windows runner is extremely slow! WTF.
    threshold = clock.slop * multiplier
    medians = [stats["median"] for stats in all_stats]
    assert all(median < threshold for median in medians), (medians, threshold)
