import asyncio
import logging

import pytest

from supriya.clocks import (
    AsyncOfflineClock,
    CallbackEvent,
    ClockCallbackState,
    ClockDelta,
    TimeUnit,
)

repeat_count = 5

logger = logging.getLogger("supriya.test")


@pytest.fixture(autouse=True)
def log_everything(caplog) -> None:
    caplog.set_level(logging.INFO, logger="supriya.clocks")


async def callback(
    state: ClockCallbackState,
    store: list[ClockCallbackState],
    *,
    blow_up_at: int | None = None,
    delta: float = 0.25,
    limit: int | None = 4,
    time_unit: TimeUnit = TimeUnit.BEATS,
) -> ClockDelta:
    assert isinstance(state.event, CallbackEvent)
    if state.event.invocations == blow_up_at:
        raise Exception
    store.append(state)
    if limit is None:
        return delta, time_unit
    elif state.event.invocations < limit:
        return delta, time_unit
    return None


def check(
    store: list[ClockCallbackState],
) -> list[tuple[list[float | str], list[float | int], list[float | int]]]:
    return [
        (
            [
                "{}/{}".format(*state.current_moment.time_signature),
                state.current_moment.beats_per_minute,
            ],
            [
                state.current_moment.measure,
                round(state.current_moment.measure_offset, 10),
                state.current_moment.offset,
                state.current_moment.seconds,
            ],
            [
                state.desired_moment.measure,
                round(state.desired_moment.measure_offset, 10),
                state.desired_moment.offset,
                state.desired_moment.seconds,
            ],
        )
        for state in store
    ]


@pytest.mark.asyncio
async def test_basic() -> None:
    clock = AsyncOfflineClock()
    store: list[ClockCallbackState] = []
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
