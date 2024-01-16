from queue import Empty, PriorityQueue, Queue
from threading import RLock
from typing import (
    Callable,
    Coroutine,
    Dict,
    Generator,
    Iterable,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
    cast,
)
from uuid import UUID, uuid4
from weakref import WeakSet

from ..clocks import BaseClock, CallbackEvent, Clock, ClockContext, OfflineClock
from ..contexts import Bus, Context, ContextObject, Node
from .eventpatterns import Pattern
from .events import Event, Priority, StartEvent, StopEvent
from .structure import PinPattern


class PatternPlayer:
    """
    A pattern player.

    Coordinates interactions between a pattern, a clock_context, and a clock.
    """

    # TODO: Rewrite type annotation after dropping 3.8
    _players = cast(Set["PatternPlayer"], WeakSet())

    def __init__(
        self,
        pattern: Pattern,
        context: Context,
        clock: BaseClock,
        callback: Optional[
            Callable[
                ["PatternPlayer", ClockContext, Event, Priority], Optional[Coroutine]
            ]
        ] = None,
        target_bus: Optional[Bus] = None,
        target_node: Optional[Node] = None,
        uuid: Optional[UUID] = None,
    ) -> None:
        self._context = context
        self._clock = clock
        self._callback = callback
        self._lock = RLock()
        self._queue: Queue[
            Tuple[float, Priority, Union[int, Tuple[int, int]], Optional[Event]]
        ] = PriorityQueue()
        self._is_running = False
        self._is_stopping = False
        self._proxies_by_uuid: Dict[Union[UUID, Tuple[UUID, int]], ContextObject] = {}
        self._notes_by_uuid: Dict[Union[UUID, Tuple[UUID, int]], float] = {}
        self._uuid: UUID = uuid or uuid4()
        self._target_bus = target_bus
        self._target_node = target_node
        self._next_delta: Optional[float] = None
        self._initial_seconds: Optional[float] = None
        self._pattern = (
            pattern
            if (target_bus is None and target_node is None)
            else PinPattern(pattern, target_bus=target_bus, target_node=target_node)
        )

    def _clock_callback(
        self, clock_context: ClockContext, *args, **kwargs
    ) -> Optional[float]:
        for clock_context, seconds, offset, events in self._find_events(clock_context):
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
        self, clock_context: ClockContext
    ) -> Iterable[Tuple[ClockContext, float, float, Sequence[Tuple[Event, Priority]]]]:
        with self._lock:
            current_offset = float("-inf")
            events: List[Tuple[Event, Priority]] = []
            if (
                not cast(CallbackEvent, clock_context.event).invocations
                and self._callback
            ):
                yield clock_context, clock_context.desired_moment.seconds, clock_context.desired_moment.offset, [
                    (StartEvent(), Priority.START)
                ]
            while True:
                try:
                    offset, priority, index, event = self._queue.get(block=False)
                except Empty:
                    if events:
                        yield clock_context, clock_context.desired_moment.seconds, current_offset, events
                    self._is_running = False
                    if self._callback:
                        yield clock_context, clock_context.desired_moment.seconds, current_offset, [
                            (StopEvent(), Priority.STOP)
                        ]
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
                        yield clock_context, clock_context.desired_moment.seconds, current_offset, events
                    self._next_delta = delta
                    return
                if not isinstance(event, Event):
                    if self._consume_iterator(offset):
                        if self._callback:
                            yield clock_context, clock_context.desired_moment.seconds, current_offset, [
                                (StopEvent(), Priority.STOP)
                            ]
                        self._next_delta = None
                        return
                elif offset != current_offset:
                    if events:
                        yield clock_context, clock_context.desired_moment.seconds, current_offset, events
                    current_offset = offset
                    events = [(event, priority)]
                else:
                    events.append((event, priority))

    def _consume_iterator(self, current_offset: float) -> bool:
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
        self, clock_context: ClockContext, *args, **kwargs
    ) -> Optional[float]:
        with self._lock:
            # Do we need to rebuild the queue? Yes.
            # Do we need to free all playing notes? Yes.
            # How do we handle when there are already stop events in the queue?
            # They'll be no-ops when performed.
            self._is_stopping = True
            self._clock.reschedule(
                self._clock_event_id, schedule_at=clock_context.desired_moment.offset
            )
            self._reschedule_queue(clock_context.desired_moment.offset)
            self._free_all_notes(clock_context.desired_moment.seconds)
        return None

    def _enumerate(
        self, iterator: Generator[Event, bool, None]
    ) -> Generator[Tuple[int, Event], bool, None]:
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
        events: List[
            Tuple[float, Priority, Union[int, Tuple[int, int]], Optional[Event]]
        ] = []
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
        quantization: Optional[str] = None,
        at: Optional[float] = None,
        until: Optional[float] = None,
    ) -> None:
        with self._lock:
            if self._is_running:
                return
            self._iterator = self._enumerate(iter(self._pattern))
            self._queue.put((float("-inf"), Priority.NONE, (0, 0), None))
            self._is_running = True
            self._is_stopping = False
            self._players.add(self)
        self._clock_event_id = self._clock.cue(
            self._clock_callback,
            event_type=3,
            quantization=quantization,
        )
        if until:
            self._clock.schedule(self._stop_callback, event_type=2, schedule_at=until)
        if (
            isinstance(self._clock, (Clock, OfflineClock))
            and not self._clock.is_running
        ):
            self._clock.start(initial_time=at)

    def stop(self, quantization: Optional[str] = None) -> None:
        with self._lock:
            if not self._is_running or self._is_stopping:
                return
            self._clock.cue(
                self._stop_callback, event_type=2, quantization=quantization
            )
            self._players.remove(self)

    def uuid_to_note_id(self, uuid: UUID, index: Optional[int] = None) -> float:
        if index is not None:
            return self._notes_by_uuid[uuid, index]
        return self._notes_by_uuid[uuid]

    @property
    def initial_seconds(self) -> Optional[float]:
        return self._initial_seconds

    @property
    def uuid(self) -> UUID:
        return self._uuid
