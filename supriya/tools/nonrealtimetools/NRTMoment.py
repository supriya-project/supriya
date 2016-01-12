# -*- encoding: utf-8 -*-


class NRTMoment(object):

    def __init__(self, session, timestep):
        self.dirty = False
        self.actions = []
        self.nodes_to_children = {}
        self.nodes_to_parent = {}
        self.session = session
        self.timestep = timestep

    def __enter__(self):
        previous_moment = None
        if self.session.active_moments:
            previous_moment = self.session.active_moments[-1]
        self.session.active_moments.append(self)
        if previous_moment:
            previous_moment._refresh()

    def __eq__(self, expr):
        if not isinstance(expr, type(self)):
            return False
        if expr.session is not self.session:
            return False
        return expr.timestep == self.timestep

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.active_moments.pop()
        self._refresh()

    def __lt__(self, expr):
        if not isinstance(expr, type(self)) or expr.session is not self.session:
            raise ValueError(expr)
        return self.timestep < expr.timestep

    def _refresh(self):
        if not self.dirty:
            pass
        self.dirty = False

    def _register_action(self, source, target, action):
        from supriya.tools import nonrealtimetools
        action = nonrealtimetools.NRTNodeAction(
            source=source, target=target, action=action)
        self.actions.append(action)
