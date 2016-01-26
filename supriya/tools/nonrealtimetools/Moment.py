# -*- encoding: utf-8 -*-
from supriya.tools.nonrealtimetools.SessionObject import SessionObject


class Moment(SessionObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_offset',
        '_session',
        '_state',
        )

    ### INITIALIZER ###

    def __init__(self, session, offset, state):
        SessionObject.__init__(self, session)
        self._offset = offset
        self._state = state

    ### SPECIAL METHODS ###

    def __enter__(self):
        if self.session.active_moments:
            previous_moment = self.session.active_moments[-1]
            previous_moment.state._propagate_action_transforms()
        self.session.active_moments.append(self)
        return self

    def __eq__(self, expr):
        if not isinstance(expr, type(self)):
            return False
        if expr.session is not self.session:
            return False
        return expr.offset == self.offset

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.active_moments.pop()
        self.state._propagate_action_transforms()

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
    def state(self):
        return self._state
