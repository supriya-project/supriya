# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class SessionMoment(SupriyaValueObject):
    r'''An NRT session moment.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_session',
        '_offset',
        )

    ### INITIALIZER ###

    def __init__(self, session, offset):
        from supriya.tools import nonrealtimetools
        assert isinstance(session, nonrealtimetools.Session)
        offset = float(offset)
        assert 0 <= offset
        self._session = session
        self._offset = offset

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
    def offset(self):
        return self._offset
