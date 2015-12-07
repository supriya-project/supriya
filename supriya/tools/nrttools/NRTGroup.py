# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.NRTSessionObject import NRTSessionObject


class NRTGroup(NRTSessionObject):

    ### CLASS VARIABLES ###

    __slots__ = ()

    def __init__(self, nrt_session, nrt_id):
        NRTSessionObject.__init__(self, nrt_session, nrt_id)
