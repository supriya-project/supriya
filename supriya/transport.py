import dataclasses
import enum
import fractions
import itertools
import logging
import queue
import threading
import time
import traceback
from typing import Any, Callable, Dict, Optional, Tuple

logger = logging.getLogger(__name__.lower())


def measure_to_offset(
    measure,
    time_signature,
    previous_measure,
    previous_time_signature_change_offset,
):
    return (
        (measure - previous_measure) * (time_signature[0] / time_signature[1])
    ) + previous_time_signature_change_offset


def offset_to_seconds(
    beats_per_minute,
    current_offset,
    previous_offset,
    previous_time,
    beat_duration,
):
    return (
        (current_offset - previous_offset) / (beats_per_minute / 60) / beat_duration
    ) + previous_time


def seconds_to_offset(
    beats_per_minute,
    current_time,
    previous_offset,
    previous_time,
    beat_duration,
):
    return (
        (current_time - previous_time) * (beats_per_minute / 60) * beat_duration
    ) + previous_offset


class EventQueue(queue.PriorityQueue):
    """
    A priority queue with peeking and item removal.

    ::

        >>> from supriya.transport import EventQueue
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
        (0, 1, PrioritizedItem(priority=0, item='zero'))

    ::

        >>> pq.peek()
        1

    ::

        >>> pq.get()
        (1, 3, PrioritizedItem(priority=1, item='one'))

    ::

        >>> pq.remove(item_c)

    ::

        >>> pq.get()
        (3, 0, PrioritizedItem(priority=3, item='three'))

    """

    ### PRIVATE METHODS ###

    def _init(self, maxsize):
        self.queue = []
        self.items = {}

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
    CUE = 1
    SCHEDULE = 2


@dataclasses.dataclass(frozen=True, order=True)
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
        "current_measure",
        "current_measure_offset",
        "current_offset",
        "current_time",
        "desired_measure",
        "desired_offset",
        "desired_time",
        "time_signature",
    )
    beats_per_minute: float
    current_measure: int
    current_measure_offset: float
    current_offset: float
    current_time: float
    desired_measure: Optional[int]
    desired_offset: Optional[float]
    desired_time: Optional[float]
    time_signature: Tuple[int, int]


class Transport:
    """
    A transport.

    ::

        >>> from supriya.transport import Transport
        >>> transport = Transport()
        >>> transport.start()

    ::

        >>> def callback(moment, event, *args, **kwargs):
        ...     print((
        ...         f"Now: {moment.current_time}\t"
        ...         f"{moment.desired_offset}\t{event.invocations}"
        ...     ))
        ...     if event.invocations < 10:
        ...         return 0.25 * (event.invocations + 1)
        ...

    ::

        >>> transport.schedule(callback, schedule_at=0.5)  # doctest: +SKIP
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

    # TODO: Use seconds internally, recompute offset-relative events accordingly

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

    ### INITIALIZER ###

    def __init__(self, name: Optional[str] = None):
        self._name = name
        # Mechanics
        self._lock = threading.RLock()
        self._condition = threading.Condition(self._lock)
        self._thread = None
        self._is_running = False
        self._slop = 0.0001
        self._counter = itertools.count()
        self._queue = EventQueue()
        self._measure_relative_event_ids = set()
        self._offset_relative_event_ids = set()
        self._events_by_id = {}
        # Time keeping
        self._beats_per_minute = 120.0
        self._initial_time = 0.0
        self._previous_measure = 1
        self._previous_offset = 0.0
        self._previous_time = 0.0
        self._previous_time_signature_change_offset = 0.0
        self._time_signature = (4, 4)

    ### PRIVATE METHODS ###

    def _add_to_queue(self, event):
        with self._lock:
            self._events_by_id[event.event_id] = event
            if event.offset:
                self._offset_relative_event_ids.add(event.event_id)
            if event.measure:
                self._measure_relative_event_ids.add(event.event_id)
            self._queue.put(event)
            self._condition.notify()
            return event.event_id

    def _get_current_time(self):
        return time.time()

    def _get_current_moment(self):
        current_time = self._get_current_time()
        current_offset = self._seconds_to_offset(current_time)
        current_measure, current_measure_offset = divmod(
            current_offset - self._previous_time_signature_change_offset,
            self._time_signature[0] / self._time_signature[1],
        )
        moment = Moment(
            beats_per_minute=self._beats_per_minute,
            current_measure=int(current_measure + self._previous_measure),
            current_measure_offset=current_measure_offset,
            current_offset=current_offset,
            current_time=current_time,
            desired_measure=None,
            desired_offset=None,
            desired_time=None,
            time_signature=self._time_signature,
        )
        return moment

    def _measure_to_offset(self, measure):
        return measure_to_offset(
            measure,
            self._time_signature,
            self._previous_measure,
            self._previous_time_signature_change_offset,
        )

    def _offset_to_seconds(self, offset):
        return offset_to_seconds(
            beats_per_minute=self._beats_per_minute,
            current_offset=offset,
            previous_offset=self._previous_offset,
            previous_time=self._previous_time,
            beat_duration=1 / self._time_signature[1],
        )

    def _seconds_to_offset(self, seconds):
        return seconds_to_offset(
            beats_per_minute=self._beats_per_minute,
            current_time=seconds,
            previous_offset=self._previous_offset,
            previous_time=self._previous_time,
            beat_duration=1 / self._time_signature[1],
        )

    def _peek(self):
        offset, _, _ = self._queue.peek()
        return offset

    def _perform_events(self, moment):
        logger.debug(f"[{self.name}] ... Ready to perform at {moment.current_time}s")
        # Perform all events that are ready
        while self._queue.qsize():
            _, event = self._queue.get()
            desired_offset = event.offset
            if moment.current_offset < desired_offset:
                self._queue.put(event)
                break
            self._events_by_id.pop(event.event_id)
            if event.offset:
                self._offset_relative_event_ids.remove(event.event_id)
            if event.measure:
                self._measure_relative_event_ids.remove(event.event_id)
            # Customize the moment for the current event
            desired_time = self._offset_to_seconds(desired_offset)
            moment = dataclasses.replace(
                moment, desired_offset=desired_offset, desired_time=desired_time
            )
            if event.event_type == EventType.CHANGE:
                moment, should_continue = self._perform_change_event(event, moment)
                if not should_continue:
                    break
            else:
                self._perform_callback_event(event, moment)
        self._previous_time = moment.current_time
        self._previous_offset = moment.current_offset

    def _perform_change_event(self, event, moment):
        logger.debug(
            f"[{self.name}] ... ... Performing change at {moment.desired_time}s"
        )
        if event.time_signature is not None:
            old_duration = self._time_signature[0] / self._time_signature[1]
            new_duration = event.time_signature[0] / event.time_signature[1]
            self._time_signature = event.time_signature
            if old_duration <= new_duration:
                # Just set the current last downbeat as the previous meter change offset
                self._previous_time_signature_change_offset = (
                    moment.current_offset - moment.current_measure_offset
                )
                self._previous_measure = moment.current_measure
            elif new_duration < old_duration:
                if new_duration < moment.current_measure_offset:
                    # Advance to the next downbeat immediately
                    self._previous_measure = moment.current_measure + 1
                    self._previous_time_signature_change_offset = moment.current_offset
            self._reschedule_measure_relative_events()
            moment = dataclasses.replace(moment, time_signature=self._time_signature)
        if event.beats_per_minute is not None:
            self._beats_per_minute = float(event.beats_per_minute)
            # If the tempo changed, we need to revise our offset math
            self._previous_time = moment.desired_time
            self._previous_offset = moment.desired_offset
            self._reschedule_offset_relative_events()
            new_current_offset = self._seconds_to_offset(moment.current_time)
            if new_current_offset < moment.current_offset:
                logger.debug(
                    f"[{self.name}] ... ... ... Revised offset from "
                    f"{moment.current_offset} to {new_current_offset}"
                )
                moment = dataclasses.replace(moment, current_offset=new_current_offset)
                return moment, False
        return moment, True

    def _perform_callback_event(self, event, moment):
        try:
            logger.warning(
                f"[{self.name}] ... ... Performing {event.procedure} at "
                f"{moment.desired_time}s"
            )
            result = event.procedure(moment, event, *event.args, **(event.kwargs or {}))
        except Exception:
            traceback.print_exc()
            return
        try:
            delta, unit = result
        except TypeError:
            delta, unit = result, TimeUnit.BEATS
        if not delta or delta <= 0:
            return
        kwargs = {"invocations": event.invocations + 1}
        if unit == TimeUnit.MEASURES:
            kwargs["measure"] = moment.desired_measure + delta
            kwargs["offset"] = self._measure_to_offset(kwargs["measure"])
        if unit == TimeUnit.BEATS:
            kwargs["offset"] = moment.desired_offset + delta
        if unit in (TimeUnit.BEATS, TimeUnit.MEASURES):
            kwargs["seconds"] = self._offset_to_seconds(kwargs["offset"])
        if unit == TimeUnit.SECONDS:
            kwargs["seconds"] = moment.desired_seconds + delta
        logger.warning(
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
                f"{event.offset} to {offset}"
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
            while self._is_running:
                logger.debug(f"[{self.name}] Loop start")
                if not self._wait_for_queue():
                    return
                moment = self._wait_for_moment()
                if moment is None:
                    return
                self._perform_events(moment)

    def _wait_for_queue(self):
        logger.debug(f"[{self.name}] ... Waiting for something to schedule")
        while not self._queue.qsize():
            self._condition.wait(timeout=1.0)
            if not self._is_running:
                logger.debug(f"[{self.name}] ... ... Terminating")
                return False
        return True

    def _wait_for_moment(self):
        moment = self._get_current_moment()
        next_time = self._peek()
        logger.debug(
            f"[{self.name}] ... Event found, waiting from {moment.current_time}s "
            f"until {next_time}s"
        )
        while moment.current_time < next_time:
            # Cache our current point in time
            self._previous_time = moment.current_time
            self._previous_offset = moment.current_offset
            self._condition.wait(timeout=self._slop)
            if not self._is_running:
                logger.debug(f"[{self.name}] ... ... Terminating")
                return
            moment = self._get_current_moment()
            logger.debug(f"[{self.name}] ... ... Now waiting at {moment.current_time}")
            next_time = self._peek()
        self._previous_time = moment.current_time
        self._previous_offset = moment.current_offset
        return moment

    ### PUBLIC METHODS ###

    def cancel(self, event_id):
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

    def cue(self, procedure, *, quantization=None, args=(), kwargs=None):
        with self._lock:
            moment = self._get_current_moment()
            if quantization is None:
                offset, measure = moment.current_offset, None
            elif quantization not in self._valid_quantizations:
                raise ValueError(f"Invalid quantization: {quantization}")
            elif "M" in quantization:
                grid = int(quantization[0])
                measure = (((moment.current_measure - 1) // grid) * grid) + grid + 1
                offset = self._measure_to_offset(measure)
            else:
                measure = None
                grid = fractions.Fraction(quantization.replace("T", ""))
                if "T" in quantization:
                    grid *= fractions.Fraction(2, 3)
                div, mod = divmod(moment.current_offset, grid)
                offset = float(div * grid)
                if mod:
                    offset += grid
            seconds = self._offset_to_seconds(offset)
            event_id = next(self._counter)
            event = CallbackEvent(
                args=args,
                event_id=event_id,
                event_type=EventType.SCHEDULE,
                invocations=0,
                kwargs=kwargs,
                measure=measure,
                offset=float(offset),
                procedure=procedure,
                seconds=seconds,
                start_time=self._get_current_time(),
            )
            logging.debug(f"[{self.name}] Cueing {procedure} at {offset}")
            return self._add_to_queue(event)

    def reschedule(self, event_id, *, earliest_wins=False, schedule_at=0.0, unit=TimeUnit.BEATS):
        with self._lock:
            if earliest_wins:
                if unit == TimeUnit.BEATS:
                    new_seconds = self._offset_to_seconds(schedule_at)
                else:
                    new_seconds = schedule_at
                if self._events_by_id[event_id].seconds < new_seconds:
                    return
            event = self.cancel(event_id)
            self.schedule(
                event.procedure,
                offset=schedule_at,
                args=event.args,
                kwargs=event.kwargs,
                unit=unit,
            )

    def schedule(
        self, procedure, *, schedule_at=0.0, unit=TimeUnit.BEATS, args=(), kwargs=None
    ):
        with self._lock:
            if unit == TimeUnit.BEATS:
                offset = schedule_at
                seconds = self._offset_to_seconds(schedule_at)
            else:
                seconds, offset = schedule_at, None
            event_id = next(self._counter)
            event = CallbackEvent(
                args=args,
                event_id=event_id,
                event_type=EventType.SCHEDULE,
                invocations=0,
                kwargs=kwargs,
                measure=None,
                offset=offset,
                procedure=procedure,
                seconds=seconds,
                start_time=self._get_current_time(),
            )
            logging.debug(
                f"[{self.name}] Scheduling {procedure} at {schedule_at} "
                f"{unit.name.lower()}"
            )
            return self._add_to_queue(event)

    def schedule_change(
        self,
        *,
        schedule_at=0.0,
        unit=TimeUnit.BEATS,
        beats_per_minute=None,
        time_signature=None,
    ):
        with self._lock:
            if unit == TimeUnit.BEATS:
                offset = schedule_at
                seconds = self._offset_to_seconds(schedule_at)
            else:
                seconds, offset = schedule_at, None
            event_id = next(self._counter)
            event = ChangeEvent(
                beats_per_minute=beats_per_minute,
                event_id=event_id,
                event_type=EventType.CHANGE,
                measure=None,
                offset=offset,
                seconds=seconds,
                time_signature=time_signature,
            )
            logging.debug(
                f"[{self.name}] Scheduling {event} at {schedule_at} "
                f"{unit.name.lower()}"
            )
            return self._add_to_queue(event)

    def start(self, initial_time=None, initial_offset=0.0):
        with self._lock:
            if initial_time is None:
                initial_time = self._get_current_time()
            self._initial_time = self._previous_time = initial_time
            self._previous_offset = initial_offset
            self._is_running = True
            self._thread = threading.Thread(target=self._run, args=(self,), daemon=True)
            self._thread.start()

    def stop(self):
        #if not self._is_running:
        #    return
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
    def beats_per_minute(self):
        return self._beats_per_minute

    @beats_per_minute.setter
    def beats_per_minute(self, beats_per_minute):
        beats_per_minute = float(beats_per_minute)
        if beats_per_minute <= 0:
            raise ValueError(beats_per_minute)
        with self._lock:
            self._beats_per_minute = beats_per_minute

    @property
    def is_running(self):
        return self._is_running

    @property
    def name(self):
        return self._name

    @property
    def slop(self):
        return self._slop

    @slop.setter
    def slop(self, slop):
        slop = float(slop)
        if slop <= 0:
            raise ValueError(slop)
        self._slop = slop
