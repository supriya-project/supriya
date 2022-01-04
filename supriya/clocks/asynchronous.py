import asyncio
import logging
import queue
import traceback
from typing import Optional, Tuple

from .bases import BaseClock
from .ephemera import ClockContext, EventType, Moment

logger = logging.getLogger("supriya.clocks")


class AsyncClock(BaseClock):
    def __init__(self):
        BaseClock.__init__(self)
        self._event = asyncio.Event()
        self._task = None
        self._slop = 1.0

    ### SCHEDULING METHODS ###

    def _enqueue_command(self, command):
        super()._enqueue_command(command)
        self._event.set()

    async def _perform_callback_event(self, event, current_moment, desired_moment):
        logger.debug(
            f"[{self.name}] ... ... Performing {event.procedure} at "
            f"{desired_moment.seconds - self._state.initial_seconds}:s / "
            f"{desired_moment.offset}:o"
        )
        context = ClockContext(current_moment, desired_moment, event)
        args = event.args or ()
        kwargs = event.kwargs or {}
        try:
            result = event.procedure(context, *args, **kwargs)
            if asyncio.iscoroutine(result):
                result = await result
        except Exception:
            traceback.print_exc()
            return
        self._process_callback_event_result(desired_moment, event, result)

    async def _perform_events(self, current_moment: Moment):
        logger.debug(
            f"[{self.name}] ... Ready to perform at "
            f"{current_moment.seconds - self._state.initial_seconds}:s / "
            f"{current_moment.offset}:o"
        )
        while self._is_running and self._event_queue.qsize():
            (
                event,
                desired_moment,
                should_continue,
                should_break,
            ) = self._process_perform_event_loop(current_moment)
            if should_continue:
                continue
            elif should_break:
                break
            if event.event_type == EventType.CHANGE:
                current_moment, should_continue = self._perform_change_event(
                    event, current_moment, desired_moment
                )
                if not should_continue:
                    break
            else:
                await self._perform_callback_event(
                    event, current_moment, desired_moment
                )
                self._process_command_deque()
        return current_moment

    async def _run(self, *args, offline=False, **kwargs):
        logger.debug(f"[{self.name}] Coroutine start")
        self._process_command_deque(first_run=True)
        while self._is_running:
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
        try:
            await asyncio.wait_for(self._event.wait(), sleep_time)
        except (asyncio.TimeoutError, RuntimeError):
            pass

    async def _wait_for_moment(self, offline=False) -> Optional[Moment]:
        current_time = self.get_current_time()
        next_time = self._event_queue.peek().seconds
        logger.debug(
            f"[{self.name}] ... Waiting for next moment at {next_time} from {current_time}"
        )
        while current_time < next_time:
            if not offline:
                await self._wait_for_event(next_time - current_time)
            if not self._is_running:
                return None
            self._process_command_deque()
            next_time = self._event_queue.peek().seconds
            current_time = self.get_current_time()
            self._event.clear()
        return self._seconds_to_moment(current_time)

    async def _wait_for_queue(self, offline=False) -> bool:
        logger.debug(f"[{self.name}] ... Waiting for events")
        self._process_command_deque()
        self._event.clear()
        while not self._event_queue.qsize():
            if not offline:
                await self._event.wait()
            if not self._is_running:
                return False
            self._process_command_deque()
            self._event.clear()
        return True

    ### PUBLIC METHODS ###

    def cancel(self, event_id) -> Optional[Tuple]:
        event = super().cancel(event_id)
        self._event.set()
        return event

    async def start(
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
        loop = asyncio.get_running_loop()
        self._task = loop.create_task(self._run())

    async def stop(self):
        if self._stop():
            self._event.set()
            await self._task
