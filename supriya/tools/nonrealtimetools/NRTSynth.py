# -*- encoding: utf-8 -*-
from supriya.tools import servertools
from supriya.tools.nonrealtimetools.NRTNode import NRTNode


class NRTSynth(NRTNode):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_synthdef',
        '_synth_kwargs',
        )

    _valid_add_actions = (
        servertools.AddAction.ADD_AFTER,
        servertools.AddAction.ADD_BEFORE,
        )

    ### INITIALIZER ###

    def __init__(
        self,
        session,
        session_id,
        duration=None,
        synthdef=None,
        start_offset=None,
        **synth_kwargs
        ):
        NRTNode.__init__(
            self,
            session,
            session_id,
            duration=duration,
            start_offset=start_offset,
            )
        self._synthdef = synthdef
        self._synth_kwargs = synth_kwargs

    ### SPECIAL METHODS ###

    def __str__(self):
        return 'synth-{}'.format(self.session_id)

    ### PUBLIC PROPERTIES ###

    @property
    def synthdef(self):
        return self._synthdef
