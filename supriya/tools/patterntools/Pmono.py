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
        Event(duration=0.5, _do_not_release=True, uuid=UUID('...'), pitch=0)
        Event(duration=0.25, _do_not_release=True, uuid=UUID('...'), pitch=3)
        Event(duration=0.25, uuid=UUID('...'), pitch=7)

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
        Event(duration=1, _do_not_release=True, uuid=UUID('...'), pitch=1)
        Event(duration=1, _do_not_release=True, uuid=UUID('...'), pitch=2)
        Event(duration=1, uuid=UUID('...'), pitch=3)
        Event(duration=1, _do_not_release=True, uuid=UUID('...'), pitch=4)
        Event(duration=1, _do_not_release=True, uuid=UUID('...'), pitch=5)
        Event(duration=1, uuid=UUID('...'), pitch=6)

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PRIVATE METHODS ###

    def _iterate(self):
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
