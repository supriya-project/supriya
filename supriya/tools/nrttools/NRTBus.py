# -*- encoding: utf-8 -*-
from supriya.tools.nrttools.NRTSessionObject import NRTSessionObject


class NRTBus(NRTSessionObject):

    ### CLASS VARIABLES ###

    __slots__ = ()

    def __init__(self, nrt_session, nrt_id):
        NRTSessionObject.__init__(self, nrt_session, nrt_id)
