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

    def __repr__(self):
        return '<{} @{!r}>'.format(
            type(self).__name__,
            self.timestep,
            )

    ### PRIVATE METHODS ###

    def _clone(self, new_timestep):
        moment = type(self)(self.session, new_timestep)
        moment.nodes_to_children = self.nodes_to_children.copy()
        moment.nodes_to_parent = self.nodes_to_parent.copy()
        return moment

    def _free_node(self, node):
        pass

    def _process_actions(self, previous_moment=None):
        if previous_moment is None:
            previous_moment = self._find_moment_before(self.timestep)
        assert previous_moment is not None
        nodes_to_children = previous_moment.nodes_to_children.copy()
        nodes_to_parent = previous_moment.nodes_to_parent.copy()
        for action in self.actions:
            action.apply_transform(nodes_to_children, nodes_to_parent)
        for stop_node in stop_nodes:
            nonrealtimetools.NRTNodeAction.free_node(
                stop_node, nodes_to_children, nodes_to_parent)
        if nodes_to_childen != self.nodes_to_children:
            self.nodes_to_children = nodes_to_children
            self.nodes_to_parent = nodes_to_parent
            next_moment = self.session._find_moment_after(self.timestep)
            if next_moment is not None:
                next_moment._process_actions(previous_moment=self)

    def _register_action(self, source, target, action):
        from supriya.tools import nonrealtimetools
        assert target in self.nodes_to_children
        action = nonrealtimetools.NRTNodeAction(
            source=source,
            target=target,
            action=action,
            )
        self.actions.append(action)
