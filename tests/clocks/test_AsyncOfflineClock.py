import asyncio
import logging

import pytest

from supriya.clocks import AsyncOfflineClock, TimeUnit

repeat_count = 5

logger = logging.getLogger("supriya.test")


@pytest.fixture(autouse=True)
def log_everything(caplog):
    caplog.set_level(logging.INFO, logger="supriya.clocks")


async def callback(
    context,
    store,
    blow_up_at=None,
    delta=0.25,
    limit=4,
    time_unit=TimeUnit.BEATS,
    **kwargs,
):
    if context.event.invocations == blow_up_at:
        raise Exception
    store.append((context.current_moment, context.desired_moment, context.event))
    if limit is None:
        return delta, time_unit
    elif context.event.invocations < limit:
        return delta, time_unit
    return None


def check(store):
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
            current_moment.seconds,
        ]
        three = [
            desired_moment.measure,
            round(desired_moment.measure_offset, 10),
            desired_moment.offset,
            desired_moment.seconds,
        ]
        moments.append((one, two, three))
    return moments


@pytest.mark.asyncio
async def test_basic():
    clock = AsyncOfflineClock()
    store = []
    clock.schedule(callback, schedule_at=0.0, args=[store])
    await clock.start()
    await asyncio.sleep(0.1)
    assert check(store) == [
        (["4/4", 120.0], [1, 0.0, 0.0, 0.0], [1, 0.0, 0.0, 0.0]),
        (["4/4", 120.0], [1, 0.25, 0.25, 0.5], [1, 0.25, 0.25, 0.5]),
        (["4/4", 120.0], [1, 0.5, 0.5, 1.0], [1, 0.5, 0.5, 1.0]),
        (["4/4", 120.0], [1, 0.75, 0.75, 1.5], [1, 0.75, 0.75, 1.5]),
        (["4/4", 120.0], [2, 0.0, 1.0, 2.0], [2, 0.0, 1.0, 2.0]),
    ]
    await clock.stop()
