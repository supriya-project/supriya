# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class NRTTimeSlice(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_nrt_session',
        '_timestep',
        )        

    ### INITIALIZER ###

    def __init__(self, nrt_session, timestep):
        self._nrt_session = nrt_session
        self._timestep = timestep

    ### PUBLIC PROPERTIES ###

    @property
    def nrt_session(self):
        return self._nrt_session

    @property
    def timestep(self):
        return self._timestep
