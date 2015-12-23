# -*- encoding: utf-8 -*-
from abjad.tools import timespantools
from supriya.tools import requesttools
from supriya.tools import servertools
from supriya.tools import synthdeftools


class Synth(timespantools.Timespan):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_synthdef',
        '_synth_kwargs',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        start_offset=None,
        stop_offset=None,
        synthdef=None,
        **synth_kwargs
        ):
        timespantools.Timespan.__init__(
            self,
            start_offset=start_offset,
            stop_offset=stop_offset,
            )
        assert isinstance(synthdef, synthdeftools.SynthDef)
        self._synthdef = synthdef
        self._synth_kwargs = synth_kwargs.copy()

    ### PUBLIC METHODS ###

    def get_start_request(self, mapping):
        node_id = mapping[self]
        target_node_id = 0
        parameter_names = self.synthdef.parameter_names
        synth_kwargs = self.synth_kwargs
        if 'duration' in parameter_names and 'duration' not in synth_kwargs:
            synth_kwargs['duration'] = float(self.duration)
        request = requesttools.SynthNewRequest(
            add_action=servertools.AddAction.ADD_TO_TAIL,
            node_id=node_id,
            synthdef=self.synthdef.anonymous_name,
            target_node_id=target_node_id,
            **synth_kwargs
            )
        return request

    ### PUBLIC PROPERTIES ###

    @property
    def synth_kwargs(self):
        return self._synth_kwargs.copy()

    @property
    def synthdef(self):
        return self._synthdef
