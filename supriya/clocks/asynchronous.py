import asyncio
import logging
import queue
import traceback
from typing import Optional, Tuple

from .bases import BaseClock
from .ephemera import CallbackEvent, ClockContext, EventType, Moment

logger = logging.getLogger("supriya.clocks")


class AsyncClock(BaseClock):
    def __init__(self) -> None:
        BaseClock.__init__(self)
        self._task: Optional[asyncio.Task] = None
        self._slop = 1.0
        try:
            self._event = asyncio.Event()
        except RuntimeError:
            pass

    ### SCHEDULING METHODS ###

    def _enqueue_command(self, command) -> None:
        super()._enqueue_command(command)
        self._event.set()

    async def _perform_callback_event_async(
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
        try:
            result = event.procedure(context, *args, **kwargs)
            if asyncio.iscoroutine(result):
                result = await result
        except Exception:
            traceback.print_exc()
            return
        self._process_callback_event_result(desired_moment, event, result)

    async def _perform_events_async(self, current_moment: Moment) -> Moment:
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
                await self._perform_callback_event_async(
                    event, current_moment, desired_moment
                )
                self._process_command_deque()
        return current_moment

    async def _run_async(self, *args, offline=False, **kwargs) -> None:
        logger.debug(f"[{self.name}] Coroutine start")
        self._process_command_deque(first_run=True)
        while self._is_running:
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
        try:
            await asyncio.wait_for(self._event.wait(), sleep_time)
        except (asyncio.TimeoutError, RuntimeError):
            pass

    async def _wait_for_moment_async(self, offline=False) -> Optional[Moment]:
        current_time = self.get_current_time()
        next_time = self._event_queue.peek().seconds
        logger.debug(
            f"[{self.name}] ... Waiting for next moment at {next_time} from {current_time}"
        )
        while current_time < next_time:
            if not offline:
                await self._wait_for_event_async(next_time - current_time)
            if not self._is_running:
                return None
            self._process_command_deque()
            next_time = self._event_queue.peek().seconds
            current_time = self.get_current_time()
            self._event.clear()
        return self._seconds_to_moment(current_time)

    async def _wait_for_queue_async(self, offline=False) -> bool:
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
    ) -> None:
        self._start(
            initial_time=initial_time,
            initial_offset=initial_offset,
            initial_measure=initial_measure,
            beats_per_minute=beats_per_minute,
            time_signature=time_signature,
        )
        loop = asyncio.get_running_loop()
        self._event = asyncio.Event()
        self._task = loop.create_task(self._run_async())

    async def stop(self) -> None:
        if self._stop():
            self._event.set()
            if self._task is not None:
                await self._task
