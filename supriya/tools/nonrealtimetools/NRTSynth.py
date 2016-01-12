# -*- encoding: utf-8 -*-
from supriya.tools import servertools
from supriya.tools.nonrealtimetools.NRTNode import NRTNode


class NRTSynth(NRTNode):

    _valid_add_actions = (
        servertools.AddAction.ADD_AFTER,
        servertools.AddAction.ADD_BEFORE,
        )

    def __init__(self, session, duration, session_id):
        NRTNode.__init__(self, session, session_id)
        self.duration = duration
