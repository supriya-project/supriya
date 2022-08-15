from queue import Empty, PriorityQueue, Queue
from threading import RLock
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, cast
from uuid import UUID, uuid4

from ..clocks import CallbackEvent, Clock, ClockContext
from ..providers import Provider
from .eventpatterns import Pattern
from .events import Event, Priority, StartEvent, StopEvent


class PatternPlayer:
    def __init__(
        self,
        pattern: Pattern,
        provider: Provider,
        clock: Clock,
        callback: Optional[
            Callable[["PatternPlayer", ClockContext, Event], None]
        ] = None,
        uuid: Optional[UUID] = None,
    ):
        self._pattern = pattern
        self._provider = provider
        self._clock = clock
        self._callback = callback
        self._lock = RLock()
        self._queue: Queue[
            Tuple[float, int, Union[int, Tuple[int, int]], Optional[Event]]
        ] = PriorityQueue()
        self._is_running = False
        self._is_stopping = False
        self._proxies_by_uuid: Dict[UUID, Any] = {}
        self._notes_by_uuid: Dict[UUID, Any] = {}
        self._uuid = uuid or uuid4()

    def _clock_callback(self, context: ClockContext, *args, **kwargs):
        with self._lock:
            current_offset = None
            events: List[Tuple[Event, int]] = []
            if not cast(CallbackEvent, context.event).invocations and self._callback:
                self._callback(self, context, StartEvent())
            while True:
                try:
                    offset, priority, index, event = self._queue.get(block=False)
                except Empty:
                    self._perform_events(
                        context, context.desired_moment.seconds, current_offset, events
                    )
                    self._is_running = False
                    if self._callback:
                        self._callback(self, context, StopEvent())
                    return
                except Exception:
                    return
                if offset == float("-inf"):
                    offset = context.desired_moment.offset
                delta = offset - context.desired_moment.offset
                if delta:
                    self._queue.put((offset, priority, index, event))
                    self._perform_events(
                        context, context.desired_moment.seconds, current_offset, events
                    )
                    return delta
                if not isinstance(event, Event):
                    if self._consume_iterator(offset):
                        if self._callback:
                            self._callback(self, context, StopEvent())
                        return
                elif offset != current_offset:
                    self._perform_events(
                        context, context.desired_moment.seconds, current_offset, events
                    )
                    current_offset = offset
                    events = [(event, priority)]
                else:
                    events.append((event, priority))

    def _consume_iterator(self, current_offset):
        try:
            try:
                index, consumed_event = self._iterator.send(self._is_stopping)
            except TypeError:
                if self._is_stopping:
                    return True
                index, consumed_event = next(self._iterator)
            for subindex, (expanded_offset, priority, expanded_event) in enumerate(
                consumed_event.expand(current_offset)
            ):
                self._queue.put(
                    (expanded_offset, priority, (index, subindex), expanded_event)
                )
            self._queue.put(
                (current_offset + consumed_event.delta, 0, (index, 0), None)
            )
        except StopIteration:
            pass
        return False

    def _stop_callback(self, context, *args, **kwargs):
        with self._lock:
            # Do we need to rebuild the queue? Yes.
            # Do we need to free all playing notes? Yes.
            # How do we handle when there are already stop events in the queue? They'll be no-ops when performed.
            self._is_stopping = True
            self._clock.reschedule(
                self._clock_event_id, schedule_at=context.desired_moment.offset
            )
            self._reschedule_queue(context.desired_moment.offset)
            self._free_all_notes(context.desired_moment.seconds)

    def _enumerate(self, iterator):
        index = 0
        should_stop = False
        while True:
            try:
                should_stop = yield (index, iterator.send(should_stop)) or should_stop
            except TypeError:
                should_stop = yield (index, next(iterator))
            except StopIteration:
                return
            index += 1

    def _free_all_notes(self, current_seconds):
        if not self._notes_by_uuid:
            return
        with self._provider.at(current_seconds):
            while self._notes_by_uuid:
                uuid, _ = self._notes_by_uuid.popitem()
                proxy = self._proxies_by_uuid.pop(uuid)
                self._provider.free_node(proxy)

    def _perform_events(
        self, context: ClockContext, current_seconds, current_offset, events
    ):
        if not events:
            return
        with self._provider.at(current_seconds):
            for event, priority in events:
                event.perform(
                    self._provider,
                    self._proxies_by_uuid,
                    current_offset=current_offset,
                    notes_mapping=self._notes_by_uuid,
                    priority=priority,
                )
                if self._callback:
                    self._callback(self, context, event)

    def _reschedule_queue(self, current_offset):
        events = []
        while not self._queue.empty():
            events.append(self._queue.get())
        if not events:
            return
        delta = events[0][0] - current_offset
        for event in events:
            offset, *rest = event
            self._queue.put((offset - delta, *rest))

    def play(self, quantization: str = None, at=None, until=None):
        with self._lock:
            if self._is_running:
                return
            self._iterator = self._enumerate(iter(self._pattern))
            self._queue.put((float("-inf"), 0, (0, 0), None))
            self._is_running = True
            self._is_stopping = False
        self._clock_event_id = self._clock.cue(
            self._clock_callback, event_type=3, quantization=quantization
        )
        if until:
            self._clock.schedule(self._stop_callback, event_type=2, schedule_at=until)
        if not self._clock.is_running:
            self._clock.start(initial_time=at)

    def stop(self, quantization: str = None):
        with self._lock:
            if not self._is_running or self._is_stopping:
                return
            self._clock.cue(
                self._stop_callback, event_type=2, quantization=quantization
            )

    @property
    def uuid(self):
        return self._uuid
