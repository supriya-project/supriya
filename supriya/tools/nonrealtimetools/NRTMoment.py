# -*- encoding: utf-8 -*-


class NRTMoment(object):

    ### INITIALIZER ###

    def __init__(self, session, timestep):
        self.actions = []
        self.nodes_to_children = {}
        self.nodes_to_parent = {}
        self.start_nodes = set()
        self.stop_nodes = set()
        self.session = session
        self.timestep = timestep

    ### SPECIAL METHODS ###

    def __enter__(self):
        self.session.active_moments.append(self)
        return self

    def __eq__(self, expr):
        if not isinstance(expr, type(self)):
            return False
        if expr.session is not self.session:
            return False
        return expr.timestep == self.timestep

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.active_moments.pop()

    def __lt__(self, expr):
        if not isinstance(expr, type(self)) or expr.session is not self.session:
            raise ValueError(expr)
        return self.timestep < expr.timestep

    ### PRIVATE METHODS ###

    def _clone(self, new_timestep):
        moment = type(self)(self.session, new_timestep)
        moment.nodes_to_children = self.nodes_to_children.copy()
        moment.nodes_to_parent = self.nodes_to_parent.copy()
        return moment

    def _process_actions(self):
        pass

    def _register_action(self, source, target, action):
        from supriya.tools import nonrealtimetools
        assert target in self.nodes_to_children
        action = nonrealtimetools.NRTNodeAction(
            source=source,
            target=target,
            action=action,
            )
        self.actions.append(action)
