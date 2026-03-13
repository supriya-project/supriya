from typing import Any, Generator, Type
from uuid import uuid4

from uqbar.objects import new

from ..typing import UUIDDict
from .events import Event, NoteEvent
from .patterns import Pattern, SequencePattern


class EventPattern(Pattern[Event]):
    """
    Akin to SuperCollider's Pbind.
    """

    def __init__(
        self, event_type: Type[NoteEvent] = NoteEvent, **patterns: Any | Pattern
    ) -> None:
        self._event_type = event_type
        self._patterns = patterns

    def _iterate(self, state: UUIDDict | None = None) -> Generator[Event, bool, None]:
        patterns = self._prepare_patterns()
        iterator_pairs = sorted(patterns.items())
        while True:
            event = {}
            for key, pattern in iterator_pairs:
                try:
                    event[key] = next(pattern)
                except StopIteration:
                    return
            if (yield self.event_type(uuid4(), **event)):
                return

    def _prepare_patterns(self) -> dict[str, Generator[Any, bool, None]]:
        generators: dict[str, Generator[Any, bool, None]] = {}
        for name, pattern in sorted(self._patterns.items()):
            if not isinstance(pattern, Pattern):
                pattern = SequencePattern([pattern], iterations=None)
            generators[name] = iter(pattern)
        return generators

    @property
    def event_type(self) -> Type[NoteEvent]:
        return self._event_type

    @property
    def is_infinite(self) -> bool:
        for value in self._patterns.values():
            if isinstance(value, Pattern) and not value.is_infinite:
                return False
        return True


class MonoEventPattern(EventPattern):
    """
    Akin to SuperCollider's Pmono.
    """

    def _iterate(self, state: UUIDDict | None = None) -> Generator[Event, bool, None]:
        id_ = uuid4()
        patterns = self._prepare_patterns()
        iterator_pairs = sorted(patterns.items())
        while True:
            event = {}
            for key, pattern in iterator_pairs:
                try:
                    event[key] = next(pattern)
                except StopIteration:
                    return
            if (yield self.event_type(id_, **event)):
                return

    @property
    def is_infinite(self) -> bool:
        for value in self._patterns.values():
            if isinstance(value, Pattern) and not value.is_infinite:
                return False
        return True


class UpdatePattern(Pattern[Event]):
    """
    Akin to SuperCollider's Pbindf.
    """

    def __init__(self, pattern: Pattern[Event], **patterns: Any | Pattern) -> None:
        self._pattern = pattern
        self._patterns = patterns

    def _iterate(self, state: UUIDDict | None = None) -> Generator[Event, bool, None]:
        event_iterator = iter(self._pattern)
        iterator_pairs = sorted(self._prepare_patterns().items())
        while True:
            try:
                event = next(event_iterator)
            except StopIteration:
                return
            template_dict = {}
            for key, key_iterator in iterator_pairs:
                try:
                    template_dict[key] = next(key_iterator)
                except StopIteration:
                    return
            event = new(event, **template_dict)
            if (yield event):
                return

    def _prepare_patterns(self) -> dict[str, Generator[Any, bool, None]]:
        generators: dict[str, Generator[Any, bool, None]] = {}
        for name, pattern in sorted(self._patterns.items()):
            if not isinstance(pattern, Pattern):
                pattern = SequencePattern([pattern], iterations=None)
            generators[name] = iter(pattern)
        return generators

    @property
    def is_infinite(self) -> bool:
        for value in self._patterns.values():
            if isinstance(value, Pattern) and not value.is_infinite:
                return False
        return self._pattern.is_infinite


class UpdateDictPattern(Pattern[Event]):
    """
    Akin to SuperCollider's Penvir.
    """

    def __init__(self, pattern: Pattern[Event], dictionary: dict[str, Any]) -> None:
        self._pattern = pattern
        self._dictionary = dictionary

    def _iterate(self, state: UUIDDict | None = None) -> Generator[Event, bool, None]:
        event_iterator = iter(self._pattern)
        while True:
            try:
                event = next(event_iterator)
            except StopIteration:
                return
            if (yield new(event, **self._dictionary)):
                return

    @property
    def is_infinite(self) -> bool:
        return self._pattern.is_infinite


class ChainPattern(Pattern[Event]):
    """
    Akin to SuperCollider's Pchain.
    """

    def __init__(self, *patterns: Pattern[Event]) -> None:
        self._patterns = tuple(patterns)

    def _iterate(self, state: UUIDDict | None = None) -> Generator[Event, bool, None]:
        patterns = [iter(_) for _ in self._patterns]
        while True:
            try:
                event = next(patterns[0])
            except StopIteration:
                return
            for pattern in patterns[1:]:
                try:
                    event = event.merge(next(pattern))
                except StopIteration:
                    return
            if (yield event):
                return

    @property
    def is_infinite(self) -> bool:
        for value in self._patterns:
            if isinstance(value, Pattern) and not value.is_infinite:
                return False
        return True
