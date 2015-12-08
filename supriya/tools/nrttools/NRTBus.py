# -*- encoding: utf-8 -*-
from supriya.tools.nrttools.NRTSessionObject import NRTSessionObject


class NRTBus(NRTSessionObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_kind',
        )

    ### INITIALIZER ###

    def __init__(self, nrt_session, nrt_id, kind='control'):
        assert kind in ('control', 'audio')
        NRTSessionObject.__init__(self, nrt_session, nrt_id)
        self._kind = kind

    ### PUBLIC PROPERTIES ###

    @property
    def kind(self):
        return self._kind
