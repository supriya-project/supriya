import dataclasses
import enum
import fractions
import itertools
import logging
import queue
import threading
import time
import traceback
from typing import Any, Callable, Dict, Optional, Set, Tuple

logger = logging.getLogger(__name__.lower())


def measure_to_offset(
    measure: int,
    time_signature: Tuple[int, int],
    previous_measure: int,
    previous_time_signature_change_offset: float,
) -> float:
    return (
        (measure - previous_measure) * (time_signature[0] / time_signature[1])
    ) + previous_time_signature_change_offset


def offset_to_measure(
    offset: float,
    time_signature: Tuple[int, int],
    previous_measure: int,
    previous_time_signature_change_offset: float,
) -> int:
    return (
        int(
            (offset - previous_time_signature_change_offset)
            // (time_signature[0] / time_signature[1])
        )
        + previous_measure
    )


def offset_to_measure_offset(
    offset: float,
    time_signature: Tuple[int, int],
    previous_time_signature_change_offset: float,
) -> float:
    return (offset - previous_time_signature_change_offset) % (
        time_signature[0] / time_signature[1]
    )


def offset_to_seconds(
    beats_per_minute: float,
    current_offset: float,
    previous_offset: float,
    previous_time: float,
    beat_duration: float,
) -> float:
    return (
        (current_offset - previous_offset) / (beats_per_minute / 60) / beat_duration
    ) + previous_time


def seconds_to_offset(
    beats_per_minute: float,
    current_time: float,
    previous_offset: float,
    previous_time: float,
    beat_duration: float,
) -> float:
    return (
        (current_time - previous_time) * (beats_per_minute / 60) * beat_duration
    ) + previous_offset


class EventQueue(queue.PriorityQueue):
    """
    A priority queue with peeking and item removal.

    ::

        >>> from supriya.clock import EventQueue
        >>> from dataclasses import dataclass, field
        >>> from typing import Any

    ::

        >>> @dataclass(frozen=True, order=True)
        ... class PrioritizedItem:
        ...     priority: int
        ...     item: Any=field(compare=False)
        ...

    ::

        >>> item_a = PrioritizedItem(priority=3, item="three")
        >>> item_b = PrioritizedItem(priority=0, item="zero")
        >>> item_c = PrioritizedItem(priority=2, item="two")
        >>> item_d = PrioritizedItem(priority=1, item="one")

    ::

        >>> pq = EventQueue()
        >>> pq.put(item_a)
        >>> pq.put(item_b)
        >>> pq.put(item_c)
        >>> pq.put(item_d)

    ::

        >>> pq.get()
        (0, PrioritizedItem(priority=0, item='zero'))

    ::

        >>> pq.peek()
        1

    ::

        >>> pq.get()
        (1, PrioritizedItem(priority=1, item='one'))

    ::

        >>> pq.remove(item_c)

    ::

        >>> pq.get()
        (3, PrioritizedItem(priority=3, item='three'))

    """

    ### PRIVATE METHODS ###

    def _init(self, maxsize):
        self.queue = []
        self.items = {}

    # TODO: Ditch priority lookup, let item sort itself

    def _put(self, item):
        entry = [item.priority, item, True]
        if item in self.items:
            self.items[item][-1] = False
        self.items[item] = entry
        super()._put(entry)

    def _get(self):
        while self.queue:
            priority, item, active = super()._get()
            if active:
                del self.items[item]
                return priority, item
        raise queue.Empty

    ### PUBLIC METHODS ###

    def clear(self):
        with self.mutex:
            self._init(None)

    def peek(self):
        with self.mutex:
            priority, item = self._get()
            entry = [priority, item, True]
            self.items[item] = entry
            super()._put(entry)
        return priority

    def remove(self, item):
        with self.mutex:
            entry = self.items.pop(item)
            entry[-1] = False


class TimeUnit(enum.IntEnum):
    BEATS = 0
    SECONDS = 1
    MEASURES = 2


class EventType(enum.IntEnum):
    CHANGE = 0
    SCHEDULE = 1


@dataclasses.dataclass(frozen=True)
class SchedulerEvent:
    seconds: float
    event_type: int
    event_id: int
    measure: Optional[int]
    offset: Optional[float]


@dataclasses.dataclass(frozen=True, order=True)
class ChangeEvent(SchedulerEvent):
    beats_per_minute: Optional[float] = dataclasses.field(compare=False)
    time_signature: Optional[Tuple[int, int]] = dataclasses.field(compare=False)

    @property
    def priority(self):
        return (self.seconds, self.event_type, self.event_id)


@dataclasses.dataclass(frozen=True, order=True)
class CallbackEvent(SchedulerEvent):
    procedure: Callable
    args: Tuple[Any, ...] = dataclasses.field(compare=False)
    kwargs: Optional[Dict[str, Any]] = dataclasses.field(compare=False)
    start_time: float = dataclasses.field(compare=False)
    invocations: int = dataclasses.field(compare=False)

    @property
    def priority(self):
        return (self.seconds, self.event_type, self.event_id)


@dataclasses.dataclass(frozen=True)
class Moment:
    __slots__ = (
        "beats_per_minute",
        "measure",
        "measure_offset",
        "offset",
        "time",
        "time_signature",
    )
    beats_per_minute: float
    measure: int
    measure_offset: float
    offset: float
    time: float
    time_signature: Tuple[int, int]


class TempoClock:
    """
    A tempo clock.

    ::

        >>> from supriya.clock import TempoClock
        >>> tempo_clock = TempoClock()
        >>> tempo_clock.start()

    ::

        >>> def callback(curren_moment, desired_moment, event, *args, **kwargs):
        ...     print((
        ...         f"Now: {desired_moment.time}\t"
        ...         f"{desired_moment.offset}\t{event.invocations}"
        ...     ))
        ...     if event.invocations < 10:
        ...         return 0.25 * (event.invocations + 1)
        ...

    ::

        >>> tempo_clock.schedule(callback, schedule_at=0.5)  # doctest: +SKIP
        Now: 1557405529.107658  503.5   0
        Now: 1557405529.232717  503.75  1
        Now: 1557405529.48273   504.25  2
        Now: 1557405529.857601  505.0   3
        Now: 1557405530.357594  506.0   4
        Now: 1557405530.9826088 507.25  5
        Now: 1557405531.7326021 508.75  6
        Now: 1557405532.6076071 510.5   7
        Now: 1557405533.607612  512.5   8
        Now: 1557405534.7327209 514.75  9
        Now: 1557405535.9825962 517.25  10

    """

    # TODO: Use separate dataclass (or instance) for desired moment vs current moment
    # TODO: Pass desired and current moment as separate arguments to callbacks

    ### CLASS VARIABLES ###

    _valid_quantizations = frozenset(
        [
            "8M",
            "4M",
            "2M",
            "1M",
            "1/2",
            "1/2T",
            "1/4",
            "1/4T",
            "1/8",
            "1/8T",
            "1/16",
            "1/16T",
            "1/32",
        ]
    )

    __slots__ = (
        "_beats_per_minute",
        "_condition",
        "_counter",
        "_events_by_id",
        "_is_running",
        "_lock",
        "_measure_relative_event_ids",
        "_name",
        "_offset_relative_event_ids",
        "_previous_measure",
        "_previous_offset",
        "_previous_time",
        "_previous_time_signature_change_offset",
        "_queue",
        "_slop",
        "_thread",
        "_time_signature",
    )

    ### INITIALIZER ###

    def __init__(self, name: Optional[str] = None):
        self._name = name
        # Mechanics
        self._lock = threading.RLock()
        self._condition = threading.Condition(self._lock)
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._is_running = False
        self._slop: float = 0.0001
        self._counter = itertools.count()
        self._queue = EventQueue()
        self._measure_relative_event_ids: Set[SchedulerEvent] = set()
        self._offset_relative_event_ids: Set[SchedulerEvent] = set()
        self._events_by_id: Dict[int, SchedulerEvent] = {}
        # Time keeping
        self._beats_per_minute: float = 120.0
        self._previous_measure: int = 1
        self._previous_offset: float = 0.0
        self._previous_time: float = 0.0
        self._previous_time_signature_change_offset: float = 0.0
        self._time_signature: Tuple[int, int] = (4, 4)

    ### PRIVATE METHODS ###

    def _add_to_queue(self, event) -> int:
        with self._lock:
            self._events_by_id[event.event_id] = event
            if event.offset is not None:
                self._offset_relative_event_ids.add(event.event_id)
            if event.measure is not None:
                self._measure_relative_event_ids.add(event.event_id)
            self._queue.put(event)
            self._condition.notify()
            return event.event_id

    def _event_to_moment(self, event):
        offset = (
            event.offset
            if event.offset is not None
            else self._seconds_to_offset(event.seconds)
        )
        measure = (
            event.measure
            if event.measure is not None
            else self._offset_to_measure(offset)
        )
        measure_offset = self._offset_to_measure_offset(offset)
        return Moment(
            beats_per_minute=self._beats_per_minute,
            measure=measure,
            measure_offset=measure_offset,
            offset=offset,
            time=event.seconds,
            time_signature=self._time_signature,
        )

    def _get_next_timepoints(
        self, schedule_at: float, unit: TimeUnit
    ) -> Tuple[Optional[int], Optional[float], float]:
        measure: Optional[int] = None
        offset: Optional[float] = None
        if unit == TimeUnit.MEASURES:
            measure = int(schedule_at)
            offset = self._measure_to_offset(measure)
            seconds: float = self._offset_to_seconds(offset)
        elif unit == TimeUnit.BEATS:
            offset = float(schedule_at)
            seconds = self._offset_to_seconds(schedule_at)
        else:
            seconds = float(schedule_at)
        return measure, offset, seconds

    def _measure_to_offset(self, measure: int) -> float:
        return measure_to_offset(
            measure,
            self._time_signature,
            self._previous_measure,
            self._previous_time_signature_change_offset,
        )

    def _offset_to_measure(self, offset: float) -> int:
        return offset_to_measure(
            offset,
            self._time_signature,
            self._previous_measure,
            self._previous_time_signature_change_offset,
        )

    def _offset_to_measure_offset(self, offset: float) -> float:
        return offset_to_measure_offset(
            offset, self._time_signature, self._previous_time_signature_change_offset
        )

    def _offset_to_seconds(self, offset: float) -> float:
        return offset_to_seconds(
            beats_per_minute=self._beats_per_minute,
            current_offset=offset,
            previous_offset=self._previous_offset,
            previous_time=self._previous_time,
            beat_duration=1 / self._time_signature[1],
        )

    def _seconds_to_offset(self, seconds: float) -> float:
        return seconds_to_offset(
            beats_per_minute=self._beats_per_minute,
            current_time=seconds,
            previous_offset=self._previous_offset,
            previous_time=self._previous_time,
            beat_duration=1 / self._time_signature[1],
        )

    def _peek(self) -> float:
        with self._lock:
            seconds, _, _ = self._queue.peek()
            return seconds

    def _perform_events(self, current_moment):
        logger.debug(f"[{self.name}] ... Ready to perform at {current_moment.time}s")
        # Perform all events that are ready
        while self._queue.qsize():
            _, event = self._queue.get()
            desired_time = event.seconds
            if current_moment.time < desired_time:
                self._queue.put(event)
                break
            self._events_by_id.pop(event.event_id)
            if event.offset:
                self._offset_relative_event_ids.remove(event.event_id)
            if event.measure:
                self._measure_relative_event_ids.remove(event.event_id)
            # Customize the moment for the current event
            desired_moment = self._event_to_moment(event)
            if event.event_type == EventType.CHANGE:
                current_moment, should_continue = self._perform_change_event(
                    event, current_moment, desired_moment
                )
                if not should_continue:
                    break
            else:
                self._perform_callback_event(event, current_moment, desired_moment)
        return current_moment

    def _perform_change_event(self, event, current_moment, desired_moment):
        logger.debug(
            f"[{self.name}] ... ... Performing change at {desired_moment.time}s"
        )
        # TODO: current offset is misleading here
        if event.time_signature is not None:
            new_duration = event.time_signature[0] / event.time_signature[1]
            self._time_signature = event.time_signature
            if desired_moment.measure_offset < new_duration:
                # On the downbeat
                self._previous_time_signature_change_offset = (
                    desired_moment.offset - desired_moment.measure_offset
                )
                self._previous_measure = desired_moment.measure
            else:
                # Moving from a longer time signature to a shorter one
                # Advance to the next downbeat immediately
                self._previous_measure = desired_moment.measure + 1
                self._previous_time_signature_change_offset = desired_moment.offset
            self._reschedule_measure_relative_events()
            current_moment = dataclasses.replace(
                current_moment,
                time_signature=self._time_signature,
                measure=self._offset_to_measure(current_moment.offset),
                measure_offset=self._offset_to_measure_offset(current_moment.offset),
            )
        if event.beats_per_minute is not None:
            # If the tempo changed, we need to revise our offset math
            self._beats_per_minute = float(event.beats_per_minute)
            self._previous_time = desired_moment.time
            self._previous_offset = desired_moment.offset
            self._reschedule_offset_relative_events()
            new_current_offset = self._seconds_to_offset(current_moment.time)
            if new_current_offset < current_moment.offset:
                logger.debug(
                    f"[{self.name}] ... ... ... Revised offset from "
                    f"{current_moment.offset} to {new_current_offset}"
                )
                current_moment = dataclasses.replace(
                    current_moment, offset=new_current_offset
                )
                return current_moment, False
        return current_moment, True

    def _perform_callback_event(self, event, current_moment, desired_moment):
        try:
            logger.debug(
                f"[{self.name}] ... ... Performing {event.procedure} at "
                f"{desired_moment.time}s"
            )
            result = event.procedure(
                current_moment,
                desired_moment,
                event,
                *event.args,
                **(event.kwargs or {}),
            )
        except Exception:
            traceback.print_exc()
            return
        try:
            delta, unit = result
        except TypeError:
            delta, unit = result, TimeUnit.BEATS
        if not delta or delta <= 0:
            return
        kwargs = {"invocations": event.invocations + 1, "measure": None, "offset": None}
        if unit == TimeUnit.MEASURES:
            kwargs["measure"] = desired_moment.measure + delta
            kwargs["offset"] = self._measure_to_offset(kwargs["measure"])
        if unit == TimeUnit.BEATS:
            kwargs["offset"] = desired_moment.offset + delta
        if unit in (TimeUnit.BEATS, TimeUnit.MEASURES):
            kwargs["seconds"] = self._offset_to_seconds(kwargs["offset"])
        if unit == TimeUnit.SECONDS:
            kwargs["seconds"] = desired_moment.time + delta
        logger.debug(
            f"[{self.name}] ... ... ... Rescheduling "
            f"{event.procedure} at {kwargs['seconds']}s"
        )
        event = dataclasses.replace(event, **kwargs)
        self._add_to_queue(event)

    def _reschedule_offset_relative_events(self):
        for event_id in tuple(self._offset_relative_event_ids):
            event = self.cancel(event_id)
            seconds = self._offset_to_seconds(event.offset)
            logger.debug(
                f"[{self.name}] ... ... ... Rescheduling offset-relative event from "
                f"{event.seconds} to {seconds}"
            )
            self._add_to_queue(dataclasses.replace(event, seconds=seconds))

    def _reschedule_measure_relative_events(self):
        for event_id in tuple(self._measure_relative_event_ids):
            event = self.cancel(event_id)
            offset = self._measure_to_offset(event.measure)
            seconds = self._offset_to_seconds(offset)
            logger.debug(
                f"[{self.name}] ... ... ... Rescheduling measure-relative event from "
                f"offset {event.offset} to {offset}"
            )
            self._add_to_queue(
                dataclasses.replace(event, offset=offset, seconds=seconds)
            )

    def _run(self, *args, **kwargs):
        with self._lock:
            logger.debug(
                f"[{self.name}] Starting offset {self._previous_offset} at "
                f"{self._previous_time} seconds"
            )
            self._reschedule_measure_relative_events()
            self._reschedule_offset_relative_events()
            while self._is_running:
                logger.debug(f"[{self.name}] Loop start")
                if not self._wait_for_queue():
                    break
                current_moment = self._wait_for_moment()
                if current_moment is None:
                    break
                current_moment = self._perform_events(current_moment)
                self._previous_time = current_moment.time
                self._previous_offset = current_moment.offset
                self._condition.wait(timeout=self._slop)
            logger.debug(f"[{self.name}] ... ... Terminating")

    def _wait_for_queue(self) -> bool:
        logger.debug(f"[{self.name}] ... Waiting for something to schedule")
        while not self._queue.qsize():
            self._condition.wait(timeout=self._slop)
            if not self._is_running:
                return False
        return True

    def _wait_for_moment(self) -> Optional[Moment]:
        moment = self.get_current_moment()
        next_time = self._peek()
        logger.debug(
            f"[{self.name}] ... Event found, waiting from {moment.time}s "
            f"until {next_time}s"
        )
        while moment.time < next_time:
            # Cache our current point in time
            self._previous_time = moment.time
            self._previous_offset = moment.offset
            self._condition.wait(timeout=self._slop)
            if not self._is_running:
                return None
            moment = self.get_current_moment()
            logger.debug(f"[{self.name}] ... ... Now waiting at {moment.time}")
            next_time = self._peek()
        self._previous_time = moment.time
        self._previous_offset = moment.offset
        return moment

    ### PUBLIC METHODS ###

    def cancel(self, event_id) -> SchedulerEvent:
        with self._lock:
            event = self._events_by_id.pop(event_id, None)
            if event is None:
                raise KeyError(event_id)
            if event.offset:
                self._offset_relative_event_ids.remove(event_id)
            if event.measure:
                self._measure_relative_event_ids.remove(event_id)
            self._queue.remove(event)
            return event

    def change(
        self,
        beats_per_minute: Optional[float] = None,
        time_signature: Optional[Tuple[int, int]] = None,
    ) -> Optional[int]:
        with self._lock:
            if not self._is_running:
                self._beats_per_minute = beats_per_minute or self._beats_per_minute
                self._time_signature = time_signature or self._time_signature
                return None
            moment = self.get_current_moment()
            event_id = next(self._counter)
            event = ChangeEvent(
                beats_per_minute=beats_per_minute,
                event_id=event_id,
                event_type=EventType.CHANGE,
                measure=None,
                offset=moment.offset,
                seconds=moment.time,
                time_signature=time_signature,
            )
            logging.debug(f"[{self.name}] Changing {event} now")
            return self._add_to_queue(event)

    def cue(
        self,
        procedure,
        *,
        event_type=EventType.SCHEDULE,
        quantization=None,
        args=(),
        kwargs=None,
    ) -> int:
        assert 0 < event_type
        with self._lock:
            moment = self.get_current_moment()
            if quantization is None:
                offset, measure = moment.offset, None
            elif quantization not in self._valid_quantizations:
                raise ValueError(f"Invalid quantization: {quantization}")
            elif "M" in quantization:
                measure_grid = int(quantization[0])
                measure = (
                    (((moment.measure - 1) // measure_grid) * measure_grid)
                    + measure_grid
                    + 1
                )
                offset = self._measure_to_offset(measure)
            else:
                measure = None
                fraction_grid = fractions.Fraction(quantization.replace("T", ""))
                if "T" in quantization:
                    fraction_grid *= fractions.Fraction(2, 3)
                div, mod = divmod(moment.offset, fraction_grid)
                offset = float(div * fraction_grid)
                if mod:
                    offset += fraction_grid
            seconds = self._offset_to_seconds(offset)
            event_id = next(self._counter)
            event = CallbackEvent(
                args=args,
                event_id=event_id,
                event_type=event_type,
                invocations=0,
                kwargs=kwargs,
                measure=measure,
                offset=float(offset),
                procedure=procedure,
                seconds=seconds,
                start_time=self.get_current_time(),
            )
            logging.debug(f"[{self.name}] Cueing {procedure} at {offset}")
            return self._add_to_queue(event)

    def get_current_moment(self):
        current_time = self.get_current_time()
        current_offset = self._seconds_to_offset(current_time)
        current_measure, current_measure_offset = divmod(
            current_offset - self._previous_time_signature_change_offset,
            self._time_signature[0] / self._time_signature[1],
        )
        moment = Moment(
            beats_per_minute=self._beats_per_minute,
            measure=int(current_measure + self._previous_measure),
            measure_offset=current_measure_offset,
            offset=current_offset,
            time=current_time,
            time_signature=self._time_signature,
        )
        return moment

    def get_current_time(self) -> float:
        return time.time()

    def reschedule(
        self, event_id, *, earliest_wins=False, schedule_at=0.0, unit=TimeUnit.BEATS
    ) -> bool:
        with self._lock:
            if earliest_wins:
                _, _, new_seconds = self._get_next_timepoints(schedule_at, unit)
                if self._events_by_id[event_id].seconds < new_seconds:
                    return False
            event = self.cancel(event_id)
            if isinstance(event, CallbackEvent):
                self.schedule(
                    event.procedure,
                    schedule_at=schedule_at,
                    args=event.args,
                    kwargs=event.kwargs,
                    unit=unit,
                )
            elif isinstance(event, ChangeEvent):
                self.schedule_change(
                    beats_per_minute=event.beats_per_minute,
                    schedule_at=schedule_at,
                    time_signature=event.time_signature,
                    unit=unit,
                )
            return True

    def schedule(
        self,
        procedure,
        *,
        schedule_at: float = 0.0,
        event_type=EventType.SCHEDULE,
        unit=TimeUnit.BEATS,
        args=(),
        kwargs=None,
    ) -> int:
        assert 0 < event_type
        with self._lock:
            measure, offset, seconds = self._get_next_timepoints(schedule_at, unit)
            event_id = next(self._counter)
            event = CallbackEvent(
                args=args,
                event_id=event_id,
                event_type=event_type,
                invocations=0,
                kwargs=kwargs,
                measure=measure,
                offset=offset,
                procedure=procedure,
                seconds=seconds,
                start_time=self.get_current_time(),
            )
            logging.debug(
                f"[{self.name}] Scheduling {procedure} at {schedule_at} "
                f"{unit.name.lower()}"
            )
            return self._add_to_queue(event)

    def schedule_change(
        self,
        *,
        schedule_at: float = 0.0,
        unit=TimeUnit.BEATS,
        beats_per_minute: Optional[float] = None,
        time_signature: Optional[Tuple[int, int]] = None,
    ) -> int:
        with self._lock:
            measure, offset, seconds = self._get_next_timepoints(schedule_at, unit)
            event_id = next(self._counter)
            event = ChangeEvent(
                beats_per_minute=beats_per_minute,
                event_id=event_id,
                event_type=EventType.CHANGE,
                measure=measure,
                offset=offset,
                seconds=seconds,
                time_signature=time_signature,
            )
            logging.debug(
                f"[{self.name}] Scheduling {event} at {schedule_at} "
                f"{unit.name.lower()}"
            )
            return self._add_to_queue(event)

    def start(
        self,
        initial_time: Optional[float] = None,
        initial_offset: float = 0.0,
        initial_measure: int = 1,
        beats_per_minute: Optional[float] = None,
        time_signature: Optional[Tuple[int, int]] = None,
    ):
        if self._is_running:
            raise RuntimeError
        with self._lock:
            if initial_time is None:
                initial_time = self.get_current_time()
            self._time_signature = time_signature or self._time_signature
            self._beats_per_minute = beats_per_minute or self._beats_per_minute
            self._previous_measure = int(initial_measure)
            self._previous_offset = float(initial_offset)
            self._previous_time = float(initial_time)
            self._previous_time_signature_change_offset = self._previous_offset
            self._is_running = True
            self._thread = threading.Thread(target=self._run, args=(self,), daemon=True)
            self._thread.start()

    def stop(self):
        if not self._is_running:
            return
        self._is_running = False
        with self._lock:
            self._condition.notify()
        self._thread.join()
        self._queue.clear()
        self._offset_relative_event_ids.clear()
        self._measure_relative_event_ids.clear()
        self._events_by_id.clear()

    ### PUBLIC PROPERTIES ###

    @property
    def beats_per_minute(self) -> float:
        return self._beats_per_minute

    @property
    def is_running(self) -> bool:
        return self._is_running

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def slop(self) -> float:
        return self._slop

    @slop.setter
    def slop(self, slop: float):
        if slop <= 0:
            raise ValueError(slop)
        self._slop = float(slop)

    @property
    def time_signature(self) -> Tuple[int, int]:
        return self._time_signature
