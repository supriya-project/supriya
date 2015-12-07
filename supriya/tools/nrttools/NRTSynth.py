# -*- encoding: utf-8 -*-
from supriya.tools.nrttools.NRTSessionObject import NRTSessionObject


class NRTSynth(NRTSessionObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_synthdef',
        )

    ### INITIALIZER ###

    def __init__(self, nrt_session, nrt_id, synthdef):
        NRTSessionObject.__init__(self, nrt_session, nrt_id)
        self._synthdef = synthdef

    ### PUBLIC PROPERTIES ###

    @property
    def synthdef(self):
        return self._synthdef
