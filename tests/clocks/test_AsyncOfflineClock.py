import asyncio
import logging

import pytest

from supriya.clocks import (
    AsyncOfflineClock,
    CallbackEvent,
    ClockContext,
    ClockDelta,
    TimeUnit,
)

repeat_count = 5

logger = logging.getLogger("supriya.test")


@pytest.fixture(autouse=True)
def log_everything(caplog) -> None:
    caplog.set_level(logging.INFO, logger="supriya.clocks")


async def callback(
    context: ClockContext,
    store: list[ClockContext],
    *,
    blow_up_at: int | None = None,
    delta: float = 0.25,
    limit: int | None = 4,
    time_unit: TimeUnit = TimeUnit.BEATS,
) -> ClockDelta:
    assert isinstance(context.event, CallbackEvent)
    if context.event.invocations == blow_up_at:
        raise Exception
    store.append(context)
    if limit is None:
        return delta, time_unit
    elif context.event.invocations < limit:
        return delta, time_unit
    return None


def check(
    store: list[ClockContext],
) -> list[tuple[list[float | str], list[float | int], list[float | int]]]:
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


@pytest.mark.asyncio
async def test_basic() -> None:
    clock = AsyncOfflineClock()
    store: list[ClockContext] = []
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
