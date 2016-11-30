# -*- encoding: utf-8 -*-
from supriya.tools.nonrealtimetools.SessionObject import SessionObject


class Moment(SessionObject):
    """
    A moment-in-time referencing a singleton non-realtime state.

    ::

        >>> session = nonrealtimetools.Session()
        >>> moment = session.at(10.5)

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Session Objects'

    __slots__ = (
        '_offset',
        '_propagate',
        '_session',
        '_state',
        )

    ### INITIALIZER ###

    def __init__(self, session, offset, state, propagate=True):
        SessionObject.__init__(self, session)
        self._offset = offset
        self._state = state
        self._propagate = bool(propagate)

    ### SPECIAL METHODS ###

    def __enter__(self):
        self.session.active_moments.append(self)
        if self.propagate:
            self.session._apply_transitions(self.state.offset)
        return self

    def __eq__(self, expr):
        if not isinstance(expr, type(self)):
            return False
        if expr.session is not self.session:
            return False
        return expr.offset == self.offset

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.active_moments.pop()
        if self.propagate:
            self.session._apply_transitions(self.state.offset)

    def __lt__(self, expr):
        if not isinstance(expr, type(self)) or expr.session is not self.session:
            raise ValueError(expr)
        return self.offset < expr.offset

    def __repr__(self):
        return '<{} @{!r}>'.format(
            type(self).__name__,
            self.offset,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def offset(self):
        return self._offset

    @property
    def propagate(self):
        return self._propagate

    @property
    def state(self):
        return self._state
