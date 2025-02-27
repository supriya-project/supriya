import logging
import queue
from typing import Generator, Optional, Tuple

from .asynchronous import AsyncClock
from .core import BaseClock, CallbackEvent, ClockContext, Moment, TimeUnit

logger = logging.getLogger(__name__)


class OfflineClock(BaseClock):
    """
    An offline clock.
    """

    ### INITIALIZER ###

    def __init__(self) -> None:
        super().__init__()
        self._generator: Optional[Generator[bool, None, None]] = None

    ### SCHEDULING METHODS ###

    def _get_current_time(self) -> float:
        if not self._is_running:
            return 0.0
        return self._state.previous_seconds

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
        if isinstance(result, float) or result is None:
            delta, time_unit = result, TimeUnit.BEATS
        else:
            delta, time_unit = result
        self._process_callback_event_result(desired_moment, event, delta, time_unit)

    def _run(self, offline: bool = False) -> Generator[bool, None, None]:
        logger.debug(f"[{self.name}] Thread start")
        self._process_command_deque(first_run=True)
        while self._is_running and self._event_queue.qsize():
            logger.debug(f"[{self.name}] Loop start")
            if not self._wait_for_queue():
                return
            try:
                if (current_moment := self._wait_for_moment()) is None:
                    return
            except queue.Empty:
                continue
            current_moment = self._perform_events(current_moment)
            self._state = self._state._replace(
                previous_seconds=current_moment.seconds,
                previous_offset=current_moment.offset,
            )
        logger.debug(f"[{self.name}] Terminating")
        yield False
        self._stop()

    def _wait_for_moment(self, offline: bool = False) -> Optional[Moment]:
        current_time = self._event_queue.peek().seconds
        return self._seconds_to_moment(current_time)

    def _wait_for_queue(self, offline: bool = False) -> bool:
        logger.debug(f"[{self.name}] ... Waiting for events")
        self._process_command_deque()
        return True

    ### PUBLIC METHODS ###

    def start(
        self,
        initial_time: Optional[float] = None,
        initial_offset: float = 0.0,
        initial_measure: int = 1,
        beats_per_minute: Optional[float] = None,
        time_signature: Optional[Tuple[int, int]] = None,
    ) -> None:
        self._start(
            initial_time=initial_time,
            initial_offset=initial_offset,
            initial_measure=initial_measure,
            beats_per_minute=beats_per_minute,
            time_signature=time_signature,
        )
        self._generator = self._run()
        if not next(self._generator):
            self._stop()

    def stop(self) -> None:
        if not self._stop():
            return
        if self._generator is not None:
            while True:
                try:
                    next(self._generator)
                except StopIteration:
                    pass


class AsyncOfflineClock(AsyncClock):

    def _get_current_time(self) -> float:
        if not self._is_running:
            return 0.0
        return self._state.previous_seconds

    async def _run_async(self, offline: bool = False) -> None:
        logger.debug(f"[{self.name}] Coroutine start")
        self._process_command_deque(first_run=True)
        while self._is_running and self._event_queue.qsize():
            logger.debug(f"[{self.name}] Loop start")
            if not await self._wait_for_queue_async():
                return
            try:
                if (current_moment := await self._wait_for_moment_async()) is None:
                    return
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

    async def _wait_for_moment_async(self, offline: bool = False) -> Optional[Moment]:
        current_time = self._event_queue.peek().seconds
        self._process_command_deque()
        self._event.clear()
        return self._seconds_to_moment(current_time)

    async def _wait_for_queue_async(self, offline: bool = False) -> bool:
        logger.debug(f"[{self.name}] ... Waiting for events")
        self._process_command_deque()
        self._event.clear()
        return True
