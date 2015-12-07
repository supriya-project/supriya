# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.NRTSessionObject import NRTSessionObject


class NRTSynth(NRTSessionObject):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, nrt_session, nrt_id):
        NRTSessionObject.__init__(self, nrt_session, nrt_id)
