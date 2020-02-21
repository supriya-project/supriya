import asyncio
import logging
import queue
import traceback
from typing import Optional, Tuple

from .bases import (
    BaseTempoClock,
    CallbackCommand,
    ChangeCommand,
    ClockState,
    EventType,
    Moment,
)

logger = logging.getLogger("supriya.clock")


class AsyncTempoClock(BaseTempoClock):
    def __init__(self):
        BaseTempoClock.__init__(self)
        self._condition = None
        self._lock = None
        self._task = None

    ### SCHEDULING METHODS ###

    def _cancel(self, event_id) -> Optional[Tuple]:
        event = self._events_by_id.pop(event_id, None)
        if event is not None and not isinstance(
            event, (CallbackCommand, ChangeCommand)
        ):
            self._event_queue.remove(event)
            if event.offset is not None:
                self._offset_relative_event_ids.remove(event.event_id)
                if event.measure is not None:
                    self._measure_relative_event_ids.remove(event.event_id)
        return event

    async def _perform_callback_event(self, event, current_moment, desired_moment):
        logger.debug(
            f"[{self.name}] ... ... Performing {event.procedure} at "
            f"{desired_moment.seconds - self._state.initial_seconds}:s / "
            f"{desired_moment.offset}:o"
        )
        try:
            result = event.procedure(
                current_moment,
                desired_moment,
                event,
                *(event.args or ()),
                **(event.kwargs or {}),
            )
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
        logger.debug(f"[{self.name}] Thread start")
        async with self._lock:
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
                if not offline:
                    try:
                        await asyncio.wait_for(self._condition.wait(), self._slop)
                    except (asyncio.TimeoutError, RuntimeError):
                        pass
        logger.debug(f"[{self.name}] Terminating")

    async def _wait_for_moment(self, offline=False) -> Optional[Moment]:
        logger.debug(f"[{self.name}] ... Waiting for next moment")
        current_time = self.get_current_time()
        while current_time < self._event_queue.peek().seconds:
            if not offline:
                try:
                    await asyncio.wait_for(self._condition.wait(), self._slop)
                except (asyncio.TimeoutError, RuntimeError):
                    pass
            if not self._is_running:
                return None
            self._process_command_deque()
            current_time = self.get_current_time()
        return self._seconds_to_moment(current_time)

    async def _wait_for_queue(self, offline=False) -> bool:
        logger.debug(f"[{self.name}] ... Waiting for events")
        self._process_command_deque()
        while not self._event_queue.qsize():
            if not offline:
                try:
                    await asyncio.wait_for(self._condition.wait(), self._slop)
                except (asyncio.TimeoutError, RuntimeError):
                    pass
            if not self._is_running:
                return False
            self._process_command_deque()
        return True

    ### PUBLIC METHODS ###

    def change(
        self,
        beats_per_minute: Optional[float] = None,
        time_signature: Optional[Tuple[int, int]] = None,
    ) -> Optional[int]:
        if not self._is_running:
            self._state = self._state._replace(
                beats_per_minute=beats_per_minute or self._state.beats_per_minute,
                time_signature=time_signature or self._state.time_signature,
            )
            return None
        event_id = next(self._counter)
        command = ChangeCommand(
            event_id=event_id,
            event_type=EventType.CHANGE,
            beats_per_minute=beats_per_minute,
            time_signature=time_signature,
            quantization=None,
            schedule_at=self.get_current_time(),
            time_unit=None,
        )
        self._enqueue_command(command)
        return event_id

    async def start(
        self,
        initial_time: Optional[float] = None,
        initial_offset: float = 0.0,
        initial_measure: int = 1,
        beats_per_minute: Optional[float] = None,
        time_signature: Optional[Tuple[int, int]] = None,
    ):
        if self._is_running:
            raise RuntimeError("Already started")
        if initial_time is None:
            initial_time = self.get_current_time()
        self._state = ClockState(
            beats_per_minute=beats_per_minute or self._state.beats_per_minute,
            initial_seconds=initial_time,
            previous_measure=int(initial_measure),
            previous_offset=float(initial_offset),
            previous_seconds=float(initial_time),
            previous_time_signature_change_offset=float(initial_offset),
            time_signature=time_signature or self._state.time_signature,
        )
        self._is_running = True
        loop = asyncio.get_running_loop()
        self._lock = asyncio.Lock()
        self._condition = asyncio.Condition(self._lock)
        self._task = loop.create_task(self._run())

    async def stop(self):
        if not self._is_running:
            return
        self._is_running = False
        async with self._lock:
            self._condition.notify()
        await self._task
