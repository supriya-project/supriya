# -*- encoding: utf-8 -*-
import collections
from supriya.tools import requesttools
from supriya.tools import servertools
from supriya.tools.nonrealtimetools.SessionObject import SessionObject


class Moment(SessionObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_actions',
        '_is_instantaneous',
        '_nodes_to_children',
        '_nodes_to_parents',
        '_offset',
        '_session',
        '_start_nodes',
        '_stop_nodes',
        )

    ### INITIALIZER ###

    def __init__(self, session, offset, is_instantaneous=False):
        SessionObject.__init__(self, session)
        self._actions = collections.OrderedDict()
        self._nodes_to_children = {}
        self._nodes_to_parents = {}
        self._start_nodes = set()
        self._stop_nodes = set()
        self._offset = offset
        self._is_instantaneous = bool(is_instantaneous)

    ### SPECIAL METHODS ###

    def __enter__(self):
        if self.session.active_moments:
            previous_moment = self.session.active_moments[-1]
            previous_moment._propagate_action_transforms()
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
        self._propagate_action_transforms()

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

    def _clone(self, new_offset, is_instantaneous=False):
        moment = type(self)(
            self.session,
            new_offset,
            is_instantaneous=is_instantaneous,
            )
        if new_offset == self.offset:
            moment.start_nodes.update(self.start_nodes)
            moment.stop_nodes.update(self.stop_nodes)
        moment._nodes_to_children = self.nodes_to_children.copy()
        moment._nodes_to_parents = self.nodes_to_parents.copy()
        return moment

    def _collect_bus_requests(self, bus_settings):
        requests = []
        if self.offset in bus_settings:
            index_value_pairs = sorted(bus_settings[self.offset].items())
            request = requesttools.ControlBusSetRequest(
                index_value_pairs=index_value_pairs,
                )
            requests.append(request)
        return requests

    def _collect_node_action_requests(self, id_mapping, node_settings, start_nodes, node_actions):
        from supriya.tools import nonrealtimetools
        requests = []
        for source, action in node_actions.items():
            if source in start_nodes:
                if isinstance(source, nonrealtimetools.Synth):
                    synth_kwargs = {} 
                    if source in node_settings:
                        synth_kwargs.update(node_settings.pop(source))
                    if 'duration' in source.synthdef.parameter_names:
                        # need to propagate in session rendering timespan
                        # as many nodes have "infinite" duration
                        synth_kwargs['duration'] = float(source.duration)
                    request = source.to_request(action, id_mapping, **synth_kwargs)
                else:
                    request = source.to_request(action, id_mapping)
            else:
                request = action.to_request(id_mapping)
            requests.append(request)
        return requests

    def _collect_node_set_requests(self, id_mapping, node_settings):
        from supriya.tools import nonrealtimetools
        requests = []
        bus_prototype = (
            nonrealtimetools.Bus,
            nonrealtimetools.BusGroup,
            type(None),
            )
        for node, settings in node_settings.items():
            node_id = id_mapping[node]
            a_settings = {}
            c_settings = {}
            n_settings = {}
            for key, value in settings.items():
                if isinstance(value, bus_prototype):
                    if value is None:
                        c_settings[key] = -1
                    elif value.calculation_rate == servertools.CalculationRate.CONTROL:
                        c_settings[key] = id_mapping[value]
                    else:
                        a_settings[key] = id_mapping[value]
                else:
                    n_settings[key] = value
                if n_settings:
                    request = requesttools.NodeSetRequest(
                        node_id=node_id,
                        **n_settings
                        )
                    requests.append(request)
                if a_settings:
                    request = requesttools.NodeMapToAudioBusRequest(
                        node_id=node_id,
                        **a_settings
                        )
                    requests.append(request)
                if c_settings:
                    request = requesttools.NodeMapToControlBusRequest(
                        node_id=node_id,
                        **c_settings
                        )
                    requests.append(request)
            # separate out floats, control buses and audio buses
        return requests

    def _collect_nodes(self, force_start, force_stop):
        start_nodes = self.start_nodes
        stop_nodes = self.stop_nodes
        if force_start or force_stop:
            nonroot_nodes = set(
                node for node in self._iterate_nodes(
                    self.session.root_node,
                    self.nodes_to_children,
                    )
                if node is not self.session.root_node
                )
            if force_start:
                start_nodes.update(nonroot_nodes)
            if force_stop:
                stop_nodes.update(nonroot_nodes)
        return start_nodes, stop_nodes

    def _collect_node_actions(self, force_start, start_nodes):
        from supriya.tools import nonrealtimetools
        if force_start:
            node_actions = collections.OrderedDict()
            for parent, child in self._iterate_node_pairs(
                self.session.root_node,
                self.nodes_to_children,
                ):
                action = nonrealtimetools.NodeAction(
                    source=child,
                    target=parent,
                    action=servertools.AddAction.ADD_TO_TAIL,
                    )
                node_actions[child] = action
        else:
            node_actions = self.actions
        return node_actions

    def _collect_node_settings(self, force_start=None):
        result = collections.OrderedDict()
        for node in self._iterate_nodes(
            self.session.root_node,
            self.nodes_to_children,
            ):
            settings = node._collect_settings(
                self.offset,
                persistent=force_start,
                )
            if settings:
                result[node] = settings
        return result

    def _collect_node_stop_requests(self, id_mapping, stop_nodes):
        requests = []
        if stop_nodes:
            free_ids, gate_ids = [], []
            for node in stop_nodes:
                node_id = id_mapping[node]
                if hasattr(node, 'synthdef') and \
                    'gate' in node.synthdef.parameter_names:
                    gate_ids.append(node_id)
                else:
                    free_ids.append(node_id)
            free_ids.sort()
            gate_ids.sort()
            if free_ids:
                request = requesttools.NodeFreeRequest(node_ids=free_ids)
                requests.append(request)
            if gate_ids:
                for node_id in gate_ids:
                    request = requesttools.NodeSetRequest(
                        node_id=node_id,
                        gate=0,
                        )
                    requests.append(request)
        return requests

    def _collect_synthdef_requests(self, visited_synthdefs, start_nodes):
        from supriya.tools import nonrealtimetools
        requests = []
        synthdefs = set()
        for node in start_nodes:
            if not isinstance(node, nonrealtimetools.Synth):
                continue
            elif node.synthdef in visited_synthdefs:
                continue
            synthdefs.add(node.synthdef)
            visited_synthdefs.add(node.synthdef)
        synthdefs = sorted(synthdefs, key=lambda x: x.anonymous_name)
        if synthdefs:
            request = requesttools.SynthDefReceiveRequest(synthdefs=synthdefs)
            requests.append(request)
        return requests

    @classmethod
    def _iterate_nodes(cls, root_node, nodes_to_children):
        def recurse(parent):
            yield parent
            children = nodes_to_children.get(parent, ()) or ()
            for child in children:
                for node in recurse(child):
                    yield node
        return recurse(root_node)

    @classmethod
    def _iterate_node_pairs(cls, root_node, nodes_to_children):
        def recurse(parent):
            children = nodes_to_children.get(parent, ()) or ()
            for child in children:
                yield parent, child 
                for pair in recurse(child):
                    yield pair
        return recurse(root_node)

    def _propagate_action_transforms(self, previous_moment=None):
        from supriya.tools import nonrealtimetools
        if previous_moment is None:
            previous_moment = self.session._find_moment_before(self.offset)
        assert previous_moment is not None
        nodes_to_children = previous_moment.nodes_to_children.copy()
        nodes_to_parents = previous_moment.nodes_to_parents.copy()
        for _, action in self.actions.items():
            action.apply_transform(nodes_to_children, nodes_to_parents)
        for stop_node in self.stop_nodes:
            nonrealtimetools.NodeAction.free_node(
                stop_node, nodes_to_children, nodes_to_parents)
        if nodes_to_children != self.nodes_to_children:
            self._nodes_to_children = nodes_to_children
            self._nodes_to_parents = nodes_to_parents
            next_moment = self.session._find_moment_after(self.offset)
            if next_moment is not None:
                next_moment._propagate_action_transforms(previous_moment=self)

    def _register_action(self, source, target, action):
        from supriya.tools import nonrealtimetools
        assert target in self.nodes_to_children
        action = nonrealtimetools.NodeAction(
            source=source,
            target=target,
            action=action,
            )
        self.actions[source] = action

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

    def to_requests(
        self,
        id_mapping,
        bus_settings=None,
        force_start=None,
        force_stop=None,
        visited_synthdefs=None,
        ):
        requests = []
        bus_settings = bus_settings or {}
        visited_synthdefs = visited_synthdefs or set()
        start_nodes, stop_nodes = self._collect_nodes(force_start, force_stop)
        node_actions = self._collect_node_actions(force_start, start_nodes)
        print('        Start:', start_nodes)
        print('         Stop:', stop_nodes)
        node_settings = self._collect_node_settings(force_start)
        requests += self._collect_synthdef_requests(visited_synthdefs, start_nodes)
        requests += self._collect_node_action_requests(id_mapping, node_settings, start_nodes, node_actions)
        requests += self._collect_node_set_requests(id_mapping, node_settings)
        requests += self._collect_bus_requests(bus_settings)
        requests += self._collect_node_stop_requests(id_mapping, stop_nodes)
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
