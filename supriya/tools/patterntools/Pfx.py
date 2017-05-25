# -*- encoding: utf-8 -*-
import uuid
from supriya.tools.patterntools.EventPattern import EventPattern


class Pfx(EventPattern):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_pattern',
        '_release_time',
        '_settings',
        '_synthdef',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pattern,
        synthdef,
        release_time=0.25,
        **settings
        ):
        from supriya.tools import synthdeftools
        self._pattern = pattern
        assert isinstance(synthdef, synthdeftools.SynthDef)
        self._synthdef = synthdef
        release_time = float(release_time)
        assert 0 <= release_time
        self._release_time = release_time
        self._settings = tuple(sorted(settings.items()))

    ### PRIVATE METHODS ###

    def _iterate(self, state=None):
        return iter(self.pattern)

    def _setup_peripherals(self, initial_expr, state):
        from supriya.tools import patterntools
        start_synth_event = patterntools.SynthEvent(
            add_action='ADD_TO_TAIL',
            synthdef=self.synthdef,
            uuid=state['synth_uuid'],
            **self.settings
            )
        stop_synth_event = patterntools.SynthEvent(
            uuid=state['synth_uuid'],
            is_stop=True,
            )
        peripheral_starts = [start_synth_event]
        peripheral_stops = []
        delta = self._release_time or 0
        if delta:
            peripheral_stops.append(patterntools.NullEvent(delta=delta))
        peripheral_stops.append(stop_synth_event)
        return peripheral_starts, peripheral_stops

    def _setup_state(self):
        return {
            'synth_uuid': uuid.uuid4(),
            }

    ### PUBLIC PROPERTIES ###

    @property
    def arity(self):
        return self._pattern.arity

    @property
    def channel_count(self):
        return self._channel_count

    @property
    def is_infinite(self):
        return self._pattern.is_infinite

    @property
    def pattern(self):
        return self._pattern

    @property
    def release_time(self):
        return self._release_time

    @property
    def synthdef(self):
        return self._synthdef

    @property
    def settings(self):
        return dict(self._settings)
