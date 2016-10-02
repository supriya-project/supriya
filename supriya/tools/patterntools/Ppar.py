# -*- encoding: utf-8 -*-
from abjad import new
try:
    from queue import PriorityQueue
except ImportError:
    from Queue import PriorityQueue
from supriya.tools.patterntools.EventPattern import EventPattern


class Ppar(EventPattern):
    """
    Interleave patterns.

    ::

        >>> one = patterntools.Pbind(
        ...     duration=1.0,
        ...     x=patterntools.Pseq([1, 2, 3, 4]),
        ...     )
        >>> two = patterntools.Pbind(
        ...     duration=0.4,
        ...     x=patterntools.Pseq([10, 20, 30, 40]),
        ...     )
        >>> ppar = patterntools.Ppar([one, two])
        >>> print(format(ppar))
        supriya.tools.patterntools.Ppar(
            (
                supriya.tools.patterntools.Pbind(
                    duration=1.0,
                    x=supriya.tools.patterntools.Pseq(
                        (1, 2, 3, 4),
                        repetitions=1,
                        ),
                    ),
                supriya.tools.patterntools.Pbind(
                    duration=0.4,
                    x=supriya.tools.patterntools.Pseq(
                        (10, 20, 30, 40),
                        repetitions=1,
                        ),
                    ),
                )
            )

    ::

        >>> for x in ppar:
        ...     x
        ...
        NoteEvent(delta=0.0, duration=1.0, uuid=UUID('...'), x=1)
        NoteEvent(delta=0.4, duration=0.4, uuid=UUID('...'), x=10)
        NoteEvent(delta=0.4, duration=0.4, uuid=UUID('...'), x=20)
        NoteEvent(delta=0.2, duration=0.4, uuid=UUID('...'), x=30)
        NoteEvent(delta=0.2, duration=1.0, uuid=UUID('...'), x=2)
        NoteEvent(delta=0.8, duration=0.4, uuid=UUID('...'), x=40)
        NoteEvent(delta=1.0, duration=1.0, uuid=UUID('...'), x=3)
        NoteEvent(duration=1.0, uuid=UUID('...'), x=4)

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_patterns',
        )

    ### INITIALIZER ###

    def __init__(self, patterns):
        from supriya.tools import patterntools
        assert all(isinstance(_, patterntools.EventPattern) for _ in patterns)
        assert patterns
        self._patterns = tuple(patterns)

    ### PRIVATE METHODS ###

    def _coerce_iterator_output(self, event, state):
        return new(event, _iterator=None)

    def _iterate(self, state=None):
        queue = state[0]
        # get first event
        previous_offset, previous_event, next_event = 0.0, None, None
        while not previous_event and not queue.empty():
            (_, index), iterator = queue.get()
            try:
                previous_event = next(iterator)
                previous_event = new(previous_event, _iterator=iterator)
            except StopIteration:
                continue
            queue.put(((previous_event.delta, index), iterator))
            break
        while not queue.empty():
            (next_offset, index), iterator = queue.get()
            try:
                next_event = next(iterator)
                next_event = new(next_event, _iterator=iterator)
            except StopIteration:
                continue
            queue.put(((next_offset + next_event.delta, index), iterator))
            delta = next_offset - previous_offset
            previous_event = new(previous_event, delta=delta)
            yield previous_event
            previous_event = next_event
            previous_offset = next_offset
            next_event = None
        if not next_event:
            yield previous_event

    def _setup_state(self):
        queue = PriorityQueue()
        for index, pattern in enumerate(self._patterns, 1):
            iterator = iter(pattern)
            payload = ((0.0, index), iterator)
            queue.put(payload)
        state = (queue,)
        return state

    ### PUBLIC PROPERTIES ###

    @property
    def arity(self):
        return max(self._get_arity(_) for _ in self._patterns)

    @property
    def is_infinite(self):
        return all(_.is_infinite for _ in self._patterns)

    @property
    def patterns(self):
        return self._patterns
