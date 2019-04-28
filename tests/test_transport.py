import time

import pytest

from supriya.transport import Transport


def callback(moment, event, store, delta=0.25, limit=4, blow_up_at=None, **kwargs):
    if event.invocations == blow_up_at:
        raise Exception
    store.append((moment, event))
    if event.invocations < limit:
        return delta
    return None


def set_time_and_check(time_to_advance, mock_time, store):
    mock_time.return_value = time_to_advance
    time.sleep(0.1)
    return condense_moments(store)


def condense_moments(store):
    return [
        (
            ["{}/{}".format(*moment.time_signature), moment.beats_per_minute],
            [
                moment.current_measure,
                round(moment.current_measure_offset, 10),
                moment.current_offset,
                moment.current_time,
            ],
            [moment.desired_offset, moment.desired_time],
        )
        for moment, event in store
    ]


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
    assert [moment.desired_offset for moment, event in store] == [
        0.0,
        0.25,
        0.5,
        0.75,
        1.0,
    ]


@pytest.mark.timeout(5)
def test_nonrealtime_basic(mocker):
    store = []
    mock = mocker.patch.object(Transport, "_get_current_time")
    mock.return_value = 0.0
    transport = Transport()
    transport.slop = 0.05
    transport.start()
    transport.schedule(callback, schedule_at=0.0, args=[store])
    time.sleep(0.1)
    assert condense_moments(store) == [(["4/4", 120.0], [1, 0.0, 0.0, 0.0], [0.0, 0.0])]
    assert set_time_and_check(0.5, mock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [0.25, 0.5]),
    ]
    assert set_time_and_check(1.0, mock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [0.25, 0.5]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [0.5, 1.0]),
    ]
    assert set_time_and_check(1.5, mock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [0.25, 0.5]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [0.5, 1.0]),
        (["4/4", 120.0], [1, 0.75, 0.75, 1.5], [0.75, 1.5]),
    ]
    assert set_time_and_check(2.0, mock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [0.25, 0.5]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [0.5, 1.0]),
        (["4/4", 120.0], [1, 0.75, 0.75, 1.5], [0.75, 1.5]),
        (["4/4", 120.0], [2, 0.0, 1.0, 2.0], [1.0, 2.0]),
    ]
    transport.stop()


@pytest.mark.timeout(5)
def test_nonrealtime_two_procedures(mocker):
    store_one = []
    store_two = []
    mock = mocker.patch.object(Transport, "_get_current_time")
    mock.return_value = 0.0
    transport = Transport()
    transport.slop = 0.05
    transport.start()
    transport.schedule(callback, schedule_at=0.0, args=[store_one])
    transport.schedule(
        callback, schedule_at=0.1, args=[store_two], kwargs={"delta": 0.3}
    )
    time.sleep(0.1)
    assert condense_moments(store_one) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [0.0, 0.0])
    ]
    assert condense_moments(store_two) == []
    mock.return_value = 0.5
    time.sleep(0.1)
    assert condense_moments(store_one) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [0.25, 0.5]),
    ]
    assert condense_moments(store_two) == [
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [0.1, 0.2])
    ]
    mock.return_value = 1.0
    time.sleep(0.1)
    assert condense_moments(store_one) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [0.25, 0.5]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [0.5, 1.0]),
    ]
    assert condense_moments(store_two) == [
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [0.1, 0.2]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [0.4, 0.8]),
    ]
    mock.return_value = 1.5
    time.sleep(0.1)
    assert condense_moments(store_one) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [0.25, 0.5]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [0.5, 1.0]),
        (["4/4", 120.0], [1, 0.75, 0.75, 1.5], [0.75, 1.5]),
    ]
    assert condense_moments(store_two) == [
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [0.1, 0.2]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [0.4, 0.8]),
        (["4/4", 120.0], [1, 0.75, 0.75, 1.5], [0.7, 1.4]),
    ]
    mock.return_value = 2.0
    time.sleep(0.1)
    assert condense_moments(store_one) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [0.25, 0.5]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [0.5, 1.0]),
        (["4/4", 120.0], [1, 0.75, 0.75, 1.5], [0.75, 1.5]),
        (["4/4", 120.0], [2, 0.0, 1.0, 2.0], [1.0, 2.0]),
    ]
    assert condense_moments(store_two) == [
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [0.1, 0.2]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [0.4, 0.8]),
        (["4/4", 120.0], [1, 0.75, 0.75, 1.5], [0.7, 1.4]),
        (["4/4", 120.0], [2, 0.0, 1.0, 2.0], [1.0, 2.0]),
    ]
    transport.stop()


@pytest.mark.timeout(5)
def test_nonrealtime_exception(mocker):
    store = []
    mock = mocker.patch.object(Transport, "_get_current_time")
    mock.return_value = 0.0
    transport = Transport()
    transport.slop = 0.05
    transport.start()
    transport.schedule(
        callback, schedule_at=0.0, args=[store], kwargs={"blow_up_at": 2}
    )
    time.sleep(0.1)
    assert condense_moments(store) == [(["4/4", 120.0], [1, 0.0, 0.0, 0.0], [0.0, 0.0])]
    assert set_time_and_check(0.5, mock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [0.25, 0.5]),
    ]
    assert set_time_and_check(1.0, mock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [0.25, 0.5]),
    ]
    assert set_time_and_check(1.5, mock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [0.25, 0.5]),
    ]
    assert set_time_and_check(2.0, mock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [0.25, 0.5]),
    ]
    transport.stop()


@pytest.mark.timeout(5)
def test_nonrealtime_change_tempo(mocker):
    store = []
    mock = mocker.patch.object(Transport, "_get_current_time")
    mock.return_value = 0.0
    transport = Transport()
    transport.slop = 0.05
    transport.start()
    transport.schedule(callback, schedule_at=0.0, args=[store])
    time.sleep(0.1)
    assert condense_moments(store) == [(["4/4", 120.0], [1, 0.0, 0.0, 0.0], [0.0, 0.0])]
    assert set_time_and_check(0.5, mock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [0.25, 0.5]),
    ]
    transport.beats_per_minute = 60
    assert set_time_and_check(1.0, mock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [0.25, 0.5]),
    ]
    assert set_time_and_check(1.5, mock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [0.25, 0.5]),
        (["4/4", 60.0], [1, 0.5, 0.5, 1.5], [0.5, 1.5]),
    ]
    assert set_time_and_check(2.0, mock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [0.25, 0.5]),
        (["4/4", 60.0], [1, 0.5, 0.5, 1.5], [0.5, 1.5]),
    ]
    transport.stop()


@pytest.mark.timeout(5)
def test_nonrealtime_schedule_tempo_change(mocker):
    store = []
    mock = mocker.patch.object(Transport, "_get_current_time")
    mock.return_value = 0.0
    transport = Transport()
    transport.slop = 0.05
    transport.start()
    transport.schedule(callback, schedule_at=0.0, args=[store])
    transport.schedule_change(schedule_at=0.5, beats_per_minute=60)
    time.sleep(0.1)
    assert condense_moments(store) == [(["4/4", 120.0], [1, 0.0, 0.0, 0.0], [0.0, 0.0])]
    assert set_time_and_check(0.5, mock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [0.25, 0.5]),
    ]
    assert set_time_and_check(1.0, mock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [0.25, 0.5]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [0.5, 1.0]),
    ]
    assert set_time_and_check(1.5, mock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [0.25, 0.5]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [0.5, 1.0]),
    ]
    assert set_time_and_check(2.0, mock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [0.25, 0.5]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [0.5, 1.0]),
        (["4/4", 60.0], [1, 0.75, 0.75, 2.0], [0.75, 2.0]),
    ]
    assert set_time_and_check(2.5, mock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [0.25, 0.5]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [0.5, 1.0]),
        (["4/4", 60.0], [1, 0.75, 0.75, 2.0], [0.75, 2.0]),
    ]
    transport.stop()


@pytest.mark.timeout(5)
def test_nonrealtime_cue_basic(mocker):
    store = []
    mock = mocker.patch.object(Transport, "_get_current_time")
    mock.return_value = 0.0
    transport = Transport()
    transport.slop = 0.05
    transport.start()
    transport.cue(callback, quantization=None, args=[store], kwargs={"limit": 0})
    time.sleep(0.1)
    assert condense_moments(store) == [(["4/4", 120.0], [1, 0.0, 0.0, 0.0], [0.0, 0.0])]
    mock.return_value = 0.25
    transport.cue(callback, quantization="1/4", args=[store], kwargs={"limit": 0})
    transport.cue(callback, quantization="1M", args=[store], kwargs={"limit": 0})
    time.sleep(0.1)
    assert condense_moments(store) == [(["4/4", 120.0], [1, 0.0, 0.0, 0.0], [0.0, 0.0])]
    assert set_time_and_check(0.5, mock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [0.25, 0.5]),
    ]
    assert set_time_and_check(1.0, mock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [0.25, 0.5]),
    ]
    assert set_time_and_check(1.5, mock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [0.25, 0.5]),
    ]
    assert set_time_and_check(2.0, mock, store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [0.25, 0.5]),
        (["4/4", 120.0], [2, 0.0, 1.0, 2.0], [1.0, 2.0]),
    ]
    transport.stop()


@pytest.mark.timeout(5)
def test_nonrealtime_cue_reschedule(mocker):
    store = []
    mock = mocker.patch.object(Transport, "_get_current_time")
    mock.return_value = 0.0
    transport = Transport()
    transport.slop = 0.05
    transport.start()
    time.sleep(0.1)
    assert condense_moments(store) == []
    mock.return_value = 0.5
    transport.cue(callback, quantization="1M", args=[store], kwargs={"limit": 0})
    transport.cue(callback, quantization="2M", args=[store], kwargs={"limit": 0})
    transport.schedule_change(schedule_at=1.0, time_signature=(5, 4))
    time.sleep(0.1)
    assert condense_moments(store) == []
    assert set_time_and_check(1.0, mock, store) == []
    assert set_time_and_check(1.5, mock, store) == []
    assert set_time_and_check(2.0, mock, store) == [
        (["5/4", 120.0], [2, 0.0, 1.0, 2.0], [1.0, 2.0])
    ]
    assert set_time_and_check(2.5, mock, store) == [
        (["5/4", 120.0], [2, 0.0, 1.0, 2.0], [1.0, 2.0])
    ]
    assert set_time_and_check(3.0, mock, store) == [
        (["5/4", 120.0], [2, 0.0, 1.0, 2.0], [1.0, 2.0])
    ]
    assert set_time_and_check(3.5, mock, store) == [
        (["5/4", 120.0], [2, 0.0, 1.0, 2.0], [1.0, 2.0])
    ]
    assert set_time_and_check(4.0, mock, store) == [
        (["5/4", 120.0], [2, 0.0, 1.0, 2.0], [1.0, 2.0])
    ]
    assert set_time_and_check(4.5, mock, store) == [
        (["5/4", 120.0], [2, 0.0, 1.0, 2.0], [1.0, 2.0]),
        (["5/4", 120.0], [3, 0.0, 2.25, 4.5], [2.25, 4.5]),
    ]
    transport.stop()
