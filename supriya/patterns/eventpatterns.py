from typing import Type
from uuid import uuid4

from uqbar.objects import new

from .events import Event, NoteEvent
from .patterns import Pattern, SequencePattern


class EventPattern(Pattern):
    """
    Akin to SuperCollider's Pbind.
    """

    def __init__(self, event_type: Type[Event] = NoteEvent, **patterns):
        self._patterns = patterns
        self._event_type = event_type

    def _iterate(self, state=None):
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

    def _prepare_patterns(self):
        patterns = self._patterns.copy()
        for name, pattern in sorted(patterns.items()):
            if not isinstance(pattern, Pattern):
                pattern = SequencePattern([pattern], iterations=None)
            patterns[name] = iter(pattern)
        return patterns

    @property
    def event_type(self) -> Type[Event]:
        return self._event_type

    @property
    def is_infinite(self):
        for value in self._patterns.values():
            if isinstance(value, Pattern) and not value.is_infinite:
                return False
        return True


class MonoEventPattern(EventPattern):
    """
    Akin to SuperCollider's Pmono.
    """

    def _iterate(self, state=None):
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
    def is_infinite(self):
        for value in self._patterns.values():
            if isinstance(value, Pattern) and not value.is_infinite:
                return False
        return True


class UpdatePattern(Pattern):
    """
    Akin to SuperCollider's Pbindf.
    """

    def __init__(self, pattern, **patterns):
        self._pattern = pattern
        self._patterns = patterns

    def _iterate(self, state=None):
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

    def _prepare_patterns(self):
        patterns = self._patterns.copy()
        for name, pattern in sorted(patterns.items()):
            if not isinstance(pattern, Pattern):
                pattern = SequencePattern([pattern], iterations=None)
            patterns[name] = iter(pattern)
        return patterns

    @property
    def is_infinite(self):
        for value in self._patterns.values():
            if isinstance(value, Pattern) and not value.is_infinite:
                return False
        return self._pattern.is_infinite


class ChainPattern(Pattern):
    """
    Akin to SuperCollider's Pchain.
    """

    def __init__(self, *patterns):
        self._patterns = tuple(patterns)

    def _iterate(self, state=None):
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
    def is_infinite(self):
        for value in self._patterns:
            if isinstance(value, Pattern) and not value.is_infinite:
                return False
        return True
