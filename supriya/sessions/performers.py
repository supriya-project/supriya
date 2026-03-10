import dataclasses
import logging
from collections import deque
from typing import (
    Callable,
    Deque,
    Generator,
    Type,
)

from .constants import IO, PolyphonyMode

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
    velocity: float = 0.0


class Performer:
    def __init__(self) -> None:
        self._input_note_numbers: list[float] = []
        self._output_note_numbers: set[float] = set()
        self._performance_event_handlers: dict[
            Type[PerformanceEvent],
            Callable[[PerformanceEvent, IO], list[PerformanceEvent]],
        ] = {
            NoteOn: self._on_note_on,
            NoteOff: self._on_note_off,
        }
        self._polyphony_limit: int | None = None
        self._polyphony_mode: PolyphonyMode = PolyphonyMode.FREE_OLDEST
        self._retrigger: bool = False

    def _apply_polyphony(
        self,
        *,
        note_number: float,
        polyphony_mode: PolyphonyMode,
        polyphony_limit: int,
    ) -> list[PerformanceEvent]:
        events: list[PerformanceEvent] = []
        if (count := len(self._input_note_numbers) - polyphony_limit) < 1:
            return events
        if polyphony_mode == PolyphonyMode.FREE_OLDEST:
            for _ in range(count):
                events.append(NoteOff(note_number=self._input_note_numbers.pop(0)))
            return events
        if polyphony_mode == PolyphonyMode.FREE_LOWEST:
            sorted_note_numbers = sorted(self._input_note_numbers)
        elif polyphony_mode == PolyphonyMode.FREE_HIGHEST:
            sorted_note_numbers = sorted(self._input_note_numbers, reverse=True)
        elif polyphony_mode == PolyphonyMode.FREE_NEAREST:
            sorted_note_numbers = sorted(
                self._input_note_numbers, key=lambda x: (abs(x - note_number), x)
            )
        for i in range(count):
            self._input_note_numbers.remove(note_number := sorted_note_numbers[i])
            events.append(NoteOff(note_number=note_number))
        return events

    def _flush(self) -> None:
        logger.info("flushing: self=%s", self)
        self._perform_loop(
            self,
            IO.READ,
            [
                NoteOff(note_number=note_number, velocity=0)
                for note_number in self._input_note_numbers
            ],
        )

    def _next_performers(self, io: IO) -> Generator[tuple["Performer", IO], None, None]:
        # N.B. This needs to be implemented on a per-performer basis because it
        # depends on the session structure in a type-aware way.
        raise NotImplementedError

    def _on_note_off(self, event: PerformanceEvent, io: IO) -> list[PerformanceEvent]:
        assert isinstance(event, NoteOff)
        events: list[PerformanceEvent] = []
        if io == IO.READ:
            if event.note_number in self._input_note_numbers:
                self._input_note_numbers.remove(event.note_number)
            events.append(event)
            for event in events:
                self._perform_event(event)
        else:
            if event.note_number in self._output_note_numbers:
                self._output_note_numbers.remove(event.note_number)
            events.append(event)
        return events

    def _on_note_on(self, event: PerformanceEvent, io: IO) -> list[PerformanceEvent]:
        assert isinstance(event, NoteOn)
        events: list[PerformanceEvent] = []
        if io == IO.READ:
            if event.note_number not in self._input_note_numbers:
                if self._polyphony_limit:
                    events.extend(
                        self._apply_polyphony(
                            note_number=event.note_number,
                            polyphony_mode=self._polyphony_mode,
                            polyphony_limit=self._polyphony_limit - 1,
                        )
                    )
                # apply polyphony limit
                self._input_note_numbers.append(event.note_number)
                events.append(event)
            elif self._retrigger:
                events.extend([NoteOff(note_number=event.note_number), event])
            else:
                events.append(event)
            for event in events:
                self._perform_event(event)
        else:
            if event.note_number not in self._output_note_numbers:
                self._output_note_numbers.add(event.note_number)
            events.append(event)
        return events

    def _perform(
        self, io: IO, events: list[PerformanceEvent]
    ) -> Generator[tuple["Performer", IO, list[PerformanceEvent]], None, None]:
        logger.info("    performing: self=%s io=%s events=%s", self, io, events)
        events_: list[PerformanceEvent] = []
        for event in events:
            if callback := self._performance_event_handlers.get(type(event)):
                events_.extend(callback(event, io))
            else:  # pass through
                events_.append(event)
        if events_:
            for performer, io in self._next_performers(io):
                yield performer, io, events_

    def _perform_event(self, event: PerformanceEvent) -> None:
        if isinstance(event, NoteOn):
            self._perform_note_on(event)
        elif isinstance(event, NoteOff):
            self._perform_note_off(event)

    def _perform_note_off(self, event: NoteOff) -> None:
        pass

    def _perform_note_on(self, event: NoteOn) -> None:
        pass

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

    def _set_polyphony_limit(self, limit: int | None) -> None:
        raise NotImplementedError

    def _set_polyphony_mode(self, mode: PolyphonyMode) -> None:
        raise NotImplementedError

    def perform(self, events: list[PerformanceEvent]) -> None:
        self._perform_loop(self, IO.READ, events)
