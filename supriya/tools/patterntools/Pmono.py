import uuid
from supriya import utils
from supriya.tools.patterntools.Pbind import Pbind


class Pmono(Pbind):
    """
    A monophonic pattern.

    ::

        >>> pattern = patterntools.Pmono(
        ...     pitch=patterntools.Pseq([0, 3, 7]),
        ...     duration=patterntools.Pseq([0.5, 0.25, 0.25]),
        ...     )

    ::

        >>> for event in pattern:
        ...     event
        ...
        NoteEvent(delta=0.5, duration=0.5, uuid=UUID('...'), pitch=0)
        NoteEvent(delta=0.25, duration=0.25, uuid=UUID('...'), pitch=3)
        NoteEvent(delta=0.25, duration=0.25, is_stop=True, uuid=UUID('...'), pitch=7)

    ::

        >>> pattern = patterntools.Pseq([
        ...     patterntools.Pmono(
        ...         pitch=patterntools.Pseq([1, 2, 3], 1),
        ...         ),
        ...     patterntools.Pmono(
        ...         pitch=patterntools.Pseq([4, 5, 6], 1),
        ...         ),
        ...     ], 1)

    ::

        >>> for event in pattern:
        ...     event
        ...
        NoteEvent(uuid=UUID('...'), pitch=1)
        NoteEvent(uuid=UUID('...'), pitch=2)
        NoteEvent(is_stop=True, uuid=UUID('...'), pitch=3)
        NoteEvent(uuid=UUID('...'), pitch=4)
        NoteEvent(uuid=UUID('...'), pitch=5)
        NoteEvent(is_stop=True, uuid=UUID('...'), pitch=6)

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
            event = utils.new(events.pop(0), uuid=synth_uuid, is_stop=None)
            should_stop = yield event
            if should_stop:
                return
        assert len(events) == 1
        if events:
            event = events.pop()
            event = utils.new(event, uuid=synth_uuid, is_stop=True)
            yield event
