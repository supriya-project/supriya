# -*- encoding: utf-8 -*-
import uuid
from supriya.tools.patterntools.Pbind import Pbind


class Pmono(Pbind):
    '''
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
        NoteEvent(duration=0.5, uuid=UUID('...'), _do_not_release=True, pitch=0)
        NoteEvent(duration=0.25, uuid=UUID('...'), _do_not_release=True, pitch=3)
        NoteEvent(duration=0.25, uuid=UUID('...'), pitch=7)

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
        NoteEvent(uuid=UUID('...'), _do_not_release=True, pitch=1)
        NoteEvent(uuid=UUID('...'), _do_not_release=True, pitch=2)
        NoteEvent(uuid=UUID('...'), pitch=3)
        NoteEvent(uuid=UUID('...'), _do_not_release=True, pitch=4)
        NoteEvent(uuid=UUID('...'), _do_not_release=True, pitch=5)
        NoteEvent(uuid=UUID('...'), pitch=6)

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PRIVATE METHODS ###

    def _iterate(self, state=None):
        patterns = self._coerce_pattern_pairs(self._patterns)
        synth_uuid = uuid.uuid4()
        generator = self._iterate_inner(patterns, synth_uuid)
        event_dicts = []
        try:
            first_event = next(generator)
            event_dicts.append(first_event)
        except StopIteration:
            return
        for event_dict in generator:
            event_dicts.append(event_dict)
            event_dicts[0]['_do_not_release'] = True
            yield event_dicts.pop(0)
        if event_dicts:
            yield event_dicts[0]

    def _iterate_inner(self, patterns, uuid):
        while True:
            event = {'uuid': uuid}
            for name, pattern in patterns.items():
                try:
                    event[name] = next(pattern)
                except StopIteration:
                    return
            yield event
