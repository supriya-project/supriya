# -*- encoding: utf-8 -*-
from supriya.tools import servertools
from supriya.tools.nonrealtimetools.NRTNode import NRTNode


class NRTSynth(NRTNode):

    _valid_add_actions = (
        servertools.AddAction.ADD_AFTER,
        servertools.AddAction.ADD_BEFORE,
        )

    def __init__(
        self,
        session,
        session_id,
        duration=None,
        start_offset=None,
        ):
        NRTNode.__init__(self, session, session_id)
        self.duration = duration
        self.start_offset = start_offset

    @property
    def stop_offset(self):
        return self.start_offset + self.duration
