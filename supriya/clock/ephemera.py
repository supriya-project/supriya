import dataclasses
import enum
from typing import Callable, Dict, NamedTuple, Optional, Tuple, Union


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
    offset: float
    seconds: float
    time_signature: Tuple[int, int]


class CallbackCommand(NamedTuple):
    args: Optional[Tuple]
    event_id: int
    event_type: int
    kwargs: Optional[Dict]
    procedure: Callable
    quantization: Optional[str]
    schedule_at: float
    time_unit: Optional[int]


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
    quantization: Optional[str]
    schedule_at: float
    time_signature: Optional[Tuple[int, int]]
    time_unit: Optional[int]


class ChangeEvent(NamedTuple):
    seconds: float
    event_type: int
    event_id: int
    measure: Optional[int]
    offset: Optional[float]
    beats_per_minute: float
    time_signature: Tuple[int, int]

    def __hash__(self):
        return hash((type(self), self.event_id))


class ClockContext(NamedTuple):
    current_moment: Moment
    desired_moment: Moment
    event: Union[CallbackEvent, ChangeEvent]
