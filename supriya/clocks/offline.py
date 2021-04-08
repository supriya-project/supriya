import logging
import queue
from typing import Optional, Tuple

from .asynchronous import AsyncClock
from .bases import BaseClock
from .ephemera import ClockContext, Moment

logger = logging.getLogger("supriya.clocks")


class OfflineClock(BaseClock):
    def __init__(self):
        super().__init__()
        self._generator = None

    ### SCHEDULING METHODS ###

    def _perform_callback_event(self, event, current_moment, desired_moment):
        logger.debug(
            f"[{self.name}] ... ... Performing {event.procedure} at "
            f"{desired_moment.seconds - self._state.initial_seconds}:s / "
            f"{desired_moment.offset}:o"
        )
        context = ClockContext(current_moment, desired_moment, event)
        args = event.args or ()
        kwargs = event.kwargs or {}
        result = event.procedure(context, *args, **kwargs)
        self._process_callback_event_result(desired_moment, event, result)

    def _run(self, *args, offline=False, **kwargs):
        logger.debug(f"[{self.name}] Thread start")
        self._process_command_deque(first_run=True)
        while self._is_running and self._event_queue.qsize():
            logger.debug(f"[{self.name}] Loop start")
            if not self._wait_for_queue():
                return
            try:
                current_moment = self._wait_for_moment()
            except queue.Empty:
                continue
            if current_moment is None:
                return
            current_moment = self._perform_events(current_moment)
            self._state = self._state._replace(
                previous_seconds=current_moment.seconds,
                previous_offset=current_moment.offset,
            )
        logger.debug(f"[{self.name}] Terminating")
        yield False
        self._stop()

    def _wait_for_moment(self, offline=False) -> Optional[Moment]:
        current_time = self._event_queue.peek().seconds
        return self._seconds_to_moment(current_time)

    def _wait_for_queue(self, offline=False) -> bool:
        logger.debug(f"[{self.name}] ... Waiting for events")
        self._process_command_deque()
        return True

    ### PUBLIC METHODS ###

    def get_current_time(self) -> float:
        if not self._is_running:
            return 0.0
        return self._state.previous_seconds

    def start(
        self,
        initial_time: Optional[float] = None,
        initial_offset: float = 0.0,
        initial_measure: int = 1,
        beats_per_minute: Optional[float] = None,
        time_signature: Optional[Tuple[int, int]] = None,
    ):
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

    def stop(self):
        if not self._stop():
            return
        if self._generator is not None:
            while True:
                try:
                    next(self._generator)
                except StopIteration:
                    pass


class AsyncOfflineClock(AsyncClock):
    async def _run(self, *args, offline=False, **kwargs):
        logger.debug(f"[{self.name}] Coroutine start")
        self._process_command_deque(first_run=True)
        while self._is_running and self._event_queue.qsize():
            logger.debug(f"[{self.name}] Loop start")
            if not await self._wait_for_queue():
                return
            try:
                current_moment = await self._wait_for_moment()
            except queue.Empty:
                continue
            if current_moment is None:
                return
            current_moment = await self._perform_events(current_moment)
            self._state = self._state._replace(
                previous_seconds=current_moment.seconds,
                previous_offset=current_moment.offset,
            )
        logger.debug(f"[{self.name}] Coroutine terminating")
        self._stop()

    async def _wait_for_event(self, sleep_time):
        pass

    async def _wait_for_moment(self, offline=False) -> Optional[Moment]:
        current_time = self._event_queue.peek().seconds
        self._process_command_deque()
        self._event.clear()
        return self._seconds_to_moment(current_time)

    async def _wait_for_queue(self, offline=False) -> bool:
        logger.debug(f"[{self.name}] ... Waiting for events")
        self._process_command_deque()
        self._event.clear()
        return True

    def get_current_time(self) -> float:
        if not self._is_running:
            return 0.0
        return self._state.previous_seconds
