# -*- encoding: utf-8 -*-


class NRTMoment(object):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_actions',
        '_nodes_to_children',
        '_nodes_to_parents',
        '_offset',
        '_session',
        '_start_nodes',
        '_stop_nodes',
        )

    ### INITIALIZER ###

    def __init__(self, session, offset):
        self._actions = []
        self._nodes_to_children = {}
        self._nodes_to_parents = {}
        self._start_nodes = set()
        self._stop_nodes = set()
        self._session = session
        self._offset = offset

    ### SPECIAL METHODS ###

    def __enter__(self):
        if self.session.active_moments:
            previous_moment = self.session.active_moments[-1]
            previous_moment._process_actions()
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
        self._process_actions()

    def __lt__(self, expr):
        if not isinstance(expr, type(self)) or expr.session is not self.session:
            raise ValueError(expr)
        return self.offset < expr.offset

    def __repr__(self):
        return '<{} @{!r}>'.format(
            type(self).__name__,
            self.offset,
            )

    ### PRIVATE METHODS ###

    def _clone(self, new_offset):
        moment = type(self)(self.session, new_offset)
        moment._nodes_to_children = self.nodes_to_children.copy()
        moment._nodes_to_parents = self.nodes_to_parents.copy()
        return moment

    def _free_node(self, node):
        pass

    def _process_actions(self, previous_moment=None):
        from supriya.tools import nonrealtimetools
        if previous_moment is None:
            previous_moment = self.session._find_moment_before(self.offset)
        assert previous_moment is not None
        nodes_to_children = previous_moment.nodes_to_children.copy()
        nodes_to_parents = previous_moment.nodes_to_parents.copy()
        for action in self.actions:
            action.apply_transform(nodes_to_children, nodes_to_parents)
        for stop_node in self.stop_nodes:
            nonrealtimetools.NRTNodeAction.free_node(
                stop_node, nodes_to_children, nodes_to_parents)
        if nodes_to_children != self.nodes_to_children:
            self._nodes_to_children = nodes_to_children
            self._nodes_to_parents = nodes_to_parents
            next_moment = self.session._find_moment_after(self.offset)
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

    ### PUBLIC METHODS ###

    def report(self):
        state = {}
        node_hierarchy = {}
        items = sorted(self.nodes_to_children.items(),
            key=lambda item: item[0].session_id)
        for parent, children in items:
            if not children:
                children = []
            node_hierarchy[str(parent)] = [str(child) for child in children]
        node_lifecycle = {}
        if self.start_nodes:
            node_lifecycle['start'] = sorted(str(node) for node in self.start_nodes)
        if self.stop_nodes:
            node_lifecycle['stop'] = sorted(str(node) for node in self.stop_nodes)
        if node_hierarchy:
            state['hierarchy'] = node_hierarchy
        if node_lifecycle:
            state['lifecycle'] = node_lifecycle
        state['offset'] = self.offset
        return state

    def to_requests(self, node_id_mapping, visited_synthdefs):
        from supriya.tools import requesttools
        requests = []
        synthdefs = [x for x in self.synthdefs if x not in visited_synthdefs]
        if synthdefs:
            request = requesttools.SynthDefReceiveRequest(synthdefs=synthdefs)
            requests.append(request)
        return requests

    ### PUBLIC PROPERTIES ###

    @property
    def actions(self):
        return self._actions

    @property
    def nodes_to_children(self):
        return self._nodes_to_children

    @property
    def nodes_to_parents(self):
        return self._nodes_to_parents

    @property
    def offset(self):
        return self._offset

    @property
    def session(self):
        return self._session

    @property
    def start_nodes(self):
        return self._start_nodes

    @property
    def stop_nodes(self):
        return self._stop_nodes

    @property
    def synthdefs(self):
        from supriya.tools import nonrealtimetools
        synthdefs = set()
        for node in self.start_nodes:
            if not isinstance(node, nonrealtimetools.NRTSynth):
                continue
            synthdefs.add(node.synthdef)
        synthdefs = sorted(synthdefs, key=lambda x: x.anonymous_name)
        return synthdefs
