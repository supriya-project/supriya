import dataclasses
import enum
from functools import total_ordering
from typing import Callable, Dict, Literal, NamedTuple, Optional, Tuple, Union

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
    time_signature: Tuple[int, int]


@dataclasses.dataclass(frozen=True)
class Moment:
    __slots__ = (
        "beats_per_minute",
        "measure",
        "measure_offset",
        "offset",
        "seconds",
        "time_signature",
    )
    beats_per_minute: float
    measure: int
    measure_offset: float
    offset: float  # the beat since zero
    seconds: float  # the seconds since zero
    time_signature: Tuple[int, int]


@dataclasses.dataclass(frozen=True)
class Action:
    event_id: int
    event_type: int


@dataclasses.dataclass(frozen=True)
class Command(Action):
    quantization: Optional[Quantization]
    schedule_at: float
    time_unit: Optional[TimeUnit]


@dataclasses.dataclass(frozen=True)
class CallbackCommand(Command):
    args: Optional[Tuple]
    kwargs: Optional[Dict]
    procedure: Callable[["ClockContext"], Union[None, float, Tuple[float, TimeUnit]]]


@dataclasses.dataclass(frozen=True)
class ChangeCommand(Command):
    beats_per_minute: Optional[float]
    time_signature: Optional[Tuple[int, int]]


@total_ordering
@dataclasses.dataclass(frozen=True, eq=False)
class Event(Action):
    seconds: float
    measure: Optional[int]
    offset: Optional[float]

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
    procedure: Callable[["ClockContext"], Union[None, float, Tuple[float, TimeUnit]]]
    args: Optional[Tuple]
    kwargs: Optional[Dict]
    invocations: int

    def __hash__(self) -> int:
        return hash((type(self), self.event_id))


@dataclasses.dataclass(frozen=True, eq=False)
class ChangeEvent(Event):
    beats_per_minute: Optional[float]
    time_signature: Optional[Tuple[int, int]]

    def __hash__(self) -> int:
        return hash((type(self), self.event_id))


class ClockContext(NamedTuple):
    current_moment: Moment
    desired_moment: Moment
    event: Union[CallbackEvent, ChangeEvent]
