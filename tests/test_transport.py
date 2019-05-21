import random
import statistics
import time

import pytest

from supriya.transport import TimeUnit, Transport


@pytest.fixture
def transport(mocker):
    transport = Transport()
    transport.slop = 0.001
    mock = mocker.patch.object(Transport, "get_current_time")
    mock.return_value = 0.0
    yield transport
    transport.stop()


def callback(
    current_moment,
    desired_moment,
    event,
    store,
    blow_up_at=None,
    delta=0.25,
    limit=4,
    unit=TimeUnit.BEATS,
    **kwargs,
):
    if event.invocations == blow_up_at:
        raise Exception
    store.append((current_moment, desired_moment, event))
    if limit is None:
        return delta, unit
    elif event.invocations < limit:
        return delta, unit
    return None


def set_time_and_check(time_to_advance, transport, store):
    transport.get_current_time.return_value = time_to_advance
    time.sleep(transport.slop * 2)
    moments = []
    for current_moment, desired_moment, event in store:
        one = [
            "{}/{}".format(*current_moment.time_signature),
            current_moment.beats_per_minute,
        ]
        two = [
            current_moment.measure,
            round(current_moment.measure_offset, 10),
            current_moment.offset,
            current_moment.time,
        ]
        three = [
            desired_moment.measure,
            round(desired_moment.measure_offset, 10),
            desired_moment.offset,
            desired_moment.time,
        ]
        moments.append((one, two, three))
    return moments


def calculate_skew(store):
    skews = [
        abs(current_moment.time - desired_moment.time)
        for current_moment, desired_moment, event in store
    ]
    return {
        "min": min(skews),
        "mean": statistics.mean(skews),
        "median": statistics.median(skews),
        "stdev": statistics.stdev(skews),
        "max": max(skews),
    }


@pytest.mark.timeout(5)
def test_realtime_01():
    store = []
    transport = Transport()
    assert not transport.is_running
    assert transport.beats_per_minute == 120
    transport.start()
    assert transport.is_running
    assert transport.beats_per_minute == 120
    transport.schedule(callback, schedule_at=0.0, args=[store])
    time.sleep(4)
    transport.stop()
    assert not transport.is_running
    assert transport.beats_per_minute == 120
    assert len(store) == 5
    assert [
        desired_moment.offset for current_moment, desired_moment, event in store
    ] == [0.0, 0.25, 0.5, 0.75, 1.0]


@pytest.mark.timeout(5)
def test_basic(transport):
    store = []
    transport.start()
    transport.schedule(callback, schedule_at=0.0, args=[store])
    assert set_time_and_check(0.0, transport, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0])
    ]
    assert set_time_and_check(0.5, transport, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
    ]
    assert set_time_and_check(1.0, transport, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [1, 0.5, 0.5, 1.0]),
    ]
    assert set_time_and_check(1.5, transport, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [1, 0.5, 0.5, 1.0]),
        (["4/4", 120.0], [1, 0.75, 0.75, 1.5], [1, 0.75, 0.75, 1.5]),
    ]
    assert set_time_and_check(2.0, transport, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [1, 0.5, 0.5, 1.0]),
        (["4/4", 120.0], [1, 0.75, 0.75, 1.5], [1, 0.75, 0.75, 1.5]),
        (["4/4", 120.0], [2, 0.0, 1.0, 2.0], [2, 0.0, 1.0, 2.0]),
    ]


@pytest.mark.timeout(5)
def test_two_procedures(transport):
    store_one = []
    store_two = []
    transport.start()
    transport.schedule(callback, schedule_at=0.0, args=[store_one])
    transport.schedule(
        callback, schedule_at=0.1, args=[store_two], kwargs={"delta": 0.3}
    )
    assert set_time_and_check(0.0, transport, store_one) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0])
    ]
    assert set_time_and_check(0.0, transport, store_two) == []
    assert set_time_and_check(0.5, transport, store_one) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
    ]
    assert set_time_and_check(0.5, transport, store_two) == [
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.1, 0.1, 0.2])
    ]
    assert set_time_and_check(1.0, transport, store_one) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [1, 0.5, 0.5, 1.0]),
    ]
    assert set_time_and_check(1.0, transport, store_two) == [
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.1, 0.1, 0.2]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [1, 0.4, 0.4, 0.8]),
    ]
    assert set_time_and_check(1.5, transport, store_one) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [1, 0.5, 0.5, 1.0]),
        (["4/4", 120.0], [1, 0.75, 0.75, 1.5], [1, 0.75, 0.75, 1.5]),
    ]
    assert set_time_and_check(1.5, transport, store_two) == [
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.1, 0.1, 0.2]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [1, 0.4, 0.4, 0.8]),
        (["4/4", 120.0], [1, 0.75, 0.75, 1.5], [1, 0.7, 0.7, 1.4]),
    ]
    assert set_time_and_check(2.0, transport, store_one) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [1, 0.5, 0.5, 1.0]),
        (["4/4", 120.0], [1, 0.75, 0.75, 1.5], [1, 0.75, 0.75, 1.5]),
        (["4/4", 120.0], [2, 0.0, 1.0, 2.0], [2, 0.0, 1.0, 2.0]),
    ]
    assert set_time_and_check(2.0, transport, store_two) == [
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.1, 0.1, 0.2]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [1, 0.4, 0.4, 0.8]),
        (["4/4", 120.0], [1, 0.75, 0.75, 1.5], [1, 0.7, 0.7, 1.4]),
        (["4/4", 120.0], [2, 0.0, 1.0, 2.0], [2, 0.0, 1.0, 2.0]),
    ]


@pytest.mark.timeout(5)
def test_exception(transport):
    store = []
    transport.start()
    transport.schedule(
        callback, schedule_at=0.0, args=[store], kwargs={"blow_up_at": 2}
    )
    assert set_time_and_check(0.0, transport, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0])
    ]
    assert set_time_and_check(0.5, transport, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
    ]
    assert set_time_and_check(1.0, transport, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
    ]
    assert set_time_and_check(1.5, transport, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
    ]
    assert set_time_and_check(2.0, transport, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
    ]


@pytest.mark.timeout(5)
def test_change_tempo(transport):
    store = []
    transport.schedule(callback, schedule_at=0.0, args=[store])
    transport.start()
    assert set_time_and_check(0.0, transport, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0])
    ]
    assert set_time_and_check(0.5, transport, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
    ]
    transport.change(beats_per_minute=60)
    assert set_time_and_check(1.0, transport, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
    ]
    assert set_time_and_check(1.5, transport, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
        (["4/4", 60.0], [1, 0.5, 0.5, 1.5], [1, 0.5, 0.5, 1.5]),
    ]
    assert set_time_and_check(2.0, transport, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
        (["4/4", 60.0], [1, 0.5, 0.5, 1.5], [1, 0.5, 0.5, 1.5]),
    ]


@pytest.mark.timeout(5)
def test_schedule_tempo_change(transport):
    store = []
    transport.schedule(callback, schedule_at=0.0, args=[store])
    transport.schedule_change(schedule_at=0.5, beats_per_minute=60)
    transport.start()
    assert set_time_and_check(0.0, transport, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0])
    ]
    assert set_time_and_check(0.5, transport, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
    ]
    assert set_time_and_check(1.0, transport, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [1, 0.5, 0.5, 1.0]),
    ]
    assert set_time_and_check(1.5, transport, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [1, 0.5, 0.5, 1.0]),
    ]
    assert set_time_and_check(2.0, transport, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [1, 0.5, 0.5, 1.0]),
        (["4/4", 60.0], [1, 0.75, 0.75, 2.0], [1, 0.75, 0.75, 2.0]),
    ]
    assert set_time_and_check(2.5, transport, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [1, 0.5, 0.5, 1.0]),
        (["4/4", 60.0], [1, 0.75, 0.75, 2.0], [1, 0.75, 0.75, 2.0]),
    ]


@pytest.mark.timeout(5)
def test_cue_basic(transport):
    store = []
    transport.start()
    transport.cue(callback, quantization=None, args=[store], kwargs={"limit": 0})
    assert set_time_and_check(0.0, transport, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0])
    ]
    assert set_time_and_check(0.125, transport, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0])
    ]
    transport.cue(callback, quantization="1/4", args=[store], kwargs={"limit": 0})
    transport.cue(callback, quantization="1M", args=[store], kwargs={"limit": 0})
    transport.cue(callback, quantization="1/2T", args=[store], kwargs={"limit": 0})
    assert set_time_and_check(0.5, transport, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
    ]
    assert set_time_and_check(0.75, transport, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
        (
            ["4/4", 120.0],
            [1, 0.375, 0.375, 0.75],
            [1, 0.3333333333, 0.3333333333333333, 0.6666666666666666],
        ),
    ]
    transport.cue(callback, quantization="1/2T", args=[store], kwargs={"limit": 0})
    assert set_time_and_check(1.0, transport, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
        (
            ["4/4", 120.0],
            [1, 0.375, 0.375, 0.75],
            [1, 0.3333333333, 0.3333333333333333, 0.6666666666666666],
        ),
    ]
    assert set_time_and_check(1.5, transport, store) == [
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
    assert set_time_and_check(2.0, transport, store) == [
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


@pytest.mark.timeout(5)
def test_cue_and_reschedule(transport):
    store = []
    transport.start()
    transport.cue(callback, quantization="1M", args=[store], kwargs={"limit": 0})
    transport.cue(callback, quantization="2M", args=[store], kwargs={"limit": 0})
    transport.schedule_change(schedule_at=1.0, time_signature=(5, 4))
    assert set_time_and_check(0.5, transport, store) == []
    assert set_time_and_check(1.0, transport, store) == []
    assert set_time_and_check(1.5, transport, store) == []
    assert set_time_and_check(2.0, transport, store) == [
        (["5/4", 120.0], [2, 0.0, 1.0, 2.0], [2, 0.0, 1.0, 2.0])
    ]
    assert set_time_and_check(2.5, transport, store) == [
        (["5/4", 120.0], [2, 0.0, 1.0, 2.0], [2, 0.0, 1.0, 2.0])
    ]
    assert set_time_and_check(3.0, transport, store) == [
        (["5/4", 120.0], [2, 0.0, 1.0, 2.0], [2, 0.0, 1.0, 2.0])
    ]
    assert set_time_and_check(3.5, transport, store) == [
        (["5/4", 120.0], [2, 0.0, 1.0, 2.0], [2, 0.0, 1.0, 2.0])
    ]
    assert set_time_and_check(4.0, transport, store) == [
        (["5/4", 120.0], [2, 0.0, 1.0, 2.0], [2, 0.0, 1.0, 2.0])
    ]
    assert set_time_and_check(4.5, transport, store) == [
        (["5/4", 120.0], [2, 0.0, 1.0, 2.0], [2, 0.0, 1.0, 2.0]),
        (["5/4", 120.0], [3, 0.0, 2.25, 4.5], [3, 0.0, 2.25, 4.5]),
    ]


def test_cue_invalid(transport):
    transport.start()
    with pytest.raises(ValueError):
        transport.cue(callback, quantization="BOGUS")


@pytest.mark.timeout(5)
def test_reschedule_earlier(transport):
    store = []
    transport.start()
    time.sleep(0.1)
    event_id = transport.cue(
        callback, quantization="1M", args=[store], kwargs={"limit": 0}
    )
    assert transport._peek() == 2.0
    assert set_time_and_check(0.0, transport, store) == []
    transport.reschedule(event_id, schedule_at=0.5)
    assert transport._peek() == 1.0
    assert set_time_and_check(2.0, transport, store) == [
        (["4/4", 120.0], [2, 0.0, 1.0, 2.0], [1, 0.5, 0.5, 1.0])
    ]


@pytest.mark.timeout(5)
def test_reschedule_later(transport):
    store = []
    transport.start()
    time.sleep(0.1)
    event_id = transport.cue(
        callback, quantization="1M", args=[store], kwargs={"limit": 0}
    )
    assert transport._peek() == 2.0
    assert set_time_and_check(0.0, transport, store) == []
    transport.reschedule(event_id, schedule_at=1.5)
    assert transport._peek() == 3.0
    assert set_time_and_check(3.0, transport, store) == [
        (["4/4", 120.0], [2, 0.5, 1.5, 3.0], [2, 0.5, 1.5, 3.0])
    ]


@pytest.mark.timeout(5)
def test_reschedule_later_but_earliest_wins(transport):
    store = []
    transport.start()
    time.sleep(0.1)
    event_id = transport.cue(
        callback, quantization="1M", args=[store], kwargs={"limit": 0}
    )
    assert transport._peek() == 2.0
    assert set_time_and_check(0.0, transport, store) == []
    transport.reschedule(event_id, schedule_at=1.5, earliest_wins=True)
    assert transport._peek() == 2.0
    assert set_time_and_check(3.0, transport, store) == [
        (["4/4", 120.0], [2, 0.5, 1.5, 3.0], [2, 0.0, 1.0, 2.0])
    ]


@pytest.mark.timeout(5)
def test_change_tempo_not_running(transport):
    assert transport.beats_per_minute == 120
    assert transport.time_signature == (4, 4)
    transport.change(beats_per_minute=135, time_signature=(3, 4))
    assert transport.beats_per_minute == 135
    assert transport.time_signature == (3, 4)


@pytest.mark.timeout(5)
def test_change_time_signature_on_downbeat(transport):
    store = []
    transport.change(beats_per_minute=240)
    transport.schedule(
        callback,
        schedule_at=0.0,
        args=[store],
        kwargs={"delta": 1, "unit": TimeUnit.MEASURES},
    )
    transport.start()
    assert set_time_and_check(0.0, transport, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0])
    ]
    transport.schedule_change(schedule_at=2, time_signature=(3, 4))
    assert set_time_and_check(1.0, transport, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [2, 0.0, 1.0, 1.0]),
    ]
    assert set_time_and_check(2.0, transport, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [2, 0.0, 1.0, 1.0]),
        (["3/4", 240], [3, 0.0, 2.0, 2.0], [3, 0.0, 2.0, 2.0]),
    ]
    assert set_time_and_check(3.0, transport, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [2, 0.0, 1.0, 1.0]),
        (["3/4", 240], [3, 0.0, 2.0, 2.0], [3, 0.0, 2.0, 2.0]),
        (["3/4", 240], [4, 0.25, 3.0, 3.0], [4, 0.0, 2.75, 2.75]),
    ]


@pytest.mark.timeout(5)
def test_change_time_signature_on_downbeat_laggy(transport):
    store = []
    transport.change(beats_per_minute=240)
    transport.schedule(
        callback,
        schedule_at=0.0,
        args=[store],
        kwargs={"delta": 1, "unit": TimeUnit.MEASURES},
    )
    transport.start()
    assert set_time_and_check(0.0, transport, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0])
    ]
    transport.schedule_change(schedule_at=2, time_signature=(3, 4))
    assert set_time_and_check(3.0, transport, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 240], [4, 0.0, 3.0, 3.0], [2, 0.0, 1.0, 1.0]),
        (["3/4", 240], [4, 0.25, 3.0, 3.0], [3, 0.0, 2.0, 2.0]),
        (["3/4", 240], [4, 0.25, 3.0, 3.0], [4, 0.0, 2.75, 2.75]),
    ]


@pytest.mark.timeout(5)
def test_change_time_signature_late(transport):
    store = []
    transport.change(beats_per_minute=240)
    transport.schedule(
        callback,
        schedule_at=0.0,
        args=[store],
        kwargs={"delta": 1, "unit": TimeUnit.MEASURES},
    )
    transport.start()
    assert set_time_and_check(0.0, transport, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0])
    ]
    transport.schedule_change(schedule_at=1.875, time_signature=(3, 4))
    assert set_time_and_check(1.0, transport, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [2, 0.0, 1.0, 1.0]),
    ]
    assert set_time_and_check(2.0, transport, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [2, 0.0, 1.0, 1.0]),
        (["3/4", 240], [3, 0.125, 2.0, 2.0], [3, 0.0, 1.875, 1.875]),
    ]
    assert set_time_and_check(3.0, transport, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [2, 0.0, 1.0, 1.0]),
        (["3/4", 240], [3, 0.125, 2.0, 2.0], [3, 0.0, 1.875, 1.875]),
        (["3/4", 240], [4, 0.375, 3.0, 3.0], [4, 0.0, 2.625, 2.625]),
    ]


@pytest.mark.timeout(5)
def test_change_time_signature_late_laggy(transport):
    store = []
    transport.change(beats_per_minute=240)
    transport.schedule(
        callback,
        schedule_at=0.0,
        args=[store],
        kwargs={"delta": 1, "unit": TimeUnit.MEASURES},
    )
    transport.start()
    assert set_time_and_check(0.0, transport, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0])
    ]
    transport.schedule_change(schedule_at=1.875, time_signature=(3, 4))
    assert set_time_and_check(3.0, transport, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 240], [4, 0.0, 3.0, 3.0], [2, 0.0, 1.0, 1.0]),
        (["3/4", 240], [4, 0.375, 3.0, 3.0], [3, 0.0, 1.875, 1.875]),
        (["3/4", 240], [4, 0.375, 3.0, 3.0], [4, 0.0, 2.625, 2.625]),
    ]


@pytest.mark.timeout(5)
def test_change_time_signature_early(transport):
    store = []
    transport.change(beats_per_minute=240)
    transport.schedule(
        callback,
        schedule_at=0.0,
        args=[store],
        kwargs={"delta": 1, "unit": TimeUnit.MEASURES},
    )
    transport.start()
    assert set_time_and_check(0.0, transport, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0])
    ]
    transport.schedule_change(schedule_at=1.125, time_signature=(5, 4))
    assert set_time_and_check(1.0, transport, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [2, 0.0, 1.0, 1.0]),
    ]
    assert transport.time_signature == (4, 4)
    assert set_time_and_check(2.0, transport, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [2, 0.0, 1.0, 1.0]),
    ]
    assert transport.time_signature == (5, 4)
    assert set_time_and_check(3.0, transport, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [2, 0.0, 1.0, 1.0]),
        (["5/4", 240], [3, 0.75, 3.0, 3.0], [3, 0.0, 2.25, 2.25]),
    ]


@pytest.mark.timeout(5)
def test_change_time_signature_early_laggy(transport):
    store = []
    transport.change(beats_per_minute=240)
    transport.schedule(
        callback,
        schedule_at=0.0,
        args=[store],
        kwargs={"delta": 1, "unit": TimeUnit.MEASURES},
    )
    transport.start()
    assert set_time_and_check(0.0, transport, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0])
    ]
    transport.schedule_change(schedule_at=1.125, time_signature=(5, 4))
    assert set_time_and_check(3.0, transport, store) == [
        (["4/4", 240], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 240], [4, 0.0, 3.0, 3.0], [2, 0.0, 1.0, 1.0]),
        (["5/4", 240], [3, 0.75, 3.0, 3.0], [3, 0.0, 2.25, 2.25]),  # time travel
    ]


@pytest.mark.timeout(5)
def test_change_time_signature_shrinking(transport):
    """
    When shifting to a smaller time signature, if the desired measure offset is
    within that smaller time signature, maintain the desired measure and
    measure offset.
    """
    store = []
    transport.change(beats_per_minute=240)
    transport.schedule(callback, schedule_at=0.0, args=[store], kwargs={"limit": 12})
    transport.schedule_change(schedule_at=1.125, time_signature=(2, 4))
    transport.start()
    assert set_time_and_check(1.0, transport, store) == [
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [1, 0.25, 0.25, 0.25]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [1, 0.5, 0.5, 0.5]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [1, 0.75, 0.75, 0.75]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [2, 0.0, 1.0, 1.0]),
    ]
    assert set_time_and_check(1.25, transport, store) == [
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [1, 0.25, 0.25, 0.25]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [1, 0.5, 0.5, 0.5]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [1, 0.75, 0.75, 0.75]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [2, 0.0, 1.0, 1.0]),
        (["2/4", 240], [2, 0.25, 1.25, 1.25], [2, 0.25, 1.25, 1.25]),
    ]
    assert set_time_and_check(1.5, transport, store) == [
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [1, 0.25, 0.25, 0.25]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [1, 0.5, 0.5, 0.5]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [1, 0.75, 0.75, 0.75]),
        (["4/4", 240], [2, 0.0, 1.0, 1.0], [2, 0.0, 1.0, 1.0]),
        (["2/4", 240], [2, 0.25, 1.25, 1.25], [2, 0.25, 1.25, 1.25]),
        (["2/4", 240], [3, 0.0, 1.5, 1.5], [3, 0.0, 1.5, 1.5]),
    ]


@pytest.mark.timeout(5)
def test_schedule_measure_relative(transport):
    store = []
    transport.change(beats_per_minute=240)
    transport.schedule(
        callback,
        schedule_at=3,
        unit=TimeUnit.MEASURES,
        args=[store],
        kwargs={"limit": 0},
    )
    transport.start()
    assert set_time_and_check(0.0, transport, store) == []
    assert set_time_and_check(4.0, transport, store) == [
        (["4/4", 240], [5, 0.0, 4.0, 4.0], [3, 0.0, 2.0, 2.0])
    ]


@pytest.mark.timeout(5)
def test_schedule_seconds_relative(transport):
    store = []
    transport.change(beats_per_minute=240)
    transport.schedule(
        callback,
        schedule_at=1.234,
        unit=TimeUnit.SECONDS,
        args=[store],
        kwargs={"limit": 0},
    )
    transport.start()
    assert set_time_and_check(0.0, transport, store) == []
    assert set_time_and_check(4.0, transport, store) == [
        (["4/4", 240], [5, 0.0, 4.0, 4.0], [2, 0.234, 1.234, 1.234])
    ]


@pytest.mark.timeout(5)
def test_cancel_invalid(transport):
    transport.start()
    with pytest.raises(KeyError):
        transport.cancel(1)


def test_slop(transport):
    assert transport.slop == 0.001
    transport.slop = 0.1
    assert transport.slop == 0.1
    with pytest.raises(ValueError):
        transport.slop = 0
    with pytest.raises(ValueError):
        transport.slop = -1.0


def test_start_and_restart(transport):
    assert not transport.is_running
    transport.start()
    assert transport.is_running
    with pytest.raises(RuntimeError):
        transport.start()
    assert transport.is_running


def test_stop_and_restop(transport):
    assert not transport.is_running
    transport.start()
    assert transport.is_running
    transport.stop()
    assert not transport.is_running
    transport.stop()
    assert not transport.is_running


def test_clock_skew():
    transport = Transport()
    transport.slop = 0.0001
    all_stats = []
    for _ in range(5):
        store = []
        for _ in range(20):
            delta = random.random() / 100
            transport.schedule(
                callback,
                schedule_at=random.random(),
                args=[store],
                kwargs={"limit": 100, "delta": delta, "unit": TimeUnit.SECONDS},
            )
        transport.start()
        time.sleep(5.0)
        transport.stop()
        stats = calculate_skew(store)
        print(" ".join(f"{key}: {value:f}" for key, value in stats.items()))
        all_stats.append(stats)
    assert all(stats["median"] < transport.slop for stats in all_stats)
