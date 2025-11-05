from queue import Empty, PriorityQueue, Queue
from threading import RLock
from typing import (
    Callable,
    Generator,
    Iterable,
    Sequence,
    cast,
)
from uuid import UUID, uuid4
from weakref import WeakSet

from ..clocks import (
    BaseClock,
    CallbackEvent,
    ClockCallbackState,
    ClockDelta,
    Quantization,
)
from ..contexts import Bus, Context, ContextObject, Node
from .events import Event, Priority, StartEvent, StopEvent
from .patterns import Pattern
from .structure import PinPattern


class PatternPlayer:
    """
    A pattern player.

    Coordinates interactions between a pattern, a clock_context, and a clock.
    """

    # TODO: Rewrite type annotation after dropping 3.8
    _players = cast(set["PatternPlayer"], WeakSet())

    def __init__(
        self,
        pattern: Pattern,
        context: Context,
        clock: BaseClock,
        callback: (
            Callable[["PatternPlayer", ClockCallbackState, Event, Priority], None]
            | None
        ) = None,
        target_bus: Bus | None = None,
        target_node: Node | None = None,
        uuid: UUID | None = None,
    ) -> None:
        self._context = context
        self._clock = clock
        self._callback = callback
        self._lock = RLock()
        self._queue: Queue[
            tuple[float, Priority, int | tuple[int, int], Event | None]
        ] = PriorityQueue()
        self._is_running = False
        self._is_stopping = False
        self._proxies_by_uuid: dict[UUID | tuple[UUID, int], ContextObject] = {}
        self._notes_by_uuid: dict[UUID | tuple[UUID, int], float] = {}
        self._uuid: UUID = uuid or uuid4()
        self._target_bus = target_bus
        self._target_node = target_node
        self._next_delta: float | None = None
        self._initial_seconds: float | None = None
        self._clock_event_id = -1
        self._clock_stop_event_id = -1
        self._pattern = (
            pattern
            if (target_bus is None and target_node is None)
            else PinPattern(pattern, target_bus=target_bus, target_node=target_node)
        )
        self._yielded = False

    def _clock_callback(
        self, context: ClockCallbackState, *args, **kwargs
    ) -> ClockDelta:
        for clock_context, seconds, offset, events in self._find_events(context):
            if self._initial_seconds is None:
                self._initial_seconds = seconds
            with self._context.at(seconds):
                for event, priority in events:
                    event.perform(
                        self._context,
                        self._proxies_by_uuid,
                        current_offset=offset,
                        notes_mapping=self._notes_by_uuid,
                        priority=priority,
                    )
                    if self._callback is not None:
                        self._callback(self, clock_context, event, priority)
        return self._next_delta

    def _find_events(
        self, clock_context: ClockCallbackState
    ) -> Iterable[
        tuple[ClockCallbackState, float, float, Sequence[tuple[Event, Priority]]]
    ]:
        with self._lock:
            current_offset = float("-inf")
            events: list[tuple[Event, Priority]] = []
            if (
                not cast(CallbackEvent, clock_context.event).invocations
                and self._callback
            ):
                yield (
                    clock_context,
                    clock_context.desired_moment.seconds,
                    clock_context.desired_moment.offset,
                    [(StartEvent(), Priority.START)],
                )
            while True:
                try:
                    offset, priority, index, event = self._queue.get(block=False)
                except Empty:
                    if events:
                        yield (
                            clock_context,
                            clock_context.desired_moment.seconds,
                            current_offset,
                            events,
                        )
                    self._is_running = False
                    if self._callback:
                        yield (
                            clock_context,
                            clock_context.desired_moment.seconds,
                            current_offset,
                            [(StopEvent(), Priority.STOP)],
                        )
                    self._next_delta = None
                    return
                except Exception:
                    self._next_delta = None
                    return
                if offset == float("-inf"):
                    offset = clock_context.desired_moment.offset
                delta = offset - clock_context.desired_moment.offset
                if delta:
                    self._queue.put((offset, priority, index, event))
                    if events:
                        yield (
                            clock_context,
                            clock_context.desired_moment.seconds,
                            current_offset,
                            events,
                        )
                    self._next_delta = delta
                    return
                if not isinstance(event, Event):
                    if self._consume_iterator(offset):
                        if self._callback:
                            yield (
                                clock_context,
                                clock_context.desired_moment.seconds,
                                current_offset,
                                [(StopEvent(), Priority.STOP)],
                            )
                        self._next_delta = None
                        return
                elif offset != current_offset:
                    if events:
                        yield (
                            clock_context,
                            clock_context.desired_moment.seconds,
                            current_offset,
                            events,
                        )
                    current_offset = offset
                    events = [(event, priority)]
                else:
                    events.append((event, priority))

    def _consume_iterator(self, current_offset: float) -> bool:
        try:
            if self._yielded:
                index, consumed_event = self._iterator.send(self._is_stopping)
            else:
                if self._is_stopping:
                    return True
                index, consumed_event = next(self._iterator)
                self._yielded = True
            for subindex, (expanded_offset, priority, expanded_event) in enumerate(
                consumed_event.expand(current_offset)
            ):
                self._queue.put(
                    (expanded_offset, priority, (index, subindex), expanded_event)
                )
            self._queue.put(
                (
                    float(current_offset + consumed_event.delta),
                    Priority.NONE,
                    (index, 0),
                    None,
                )
            )
        except StopIteration:
            pass
        return False

    def _stop_callback(
        self, context: ClockCallbackState, *args, **kwargs
    ) -> ClockDelta:
        with self._lock:
            # Do we need to rebuild the queue? Yes.
            # Do we need to free all playing notes? Yes.
            # How do we handle when there are already stop events in the queue?
            # They'll be no-ops when performed.
            self._is_stopping = True
            self._clock.reschedule(
                self._clock_event_id, schedule_at=context.desired_moment.offset
            )
            self._reschedule_queue(context.desired_moment.offset)
            self._free_all_notes(context.desired_moment.seconds)
            self._clock_event_id = -1
            self._clock_stop_event_id = -1
        return None

    def _enumerate(
        self, iterator: Generator[Event, bool, None]
    ) -> Generator[tuple[int, Event], bool, None]:
        index = 0
        should_stop = False
        while True:
            try:
                if index:
                    should_stop = (
                        yield (index, iterator.send(should_stop)) or should_stop
                    )
                else:
                    should_stop = yield (index, next(iterator))
            except StopIteration:
                return
            index += 1

    def _free_all_notes(self, current_seconds: float) -> None:
        if not self._notes_by_uuid:
            return
        with self._context.at(current_seconds):
            while self._notes_by_uuid:
                uuid, _ = self._notes_by_uuid.popitem()
                if not isinstance(node := self._proxies_by_uuid.pop(uuid), Node):
                    raise RuntimeError
                self._context.free_node(node)

    def _reschedule_queue(self, current_offset: float) -> None:
        events: list[tuple[float, Priority, int | tuple[int, int], Event | None]] = []
        while not self._queue.empty():
            events.append(self._queue.get())
        if not events:
            return
        delta = events[0][0] - current_offset
        for event in events:
            offset, priority, index, event_ = event
            self._queue.put((offset - delta, priority, index, event_))

    def play(
        self,
        quantization: Quantization | None = None,
        until: float | None = None,
    ) -> None:
        with self._lock:
            if self._is_running:
                return
            self._iterator = self._enumerate(iter(self._pattern))
            self._queue.put((float("-inf"), Priority.NONE, (0, 0), None))
            self._is_running = True
            self._is_stopping = False
            self._yielded = False
            self._players.add(self)
        self._clock_event_id = self._clock.cue(
            self._clock_callback,
            event_type=3,
            quantization=quantization,
        )
        if until:
            self._clock_stop_event_id = self._clock.schedule(
                self._stop_callback, event_type=2, schedule_at=until
            )

    def stop(self, quantization: Quantization | None = None) -> None:
        with self._lock:
            if not self._is_running or self._is_stopping:
                return
            # If we're stopping earlier than the until parameter, cancel the current stop callback
            if self._clock_stop_event_id != -1:
                self._clock.cancel(self._clock_stop_event_id)
            self._clock.cue(
                self._stop_callback, event_type=2, quantization=quantization
            )
            self._players.remove(self)

    def uuid_to_note_id(self, uuid: UUID, index: int | None = None) -> float:
        if index is not None:
            return self._notes_by_uuid[uuid, index]
        return self._notes_by_uuid[uuid]

    @property
    def initial_seconds(self) -> float | None:
        return self._initial_seconds

    @property
    def uuid(self) -> UUID:
        return self._uuid
