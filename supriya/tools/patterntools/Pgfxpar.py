# -*- encoding: utf-8 -*-
import uuid
from supriya.tools.patterntools.Pgpar import Pgpar


class Pgfxpar(Pgpar):
    """
    A parallel stream player, which places settings in groups and follows each
    group with an identical FX synth.

    Note: This is a naive fix until I can correct how nested Ppars handle stop
    events.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_pattern_groups',
        '_release_time',
        '_settings',
        '_synthdef',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        patterns,
        synthdef,
        release_time=0.25,
        **settings
        ):
        from supriya.tools import synthdeftools
        Pgpar.__init__(self, patterns=patterns, release_time=release_time)
        assert isinstance(synthdef, synthdeftools.SynthDef)
        self._synthdef = synthdef
        self._settings = tuple(sorted(settings.items()))

    ### PRIVATE METHODS ###

    def _setup_peripherals(self, initial_expr, state):
        from supriya.tools import patterntools
        group_uuids = state.get('group_uuids')
        peripheral_starts, peripheral_stops = [], []
        delta = self._release_time or 0
        if delta:
            peripheral_stops.append(patterntools.NullEvent(delta=delta))
        for group_uuid in group_uuids:
            start_group_event = patterntools.GroupEvent(
                uuid=group_uuid,
                add_action='ADD_TO_TAIL',
                )
            stop_group_event = patterntools.GroupEvent(
                uuid=group_uuid,
                is_stop=True,
                )
            synth_uuid = uuid.uuid4()
            start_synth_event = patterntools.SynthEvent(
                add_action='ADD_AFTER',
                synthdef=self.synthdef,
                target_node=group_uuid,
                uuid=synth_uuid,
                **self.settings
                )
            stop_synth_event = patterntools.SynthEvent(
                uuid=synth_uuid,
                is_stop=True,
                )
            peripheral_starts.extend([start_group_event, start_synth_event])
            peripheral_stops.extend([stop_synth_event, stop_group_event])
        return peripheral_starts, peripheral_stops

    ### PUBLIC PROPERTIES ###

    @property
    def release_time(self):
        return self._release_time

    @property
    def synthdef(self):
        return self._synthdef

    @property
    def settings(self):
        return dict(self._settings)
