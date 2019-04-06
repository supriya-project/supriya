import uuid

from uqbar.objects import new

from supriya.patterns.Pbind import Pbind


class Pmono(Pbind):
    """
    A monophonic pattern.

    ::

        >>> pattern = supriya.patterns.Pmono(
        ...     pitch=supriya.patterns.Pseq([0, 3, 7]),
        ...     duration=supriya.patterns.Pseq([0.5, 0.25, 0.25]),
        ...     )

    ::

        >>> for event in pattern:
        ...     event
        ...
        NoteEvent(
            delta=0.5,
            duration=0.5,
            is_stop=False,
            pitch=0,
            uuid=UUID('...'),
            )
        NoteEvent(
            delta=0.25,
            duration=0.25,
            is_stop=False,
            pitch=3,
            uuid=UUID('...'),
            )
        NoteEvent(
            delta=0.25,
            duration=0.25,
            pitch=7,
            uuid=UUID('...'),
            )

    ::

        >>> pattern = supriya.patterns.Pseq([
        ...     supriya.patterns.Pmono(
        ...         pitch=supriya.patterns.Pseq([1, 2, 3], 1),
        ...         ),
        ...     supriya.patterns.Pmono(
        ...         pitch=supriya.patterns.Pseq([4, 5, 6], 1),
        ...         ),
        ...     ], 1)

    ::

        >>> for event in pattern:
        ...     event
        ...
        NoteEvent(
            is_stop=False,
            pitch=1,
            uuid=UUID('...'),
            )
        NoteEvent(
            is_stop=False,
            pitch=2,
            uuid=UUID('...'),
            )
        NoteEvent(
            pitch=3,
            uuid=UUID('...'),
            )
        NoteEvent(
            is_stop=False,
            pitch=4,
            uuid=UUID('...'),
            )
        NoteEvent(
            is_stop=False,
            pitch=5,
            uuid=UUID('...'),
            )
        NoteEvent(
            pitch=6,
            uuid=UUID('...'),
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PRIVATE METHODS ###

    def _iterate(self, state=None):
        synth_uuid = uuid.uuid4()
        iterator = super(Pmono, self)._iterate(state=state)
        events = []
        try:
            events.append(next(iterator))
        except StopIteration:
            return
        for event in iterator:
            events.append(event)
            event = new(events.pop(0), uuid=synth_uuid, is_stop=False)
            should_stop = yield event
            if should_stop:
                return
        assert len(events) == 1
        if events:
            event = events.pop()
            event = new(event, uuid=synth_uuid, is_stop=True)
            yield event
