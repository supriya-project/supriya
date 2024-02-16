import dataclasses
import enum
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


class CallbackCommand(NamedTuple):
    args: Optional[Tuple]
    event_id: int
    event_type: int
    kwargs: Optional[Dict]
    procedure: Callable
    quantization: Optional[Quantization]
    schedule_at: float
    time_unit: Optional[TimeUnit]


class CallbackEvent(NamedTuple):
    seconds: float
    event_type: int
    event_id: int
    measure: Optional[int]
    offset: Optional[float]
    procedure: Callable
    args: Optional[Tuple]
    kwargs: Optional[Dict]
    invocations: int

    def __hash__(self):
        return hash((type(self), self.event_id))


class ChangeCommand(NamedTuple):
    beats_per_minute: Optional[float]
    event_id: int
    event_type: int
    quantization: Optional[Quantization]
    schedule_at: float
    time_signature: Optional[Tuple[int, int]]
    time_unit: Optional[TimeUnit]


class ChangeEvent(NamedTuple):
    seconds: float
    event_type: int
    event_id: int
    measure: Optional[int]
    offset: Optional[float]
    beats_per_minute: Optional[float]
    time_signature: Optional[Tuple[int, int]]

    def __hash__(self):
        return hash((type(self), self.event_id))


class ClockContext(NamedTuple):
    current_moment: Moment
    desired_moment: Moment
    event: Union[CallbackEvent, ChangeEvent]
