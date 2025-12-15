import dataclasses
import logging
from collections import deque
from typing import (
    Callable,
    Deque,
    Generator,
    Type,
)

from .constants import IO

logger = logging.getLogger(__name__)


@dataclasses.dataclass(frozen=True)
class PerformanceEvent:
    pass


@dataclasses.dataclass(frozen=True)
class NoteOn(PerformanceEvent):
    note_number: float
    velocity: float


@dataclasses.dataclass(frozen=True)
class NoteOff(PerformanceEvent):
    note_number: float
    velocity: float


class Performer:
    def __init__(self) -> None:
        self._note_numbers: list[float] = []
        self._performance_event_handlers: dict[
            Type[PerformanceEvent], Callable[[PerformanceEvent], list[PerformanceEvent]]
        ] = {
            NoteOn: self._on_note_on,
            NoteOff: self._on_note_off,
        }

    def _flush(self) -> None:
        logger.info("flushing: self=%s", self)
        self._perform_loop(
            self,
            IO.READ,
            [
                NoteOff(note_number=note_number, velocity=0)
                for note_number in self._note_numbers
            ],
        )

    def _perform(
        self, io: IO, events: list[PerformanceEvent]
    ) -> Generator[tuple["Performer", IO, list[PerformanceEvent]], None, None]:
        logger.info("performing: self=%s io=%s events=%s", self, io, events)
        events_: list[PerformanceEvent] = []
        if io == IO.READ:
            for event in events:
                if callback := self._performance_event_handlers.get(type(event)):
                    events_.extend(callback(event))
                else:
                    events_.append(event)
        else:
            events_ = events
        if events_:
            for performer, io in self._next_performers(io):
                yield performer, io, events_

    def _next_performers(self, io: IO) -> Generator[tuple["Performer", IO], None, None]:
        # This needs to be implemented on a per-performer basis
        raise NotImplementedError

    def _on_note_on(self, event: PerformanceEvent) -> list[PerformanceEvent]:
        assert isinstance(event, NoteOn)
        if event.note_number in self._note_numbers:
            return []
        self._note_numbers.append(event.note_number)
        return [event]

    def _on_note_off(self, event: PerformanceEvent) -> list[PerformanceEvent]:
        assert isinstance(event, NoteOff)
        if event.note_number not in self._note_numbers:
            return []
        self._note_numbers.remove(event.note_number)
        return [event]

    def _perform_loop(
        self, performer: "Performer", io: IO, events: list[PerformanceEvent]
    ) -> None:
        logger.info(
            "performing loop: self=%s performer=%s io=%s events=%s",
            self,
            performer,
            io,
            events,
        )
        stack: Deque[tuple[Performer, IO, list[PerformanceEvent]]] = deque()
        stack.append((performer, io, events))
        while stack:
            performer, io, events = stack.popleft()
            for performer, io, events in performer._perform(io, events):
                if not events:
                    continue
                stack.append((performer, io, events))

    def perform(self, events: list[PerformanceEvent]) -> None:
        self._perform_loop(self, IO.READ, events)
