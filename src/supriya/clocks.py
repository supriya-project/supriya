import asyncio
import atexit
import collections
import dataclasses
import enum
import fractions
import itertools
import logging
import queue
import threading
import time
import traceback
from collections.abc import Sequence
from contextlib import asynccontextmanager, contextmanager
from functools import total_ordering
from typing import (
    Any,
    AsyncGenerator,
    Awaitable,
    Deque,
    Generator,
    Generic,
    Literal,
    NamedTuple,
    Protocol,
    TypeAlias,
    TypeVar,
)

from . import conversions

logger = logging.getLogger(__name__)

Quantization = Literal[
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
    "1/32T",
    "1/64",
    "1/64T",
    "1/128",
]


class EventType(enum.IntEnum):
    CHANGE = 0
    SCHEDULE = 1


class TimeUnit(enum.IntEnum):
    BEATS = 0
    SECONDS = 1
    MEASURES = 2


class ClockState(NamedTuple):
    beats_per_minute: float
    initial_seconds: float
    previous_measure: int
    previous_offset: float
    previous_seconds: float
    previous_time_signature_change_offset: float
    time_signature: tuple[int, int]


@dataclasses.dataclass(frozen=True, slots=True)
class Moment:
    beats_per_minute: float
    measure: int
    measure_offset: float
    offset: float  # the beat since zero
    seconds: float  # the seconds since zero
    time_signature: tuple[int, int]


@dataclasses.dataclass(frozen=True)
class Action:
    event_id: int
    event_type: int


@dataclasses.dataclass(frozen=True)
class Command(Action):
    quantization: Quantization | None
    schedule_at: float
    time_unit: TimeUnit | None


ClockDelta: TypeAlias = float | tuple[float, TimeUnit] | None


class ClockCallback(Protocol):
    def __call__(
        self, state: "ClockCallbackState", *args: Any, **kwargs: Any
    ) -> ClockDelta:
        pass


class AsyncClockCallback(Protocol):
    def __call__(
        self, state: "ClockCallbackState", *args: Any, **kwargs: Any
    ) -> Awaitable[ClockDelta] | ClockDelta:
        pass


@dataclasses.dataclass(frozen=True)
class CallbackCommand(Command):
    args: tuple | None
    kwargs: dict | None
    procedure: AsyncClockCallback | ClockCallback


@dataclasses.dataclass(frozen=True)
class ChangeCommand(Command):
    beats_per_minute: float | None
    time_signature: tuple[int, int] | None


@total_ordering
@dataclasses.dataclass(frozen=True, eq=False)
class Event(Action):
    seconds: float
    measure: int | None
    offset: float | None

    def __eq__(self, other: object) -> bool:
        # Need to act like a tuple here
        if not isinstance(other, Event):
            return NotImplemented
        return (self.seconds, self.event_type, self.event_id) == (
            other.seconds,
            other.event_type,
            other.event_id,
        )

    def __lt__(self, other: object) -> bool:
        # Need to act like a tuple here
        if not isinstance(other, Event):
            return NotImplemented
        return (self.seconds, self.event_type, self.event_id) < (
            other.seconds,
            other.event_type,
            other.event_id,
        )


@dataclasses.dataclass(frozen=True, eq=False)
class CallbackEvent(Event):
    procedure: AsyncClockCallback | ClockCallback
    args: tuple | None
    kwargs: dict | None
    invocations: int

    def __hash__(self) -> int:
        return hash((type(self), self.event_id))


@dataclasses.dataclass(frozen=True, eq=False)
class ChangeEvent(Event):
    beats_per_minute: float | None
    time_signature: tuple[int, int] | None

    def __hash__(self) -> int:
        return hash((type(self), self.event_id))


class ClockCallbackState(NamedTuple):
    current_moment: Moment
    desired_moment: Moment
    event: CallbackEvent


class _EventQueue(queue.PriorityQueue[Event]):
    ### PRIVATE METHODS ###

    def _init(self, maxsize: int | None) -> None:
        self.queue: list[Event] = []
        self.flags: dict[Event, bool] = {}

    def _put(self, event: Event) -> None:
        self.flags[event] = True
        super()._put(event)

    def _get(self) -> Event:
        while self.queue:
            if not self.flags.pop((event := super()._get()), None):
                continue
            return event
        raise queue.Empty

    ### PUBLIC METHODS ###

    def clear(self) -> None:
        with self.mutex:
            self._init(None)

    def peek(self) -> Event:
        with self.mutex:
            self._put(event := self._get())
        return event

    def remove(self, event: Event) -> None:
        with self.mutex:
            self.flags.pop(event, None)


C = TypeVar("C", bound=AsyncClockCallback | ClockCallback)


class BaseClock(Generic[C]):
    ### CLASS VARIABLES ###

    _valid_quantizations: frozenset[Quantization] = frozenset(
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
            "1/32T",
            "1/64",
            "1/64T",
            "1/128",
        ]
    )

    ### INITIALIZER ###

    def __init__(self) -> None:
        self._name = None
        self._counter = itertools.count()
        self._command_deque: Deque[Command] = collections.deque()
        self._event_queue = _EventQueue()
        self._is_running = False
        self._slop = 0.001
        self._actions_by_id: dict[int, Action] = {}
        self._measure_relative_event_ids: set[int] = set()
        self._offset_relative_event_ids: set[int] = set()
        self._state = ClockState(
            beats_per_minute=120.0,
            initial_seconds=0.0,
            previous_measure=1,
            previous_offset=0.0,
            previous_seconds=0.0,
            previous_time_signature_change_offset=0.0,
            time_signature=(4, 4),
        )

    ### TIME METHODS ###

    def _get_cue_point(
        self, seconds: float, quantization: Quantization
    ) -> tuple[float, float, int | None]:
        moment = self._seconds_to_moment(seconds)
        if quantization is None:
            offset: float = moment.offset
            measure: int | None = None
        elif "M" in quantization:
            measure_grid = int(quantization[0])
            grid_offset = moment.measure - 1 + (moment.measure_offset > 0)
            count, modulus = divmod(grid_offset, measure_grid)
            count += modulus > 0
            measure = (count * measure_grid) + 1
            offset = self._measure_to_offset(measure)
        else:
            measure = None
            fraction_grid = self._quantization_to_beats(quantization)
            div, mod = divmod(moment.offset, fraction_grid)
            offset = float(div * fraction_grid)
            if mod:
                offset += fraction_grid
        seconds = self._offset_to_seconds(offset)
        logger.debug(
            f"[{self.name}] ... ... Cueing {quantization} to "
            f"{seconds}:s / {offset}:o / {measure}:m"
        )
        return seconds, offset, measure

    def _get_current_time(self) -> float:
        return time.time()

    def _get_initial_time(self) -> float:
        return self._get_current_time()

    def _get_schedule_point(
        self, schedule_at: float, time_unit: TimeUnit
    ) -> tuple[float, float | None, int | None]:
        measure: int | None = None
        offset: float | None = None
        if time_unit == TimeUnit.MEASURES:
            measure = int(schedule_at)
            offset = self._measure_to_offset(measure)
            seconds: float = self._offset_to_seconds(offset)
        elif time_unit == TimeUnit.BEATS:
            offset = float(schedule_at)
            seconds = self._offset_to_seconds(schedule_at)
        else:
            seconds = float(schedule_at)
        return seconds, offset, measure

    def _measure_to_offset(self, measure: int) -> float:
        return conversions.measure_to_offset(
            measure,
            self._state.time_signature,
            self._state.previous_measure,
            self._state.previous_time_signature_change_offset,
        )

    def _offset_to_measure(self, offset: float) -> int:
        return conversions.offset_to_measure(
            offset,
            self._state.time_signature,
            self._state.previous_measure,
            self._state.previous_time_signature_change_offset,
        )

    def _offset_to_measure_offset(self, offset: float) -> float:
        return conversions.offset_to_measure_offset(
            offset,
            self._state.time_signature,
            self._state.previous_time_signature_change_offset,
        )

    def _offset_to_moment(self, offset: float) -> Moment:
        seconds = self._offset_to_seconds(offset)
        measure, measure_offset = divmod(
            offset - self._state.previous_time_signature_change_offset,
            self._state.time_signature[0] / self._state.time_signature[1],
        )
        return Moment(
            beats_per_minute=self._state.beats_per_minute,
            measure=int(measure + self._state.previous_measure),
            measure_offset=measure_offset,
            offset=offset,
            seconds=seconds,
            time_signature=self._state.time_signature,
        )

    def _offset_to_seconds(self, offset: float) -> float:
        return conversions.offset_to_seconds(
            beats_per_minute=self._state.beats_per_minute,
            current_offset=offset,
            previous_offset=self._state.previous_offset,
            previous_seconds=self._state.previous_seconds,
            beat_duration=1 / self._state.time_signature[1],
        )

    def _peek(self) -> Event | None:
        try:
            return self._event_queue.peek()
        except queue.Empty:
            return None

    def _quantization_to_beats(self, quantization: Quantization) -> float:
        fraction = fractions.Fraction(quantization.replace("T", ""))
        if "T" in quantization:
            fraction *= fractions.Fraction(2, 3)
        return float(fraction)

    def _seconds_to_moment(self, seconds: float) -> Moment:
        offset = self._seconds_to_offset(seconds)
        measure, measure_offset = divmod(
            offset - self._state.previous_time_signature_change_offset,
            self._state.time_signature[0] / self._state.time_signature[1],
        )
        return Moment(
            beats_per_minute=self._state.beats_per_minute,
            measure=int(measure + self._state.previous_measure),
            measure_offset=measure_offset,
            offset=offset,
            seconds=seconds,
            time_signature=self._state.time_signature,
        )

    def _seconds_to_offset(self, seconds: float) -> float:
        return conversions.seconds_to_offset(
            beats_per_minute=self._state.beats_per_minute,
            current_time=seconds,
            previous_offset=self._state.previous_offset,
            previous_seconds=self._state.previous_seconds,
            beat_duration=1 / self._state.time_signature[1],
        )

    ### SCHEDULING METHODS ###

    def _cancel(self, event_id: int) -> Action | None:
        action = self._actions_by_id.pop(event_id, None)
        if action is not None and isinstance(action, Event):
            self._event_queue.remove(action)
            if action.offset is not None:
                self._offset_relative_event_ids.remove(action.event_id)
                if action.measure is not None:
                    self._measure_relative_event_ids.remove(action.event_id)
        return action

    def _enqueue_command(self, command: Command) -> None:
        self._actions_by_id[command.event_id] = command
        self._command_deque.append(command)
        if isinstance(command, CallbackCommand):
            logger.debug(
                f"[{self.name}] Enqueued {type(command).__name__} ({command.event_id}) {command.procedure}"
            )
        else:
            logger.debug(
                f"[{self.name}] Enqueued {type(command).__name__} ({command.event_id})"
            )

    def _enqueue_event(self, event: Event) -> None:
        self._actions_by_id[event.event_id] = event
        self._event_queue.put(event)
        if event.offset is not None:
            self._offset_relative_event_ids.add(event.event_id)
            if event.measure is not None:
                self._measure_relative_event_ids.add(event.event_id)

    def _process_perform_event_loop(
        self, current_moment: Moment
    ) -> tuple[Event | None, Moment | None, bool, bool]:
        # There may be items in the queue which have been flagged "removed".
        # They contribute to the queue's size, but cannot be retrieved by .get().
        try:
            event = self._event_queue.get()
        except queue.Empty:
            return None, None, True, False
        if self._actions_by_id.pop(event.event_id, None) is None:
            return None, None, True, False
        if current_moment.seconds < event.seconds:
            self._enqueue_event(event)
            return None, None, False, True
        if event.offset is not None:
            desired_moment = self._offset_to_moment(event.offset)
        else:
            desired_moment = self._seconds_to_moment(event.seconds)
        if event.offset is not None and event.offset != desired_moment.offset:
            raise RuntimeError(
                f"Offset mismatch: {event.offset} vs {desired_moment.offset}"
            )
        return event, desired_moment, False, False

    def _perform_callback_event(
        self, event: CallbackEvent, current_moment: Moment, desired_moment: Moment
    ) -> None:
        logger.debug(
            f"[{self.name}] ... ... Performing {event.procedure} at "
            f"{desired_moment.seconds - self._state.initial_seconds}:s / "
            f"{desired_moment.offset}:o"
        )
        state = ClockCallbackState(current_moment, desired_moment, event)
        args = event.args or ()
        kwargs = event.kwargs or {}
        try:
            result = event.procedure(state, *args, **kwargs)
        except Exception:
            traceback.print_exc()
            return
        assert not isinstance(result, Awaitable)
        if isinstance(result, float) or result is None:
            delta, time_unit = result, TimeUnit.BEATS
        else:
            delta, time_unit = result
        self._process_callback_event_result(desired_moment, event, delta, time_unit)

    def _process_callback_event_result(
        self,
        desired_moment: Moment,
        event: CallbackEvent,
        delta: float | None,
        time_unit: TimeUnit,
    ) -> None:
        if delta is None or delta <= 0:
            return
        invocations = event.invocations + 1
        measure: int | None = None
        offset: float | None = None
        if time_unit in (TimeUnit.BEATS, TimeUnit.MEASURES):
            if time_unit == TimeUnit.MEASURES:
                measure = desired_moment.measure + int(delta)
                offset = self._measure_to_offset(measure)
            else:
                offset = desired_moment.offset + delta
            seconds = self._offset_to_seconds(offset)
        else:
            seconds = desired_moment.seconds + delta
        logger.debug(
            f"[{self.name}] ... ... ... Rescheduling "
            f"{event.procedure} ({event.event_id}) at {seconds - self._state.initial_seconds}s"
        )
        event = dataclasses.replace(
            event,
            invocations=invocations,
            measure=measure,
            offset=offset,
            seconds=seconds,
        )
        self._enqueue_event(event)

    def _perform_change_event(
        self, event: ChangeEvent, current_moment: Moment, desired_moment: Moment
    ) -> tuple[Moment, bool]:
        logger.debug(
            f"[{self.name}] ... ... Changing at "
            f"{desired_moment.seconds - self._state.initial_seconds}:s"
        )
        # TODO: current offset is misleading here
        if event.time_signature is not None:
            new_duration = event.time_signature[0] / event.time_signature[1]
            if desired_moment.measure_offset < new_duration:
                # On the downbeat
                self._state = self._state._replace(
                    previous_measure=desired_moment.measure,
                    previous_time_signature_change_offset=(
                        desired_moment.offset - desired_moment.measure_offset
                    ),
                    time_signature=event.time_signature,
                )
            else:
                # Moving from a longer time signature to a shorter one
                # Advance to the next downbeat immediately
                self._state = self._state._replace(
                    previous_measure=desired_moment.measure + 1,
                    previous_time_signature_change_offset=desired_moment.offset,
                    time_signature=event.time_signature,
                )
            self._reschedule_measure_relative_events()
            current_moment = dataclasses.replace(
                current_moment,
                time_signature=self._state.time_signature,
                measure=self._offset_to_measure(current_moment.offset),
                measure_offset=self._offset_to_measure_offset(current_moment.offset),
            )
        if event.beats_per_minute is not None:
            # If the tempo changed, we need to revise our offset math
            self._state = self._state._replace(
                beats_per_minute=float(event.beats_per_minute),
                previous_seconds=desired_moment.seconds,
                previous_offset=desired_moment.offset,
            )
            self._reschedule_offset_relative_events()
            new_current_offset = self._seconds_to_offset(current_moment.seconds)
            logger.debug(
                f"[{self.name}] ... ... ... Revised offset from "
                f"{current_moment.offset} to {new_current_offset}"
            )
            current_moment = dataclasses.replace(
                current_moment, offset=new_current_offset
            )
            return current_moment, False
            # if new_current_offset < current_moment.offset:
            #    return current_moment, False
        return current_moment, True

    def _perform_events(self, current_moment: Moment) -> Moment:
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
            if event is None or desired_moment is None:
                raise ValueError(event, desired_moment)
            if isinstance(event, ChangeEvent):
                current_moment, should_continue = self._perform_change_event(
                    event, current_moment, desired_moment
                )
                if not should_continue:
                    break
            elif isinstance(event, CallbackEvent):
                self._perform_callback_event(event, current_moment, desired_moment)
                self._process_command_deque()
            else:
                raise ValueError(event)
        return current_moment

    def _process_command_deque(self, first_run: bool = False) -> None:
        while self._command_deque:
            logger.debug(f"[{self.name}] ... Processing command deque ({first_run})")
            command = self._command_deque.popleft()
            if self._actions_by_id.pop(command.event_id, None) is None:
                continue
            schedule_at = command.schedule_at
            logger.debug(f"[{self.name}] ... ... Scheduled at {schedule_at}")
            if command.quantization is not None:
                seconds: float
                offset: float | None
                measure: int | None
                # If the command was queued before the clock was started,
                # reset its reference time
                if first_run and schedule_at < self._state.initial_seconds:
                    schedule_at = self._state.initial_seconds
                seconds, offset, measure = self._get_cue_point(
                    schedule_at, command.quantization
                )
            elif command.time_unit in (TimeUnit.BEATS, TimeUnit.MEASURES):
                seconds, offset, measure = self._get_schedule_point(
                    schedule_at, command.time_unit
                )
            else:
                if first_run:
                    schedule_at += self._state.initial_seconds
                seconds, offset, measure = schedule_at, None, None
            if isinstance(command, CallbackCommand):
                event: CallbackEvent | ChangeEvent = CallbackEvent(
                    args=command.args,
                    event_id=command.event_id,
                    kwargs=command.kwargs,
                    measure=measure,
                    offset=offset,
                    procedure=command.procedure,
                    seconds=seconds,
                    event_type=command.event_type,
                    invocations=0,
                )
            elif isinstance(command, ChangeCommand):
                event = ChangeEvent(
                    beats_per_minute=command.beats_per_minute,
                    event_id=command.event_id,
                    event_type=command.event_type,
                    measure=measure,
                    offset=offset,
                    seconds=seconds,
                    time_signature=command.time_signature,
                )
            else:
                raise ValueError(command)
            self._enqueue_event(event)
            logger.debug(
                f"[{self.name}] ... ... Enqueued {type(event).__name__} "
                f"({event.event_id}) for {event.seconds}:s / {event.offset}:o"
            )

    def _reschedule_offset_relative_events(self) -> None:
        for event_id in tuple(self._offset_relative_event_ids):
            action = self._cancel(event_id)
            if action is None or not isinstance(action, Event) or action.offset is None:
                self._offset_relative_event_ids.remove(event_id)
                continue
            seconds = self._offset_to_seconds(action.offset)
            logger.debug(
                f"[{self.name}] ... ... ... Rescheduling offset-relative event "
                f"({action.event_id}) from "
                f"{action.seconds - self._state.initial_seconds}:s to "
                f"{seconds - self._state.initial_seconds}:s"
            )
            self._enqueue_event(dataclasses.replace(action, seconds=seconds))

    def _reschedule_measure_relative_events(self) -> None:
        for event_id in tuple(self._measure_relative_event_ids):
            action = self._cancel(event_id)
            if (
                action is None
                or not isinstance(action, Event)
                or action.measure is None
            ):
                self._measure_relative_event_ids.remove(event_id)
                continue
            offset = self._measure_to_offset(action.measure)
            seconds = self._offset_to_seconds(offset)
            logger.debug(
                f"[{self.name}] ... ... ... Rescheduling measure-relative event from "
                f"offset {action.offset} to {offset}"
            )
            self._enqueue_event(
                dataclasses.replace(action, offset=offset, seconds=seconds)
            )

    def _start(
        self,
        initial_time: float | None = None,
        initial_offset: float = 0.0,
        initial_measure: int = 1,
        beats_per_minute: float | None = None,
        time_signature: tuple[int, int] | None = None,
    ) -> None:
        if self._is_running:
            raise RuntimeError("Already started")
        # TODO: This if block only makes sense in online clocks
        if initial_time is None:
            initial_time = self._get_initial_time()
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

    def _stop(self) -> bool:
        if not self._is_running:
            return False
        self._is_running = False
        return True

    ### PUBLIC METHODS ###

    def cancel(self, event_id: int) -> Action | None:
        logger.debug(f"[{self.name}] Canceling {event_id}")
        event = self._cancel(event_id)
        return event

    def change(
        self,
        beats_per_minute: float | None = None,
        time_signature: tuple[int, int] | None = None,
    ) -> int | None:
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
            schedule_at=self._get_current_time(),
            time_unit=None,
        )
        self._enqueue_command(command)
        return event_id

    def cue(
        self,
        procedure: C,
        quantization: Quantization | None = None,
        *,
        args: Sequence[Any] | None = None,
        event_type: int = EventType.SCHEDULE,
        kwargs: dict[str, Any] | None = None,
    ) -> int:
        if event_type <= 0:
            raise ValueError(f"Invalid event type {event_type}")
        elif quantization is not None and quantization not in self._valid_quantizations:
            raise ValueError(f"Invalid quantization: {quantization}")
        event_id = next(self._counter)
        command = CallbackCommand(
            args=tuple(args) if args else (),
            event_id=event_id,
            event_type=event_type,
            kwargs=kwargs,
            procedure=procedure,
            quantization=quantization,
            schedule_at=self._get_current_time() if self.is_running else 0,
            time_unit=None,
        )
        self._enqueue_command(command)
        return event_id

    def cue_change(
        self,
        quantization: Quantization | None = None,
        *,
        beats_per_minute: float | None = None,
        time_signature: tuple[int, int] | None = None,
    ) -> int:
        if quantization is not None and quantization not in self._valid_quantizations:
            raise ValueError(f"Invalid quantization: {quantization}")
        event_id = next(self._counter)
        command = ChangeCommand(
            beats_per_minute=beats_per_minute,
            event_id=event_id,
            event_type=EventType.CHANGE,
            quantization=quantization,
            schedule_at=self._get_current_time() if self.is_running else 0,
            time_signature=time_signature,
            time_unit=None,
        )
        self._enqueue_command(command)
        return event_id

    def reschedule(
        self,
        event_id: int,
        schedule_at: float = 0.0,
        *,
        time_unit: TimeUnit = TimeUnit.BEATS,
    ) -> int | None:
        if (event_or_command := self.cancel(event_id)) is None:
            return None
        if isinstance(event_or_command, Command):
            command: Command = dataclasses.replace(
                event_or_command, schedule_at=schedule_at, time_unit=time_unit
            )
        elif isinstance(event_or_command, CallbackEvent):
            command = CallbackCommand(
                args=event_or_command.args,
                event_id=event_or_command.event_id,
                event_type=event_or_command.event_type,
                kwargs=event_or_command.kwargs,
                procedure=event_or_command.procedure,
                quantization=None,
                schedule_at=schedule_at,
                time_unit=time_unit,
            )
        elif isinstance(event_or_command, ChangeEvent):
            command = ChangeCommand(
                beats_per_minute=event_or_command.beats_per_minute,
                event_id=event_or_command.event_id,
                event_type=EventType.CHANGE,
                quantization=None,
                schedule_at=schedule_at,
                time_signature=event_or_command.time_signature,
                time_unit=time_unit,
            )
        else:
            raise ValueError(event_or_command)
        self._enqueue_command(command)
        return event_id

    def schedule(
        self,
        procedure: C,
        schedule_at: float = 0.0,
        *,
        args: Sequence[Any] | None = None,
        event_type: int = EventType.SCHEDULE,
        kwargs: dict[str, Any] | None = None,
        time_unit: TimeUnit = TimeUnit.BEATS,
    ) -> int:
        logger.debug(f"[{self.name}] Scheduling {procedure}")
        if event_type <= 0:
            raise ValueError(f"Invalid event type {event_type}")
        event_id = next(self._counter)
        command = CallbackCommand(
            args=tuple(args) if args else (),
            event_id=event_id,
            event_type=event_type,
            kwargs=kwargs,
            procedure=procedure,
            quantization=None,
            schedule_at=schedule_at,
            time_unit=time_unit,
        )
        self._enqueue_command(command)
        return event_id

    def schedule_change(
        self,
        schedule_at: float = 0.0,
        *,
        beats_per_minute: float | None = None,
        time_signature: tuple[int, int] | None = None,
        time_unit: TimeUnit = TimeUnit.BEATS,
    ) -> int:
        event_id = next(self._counter)
        command = ChangeCommand(
            beats_per_minute=beats_per_minute,
            event_id=event_id,
            event_type=EventType.CHANGE,
            quantization=None,
            schedule_at=schedule_at,
            time_signature=time_signature,
            time_unit=time_unit,
        )
        self._enqueue_command(command)
        return event_id

    ### PUBLIC PROPERTIES ###

    @property
    def beats_per_minute(self) -> float:
        return self._state.beats_per_minute

    @property
    def is_running(self) -> bool:
        return self._is_running

    @property
    def name(self) -> str | None:
        return self._name

    @property
    def slop(self) -> float:
        return self._slop

    @slop.setter
    def slop(self, slop: float) -> None:
        if slop <= 0:
            raise ValueError(slop)
        self._slop = float(slop)

    @property
    def time_signature(self) -> tuple[int, int]:
        return self._state.time_signature


class Clock(BaseClock[ClockCallback]):
    """
    A threaded clock.
    """

    ### INITIALIZER ###

    def __init__(self) -> None:
        BaseClock.__init__(self)
        self._event = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        atexit.register(self.stop)

    ### SCHEDULING METHODS ###

    def _enqueue_command(self, command: Command) -> None:
        super()._enqueue_command(command)
        self._event.set()

    def _run(self, offline: bool = False) -> None:
        logger.debug(f"[{self.name}] Thread start")
        self._process_command_deque(first_run=True)
        while self._is_running:
            logger.debug(f"[{self.name}] Loop start")
            if not self._wait_for_queue():
                break
            try:
                current_moment = self._wait_for_moment()
            except queue.Empty:
                continue
            if current_moment is None:
                break
            current_moment = self._perform_events(current_moment)
            self._state = self._state._replace(
                previous_seconds=current_moment.seconds,
                previous_offset=current_moment.offset,
            )
            if not offline:
                self._event.wait(timeout=self._slop)
        logger.debug(f"[{self.name}] Terminating")
        self._stop()

    def _wait_for_moment(self, offline: bool = False) -> Moment | None:
        current_time = self._get_current_time()
        next_time = self._event_queue.peek().seconds
        logger.debug(
            f"[{self.name}] ... Waiting for next moment at {next_time} from {current_time}"
        )
        while current_time < next_time:
            if not offline:
                self._event.wait(timeout=self._slop)
            if not self._is_running:
                return None
            self._process_command_deque()
            next_time = self._event_queue.peek().seconds
            current_time = self._get_current_time()
            self._event.clear()
        return self._seconds_to_moment(current_time)

    def _wait_for_queue(self, offline: bool = False) -> bool:
        logger.debug(f"[{self.name}] ... Waiting for events")
        self._process_command_deque()
        self._event.clear()
        while not self._event_queue.qsize():
            if not offline:
                self._event.wait(timeout=self._slop)
            if not self._is_running:
                return False
            self._process_command_deque()
            self._event.clear()
        return True

    ### PUBLIC METHODS ###

    def cancel(self, event_id: int) -> Action | None:
        event = super().cancel(event_id)
        self._event.set()
        return event

    def start(
        self,
        initial_time: float | None = None,
        initial_offset: float = 0.0,
        initial_measure: int = 1,
        beats_per_minute: float | None = None,
        time_signature: tuple[int, int] | None = None,
    ) -> None:
        self._start(
            initial_time=initial_time,
            initial_offset=initial_offset,
            initial_measure=initial_measure,
            beats_per_minute=beats_per_minute,
            time_signature=time_signature,
        )
        self._thread = threading.Thread(target=self._run, args=(self,), daemon=True)
        self._thread.start()

    def stop(self) -> None:
        if self._stop():
            self._event.set()
            self._thread.join()


class AsyncClock(BaseClock[AsyncClockCallback]):
    """
    An async clock.
    """

    ### INITIALIZER ###

    def __init__(self) -> None:
        BaseClock.__init__(self)
        self._task: Awaitable[None] | None = None
        self._slop = 1.0
        try:
            self._event = asyncio.Event()
        except RuntimeError:
            pass

    ### SCHEDULING METHODS ###

    def _enqueue_command(self, command: Command) -> None:
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
        state = ClockCallbackState(current_moment, desired_moment, event)
        args = event.args or ()
        kwargs = event.kwargs or {}
        try:
            if asyncio.iscoroutine(result := event.procedure(state, *args, **kwargs)):
                result = await result
        except Exception:
            traceback.print_exc()
            return
        assert not isinstance(result, Awaitable)
        if isinstance(result, float) or result is None:
            delta, time_unit = result, TimeUnit.BEATS
        else:
            delta, time_unit = result
        self._process_callback_event_result(desired_moment, event, delta, time_unit)

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
            if event is None or desired_moment is None:
                raise ValueError(event, desired_moment)
            if isinstance(event, ChangeEvent):
                current_moment, should_continue = self._perform_change_event(
                    event, current_moment, desired_moment
                )
                if not should_continue:
                    break
            elif isinstance(event, CallbackEvent):
                await self._perform_callback_event_async(
                    event, current_moment, desired_moment
                )
                self._process_command_deque()
            else:
                raise ValueError(event)
        return current_moment

    async def _run_async(self, offline: bool = False) -> None:
        logger.debug(f"[{self.name}] Coroutine start")
        self._process_command_deque(first_run=True)
        while self._is_running:
            logger.debug(f"[{self.name}] Loop start")
            if not await self._wait_for_queue_async():
                break
            try:
                if (current_moment := await self._wait_for_moment_async()) is None:
                    break
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

    async def _wait_for_moment_async(self, offline: bool = False) -> Moment | None:
        current_time = self._get_current_time()
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
            current_time = self._get_current_time()
            self._event.clear()
        return self._seconds_to_moment(current_time)

    async def _wait_for_queue_async(self, offline: bool = False) -> bool:
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

    def cancel(self, event_id: int) -> Action | None:
        event = super().cancel(event_id)
        self._event.set()
        return event

    async def start(
        self,
        initial_time: float | None = None,
        initial_offset: float = 0.0,
        initial_measure: int = 1,
        beats_per_minute: float | None = None,
        time_signature: tuple[int, int] | None = None,
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


class OfflineClock(BaseClock[ClockCallback]):
    """
    An offline clock.
    """

    ### SCHEDULING METHODS ###

    def _get_current_time(self) -> float:
        return self._state.previous_seconds

    def _get_initial_time(self) -> float:
        return self._state.initial_seconds

    def _perform_callback_event(
        self, event: CallbackEvent, current_moment: Moment, desired_moment: Moment
    ) -> None:
        logger.debug(
            f"[{self.name}] ... ... Performing {event.procedure} at "
            f"{desired_moment.seconds - self._state.initial_seconds}:s / "
            f"{desired_moment.offset}:o"
        )
        state = ClockCallbackState(current_moment, desired_moment, event)
        args = event.args or ()
        kwargs = event.kwargs or {}
        result = event.procedure(state, *args, **kwargs)
        assert not isinstance(result, Awaitable)
        if isinstance(result, float) or result is None:
            delta, time_unit = result, TimeUnit.BEATS
        else:
            delta, time_unit = result
        self._process_callback_event_result(desired_moment, event, delta, time_unit)

    def _run(self, offline: bool = False):
        logger.debug(f"[{self.name}] Thread start")
        self._process_command_deque(first_run=True)
        while self._is_running and self._event_queue.qsize():
            logger.debug(f"[{self.name}] Loop start")
            if not self._wait_for_queue():
                break
            try:
                if (current_moment := self._wait_for_moment()) is None:
                    break
            except queue.Empty:
                continue
            current_moment = self._perform_events(current_moment)
            self._state = self._state._replace(
                previous_seconds=current_moment.seconds,
                previous_offset=current_moment.offset,
            )
        logger.debug(f"[{self.name}] Terminating")
        self._stop()

    def _wait_for_moment(self, offline: bool = False) -> Moment | None:
        current_time = self._event_queue.peek().seconds
        return self._seconds_to_moment(current_time)

    def _wait_for_queue(self, offline: bool = False) -> bool:
        logger.debug(f"[{self.name}] ... Waiting for events")
        self._process_command_deque()
        return True

    ### PUBLIC METHODS ###

    @contextmanager
    def at(
        self,
        initial_time: float | None = None,
        initial_offset: float = 0.0,
        initial_measure: int = 1,
        beats_per_minute: float | None = None,
        time_signature: tuple[int, int] | None = None,
    ) -> Generator["OfflineClock", None, None]:
        yield self
        self.start(
            initial_time=initial_time,
            initial_offset=initial_offset,
            initial_measure=initial_measure,
            beats_per_minute=beats_per_minute,
            time_signature=time_signature,
        )

    def start(
        self,
        initial_time: float | None = None,
        initial_offset: float = 0.0,
        initial_measure: int = 1,
        beats_per_minute: float | None = None,
        time_signature: tuple[int, int] | None = None,
    ) -> None:
        self._start(
            initial_time=initial_time,
            initial_offset=initial_offset,
            initial_measure=initial_measure,
            beats_per_minute=beats_per_minute,
            time_signature=time_signature,
        )
        self._run()

    def stop(self) -> None:
        return


class AsyncOfflineClock(AsyncClock):
    ### SCHEDULING METHODS ###

    def _get_current_time(self) -> float:
        return self._state.previous_seconds

    def _get_initial_time(self) -> float:
        return self._state.initial_seconds

    async def _run_async(self, offline: bool = False) -> None:
        logger.debug(f"[{self.name}] Coroutine start")
        self._process_command_deque(first_run=True)
        while self._is_running and self._event_queue.qsize():
            logger.debug(f"[{self.name}] Loop start")
            if not await self._wait_for_queue_async():
                break
            try:
                if (current_moment := await self._wait_for_moment_async()) is None:
                    break
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

    async def _wait_for_moment_async(self, offline: bool = False) -> Moment | None:
        current_time = self._event_queue.peek().seconds
        self._process_command_deque()
        self._event.clear()
        return self._seconds_to_moment(current_time)

    async def _wait_for_queue_async(self, offline: bool = False) -> bool:
        logger.debug(f"[{self.name}] ... Waiting for events")
        self._process_command_deque()
        self._event.clear()
        return True

    ### PUBLIC METHODS ###

    @asynccontextmanager
    async def at(
        self,
        initial_time: float | None = None,
        initial_offset: float = 0.0,
        initial_measure: int = 1,
        beats_per_minute: float | None = None,
        time_signature: tuple[int, int] | None = None,
    ) -> AsyncGenerator["AsyncOfflineClock", None]:
        yield self
        await self.start(
            initial_time=initial_time,
            initial_offset=initial_offset,
            initial_measure=initial_measure,
            beats_per_minute=beats_per_minute,
            time_signature=time_signature,
        )

    async def start(
        self,
        initial_time: float | None = None,
        initial_offset: float = 0.0,
        initial_measure: int = 1,
        beats_per_minute: float | None = None,
        time_signature: tuple[int, int] | None = None,
    ) -> None:
        self._start(
            initial_time=initial_time,
            initial_offset=initial_offset,
            initial_measure=initial_measure,
            beats_per_minute=beats_per_minute,
            time_signature=time_signature,
        )
        await self._run_async()

    async def stop(self) -> None:
        return
