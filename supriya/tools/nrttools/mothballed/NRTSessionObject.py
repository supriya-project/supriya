# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class NRTSessionObject(SupriyaValueObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_nrt_id',
        '_nrt_session',
        )

    ### INITIALIZER ###

    def __init__(self, nrt_session, nrt_id):
        self._nrt_session = nrt_session
        self._nrt_id = nrt_id

    ### PUBLIC PROPERTIES ###

    @property
    def nrt_id(self):
        return self._nrt_id

    @property
    def nrt_session(self):
        return self._nrt_session
