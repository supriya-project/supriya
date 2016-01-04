# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class SessionMoment(SupriyaValueObject):
    r'''An NRT session moment.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_session',
        '_timestep',
        )

    ### INITIALIZER ###

    def __init__(self, session, timestep):
        from supriya.tools import nrttools
        assert isinstance(session, nrttools.Session)
        timestep = float(timestep)
        assert 0 <= timestep
        self._session = session
        self._timestep = timestep

    ### SPECIAL METHODS ###

    def __enter__(self):
        self._session._session_moments.append(self)

    def __exit__(self, exc_type, exc_value, traceback):
        self._session._session_moments.pop()

    ### PUBLIC PROPERTIES ###

    @property
    def session(self):
        return self._session

    @property
    def timestep(self):
        return self._timestep
