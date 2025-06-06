import logging
import queue
from contextlib import asynccontextmanager, contextmanager
from typing import AsyncGenerator, Awaitable, Generator

from .asynchronous import AsyncClock
from .core import (
    BaseClock,
    CallbackEvent,
    ClockCallback,
    ClockContext,
    Moment,
    TimeUnit,
)

logger = logging.getLogger(__name__)


class OfflineClock(BaseClock[ClockCallback]):
    """
    An offline clock.
    """

    ### SCHEDULING METHODS ###

    def _get_current_time(self) -> float:
        return self._state.previous_seconds

    def _get_initial_time(self) -> float:
        return self._state.initial_seconds

    def _perform_callback_event(
        self, event: CallbackEvent, current_moment: Moment, desired_moment: Moment
    ) -> None:
        logger.debug(
            f"[{self.name}] ... ... Performing {event.procedure} at "
            f"{desired_moment.seconds - self._state.initial_seconds}:s / "
            f"{desired_moment.offset}:o"
        )
        context = ClockContext(current_moment, desired_moment, event)
        args = event.args or ()
        kwargs = event.kwargs or {}
        result = event.procedure(context, *args, **kwargs)
        assert not isinstance(result, Awaitable)
        if isinstance(result, float) or result is None:
            delta, time_unit = result, TimeUnit.BEATS
        else:
            delta, time_unit = result
        self._process_callback_event_result(desired_moment, event, delta, time_unit)

    def _run(self, offline: bool = False):
        logger.debug(f"[{self.name}] Thread start")
        self._process_command_deque(first_run=True)
        while self._is_running and self._event_queue.qsize():
            logger.debug(f"[{self.name}] Loop start")
            if not self._wait_for_queue():
                break
            try:
                if (current_moment := self._wait_for_moment()) is None:
                    break
            except queue.Empty:
                continue
            current_moment = self._perform_events(current_moment)
            self._state = self._state._replace(
                previous_seconds=current_moment.seconds,
                previous_offset=current_moment.offset,
            )
        logger.debug(f"[{self.name}] Terminating")
        self._stop()

    def _wait_for_moment(self, offline: bool = False) -> Moment | None:
        current_time = self._event_queue.peek().seconds
        return self._seconds_to_moment(current_time)

    def _wait_for_queue(self, offline: bool = False) -> bool:
        logger.debug(f"[{self.name}] ... Waiting for events")
        self._process_command_deque()
        return True

    ### PUBLIC METHODS ###

    @contextmanager
    def at(
        self,
        initial_time: float | None = None,
        initial_offset: float = 0.0,
        initial_measure: int = 1,
        beats_per_minute: float | None = None,
        time_signature: tuple[int, int] | None = None,
    ) -> Generator["OfflineClock", None, None]:
        yield self
        self.start(
            initial_time=initial_time,
            initial_offset=initial_offset,
            initial_measure=initial_measure,
            beats_per_minute=beats_per_minute,
            time_signature=time_signature,
        )

    def start(
        self,
        initial_time: float | None = None,
        initial_offset: float = 0.0,
        initial_measure: int = 1,
        beats_per_minute: float | None = None,
        time_signature: tuple[int, int] | None = None,
    ) -> None:
        self._start(
            initial_time=initial_time,
            initial_offset=initial_offset,
            initial_measure=initial_measure,
            beats_per_minute=beats_per_minute,
            time_signature=time_signature,
        )
        self._run()

    def stop(self) -> None:
        return


class AsyncOfflineClock(AsyncClock):
    ### SCHEDULING METHODS ###

    def _get_current_time(self) -> float:
        return self._state.previous_seconds

    def _get_initial_time(self) -> float:
        return self._state.initial_seconds

    async def _run_async(self, offline: bool = False) -> None:
        logger.debug(f"[{self.name}] Coroutine start")
        self._process_command_deque(first_run=True)
        while self._is_running and self._event_queue.qsize():
            logger.debug(f"[{self.name}] Loop start")
            if not await self._wait_for_queue_async():
                break
            try:
                if (current_moment := await self._wait_for_moment_async()) is None:
                    break
            except queue.Empty:
                continue
            current_moment = await self._perform_events_async(current_moment)
            self._state = self._state._replace(
                previous_seconds=current_moment.seconds,
                previous_offset=current_moment.offset,
            )
        logger.debug(f"[{self.name}] Coroutine terminating")
        self._stop()

    async def _wait_for_event_async(self, sleep_time: float) -> None:
        pass

    async def _wait_for_moment_async(self, offline: bool = False) -> Moment | None:
        current_time = self._event_queue.peek().seconds
        self._process_command_deque()
        self._event.clear()
        return self._seconds_to_moment(current_time)

    async def _wait_for_queue_async(self, offline: bool = False) -> bool:
        logger.debug(f"[{self.name}] ... Waiting for events")
        self._process_command_deque()
        self._event.clear()
        return True

    ### PUBLIC METHODS ###

    @asynccontextmanager
    async def at(
        self,
        initial_time: float | None = None,
        initial_offset: float = 0.0,
        initial_measure: int = 1,
        beats_per_minute: float | None = None,
        time_signature: tuple[int, int] | None = None,
    ) -> AsyncGenerator["AsyncOfflineClock", None]:
        yield self
        await self.start(
            initial_time=initial_time,
            initial_offset=initial_offset,
            initial_measure=initial_measure,
            beats_per_minute=beats_per_minute,
            time_signature=time_signature,
        )

    async def start(
        self,
        initial_time: float | None = None,
        initial_offset: float = 0.0,
        initial_measure: int = 1,
        beats_per_minute: float | None = None,
        time_signature: tuple[int, int] | None = None,
    ) -> None:
        self._start(
            initial_time=initial_time,
            initial_offset=initial_offset,
            initial_measure=initial_measure,
            beats_per_minute=beats_per_minute,
            time_signature=time_signature,
        )
        await self._run_async()

    async def stop(self) -> None:
        return
