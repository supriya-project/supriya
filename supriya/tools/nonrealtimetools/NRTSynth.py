# -*- encoding: utf-8 -*-
from supriya.tools import servertools
from supriya.tools.nonrealtimetools.NRTNode import NRTNode


class NRTSynth(NRTNode):

    ### CLASS VARIABLES ###

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
        ):
        NRTNode.__init__(self, session, session_id, start_offset=start_offset)
        self.duration = duration
        self.synthdef = synthdef

    ### SPECIAL METHODS ###

    def __str__(self):
        return 'synth-{}'.format(self.session_id)
