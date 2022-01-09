import collections
import threading
from typing import Dict, List, Tuple

import uqbar.graphs

import supriya.commands
from supriya.nonrealtime.bases import SessionObject
from supriya.system import SupriyaValueObject
from supriya.utils import iterate_nwise

_local = threading.local()
_local._do_not_propagate_stack = []


class State(SessionObject):
    """
    A non-realtime state.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_transitions",
        "_nodes_to_children",
        "_nodes_to_parents",
        "_offset",
        "_session",
        "_start_buffers",
        "_start_nodes",
        "_stop_buffers",
        "_stop_nodes",
    )

    _ordered_buffer_request_types = (supriya.commands.BufferZeroRequest,)

    ### INITIALIZER ###

    def __init__(self, session, offset):
        from supriya.nonrealtime import Node

        SessionObject.__init__(self, session)
        self._transitions = collections.OrderedDict()
        self._nodes_to_children: Dict[Node, Tuple[Node]] = {}
        self._nodes_to_parents: Dict[Node, Tuple[Node]] = {}
        self._start_nodes = set()
        self._stop_nodes = set()
        self._start_buffers = set()
        self._stop_buffers = set()
        self._offset = offset

    ### SPECIAL METHODS ###

    def __repr__(self):
        return "<{} @{!r}>".format(type(self).__name__, self.offset)

    ### PRIVATE METHODS ###

    @classmethod
    def _apply_transitions(
        cls,
        transitions=None,
        nodes_to_children=None,
        nodes_to_parents=None,
        stop_nodes=None,
    ):
        import supriya.nonrealtime

        if nodes_to_children is not None:
            nodes_to_children = nodes_to_children.copy()
        else:
            nodes_to_children = {}
        if nodes_to_parents is not None:
            nodes_to_parents = nodes_to_parents.copy()
        else:
            nodes_to_parents = {}
        transitions = transitions or {}
        for node, action in transitions.items():
            action.apply_transform(nodes_to_children, nodes_to_parents)
        stop_nodes = stop_nodes or ()
        for stop_node in stop_nodes:
            supriya.nonrealtime.NodeTransition.free_node(
                stop_node, nodes_to_children, nodes_to_parents
            )
        return nodes_to_children, nodes_to_parents

    def _as_graphviz_graph(self):
        from .nodes import Synth

        ordered_synths = []
        cluster = uqbar.graphs.Graph(
            is_cluster=True,
            # attributes={'rank': 'same'},
        )
        node_mapping = {self.session.root_node: cluster}
        for parent, child in self._iterate_node_pairs(
            self.session.root_node, self._nodes_to_children
        ):
            if isinstance(child, Synth) and child not in ordered_synths:
                child_node = child._as_graphviz_node(self.offset)
                ordered_synths.append(child_node)
            else:
                child_node = uqbar.graphs.Graph(
                    is_cluster=True,
                    attributes={
                        "label": child.session_id,
                        "style": ["dashed", "rounded"],
                    },
                )
            node_mapping[child] = child_node
            parent_node = node_mapping[parent]
            parent_node.append(child_node)
        for synth_a, synth_b in iterate_nwise(ordered_synths):
            synth_a.attach(synth_b)
        return cluster, node_mapping, ordered_synths

    def _clone(self, new_offset):
        if float("-inf") < self.offset:
            self.session._apply_transitions(self.offset, chain=False)
        state = type(self)(self.session, new_offset)
        state._nodes_to_children = self.nodes_to_children.copy()
        state._nodes_to_parents = self.nodes_to_parents.copy()
        if new_offset == self.offset:
            state._transitions = self._transitions.copy()
            state._start_buffers.update(self.start_buffers)
            state._stop_buffers.update(self.stop_buffers)
            state._start_nodes.update(self.start_nodes)
            state._stop_nodes.update(self.stop_nodes)
        return state

    def _desparsify(self):
        if self._nodes_to_children is not None:
            return
        previous_state = self.session._find_state_before(
            self.offset, with_node_tree=True
        )
        self._nodes_to_children = previous_state.nodes_to_children.copy()
        self._nodes_to_parents = previous_state.nodes_to_parents.copy()

    def _sparsify(self):
        if self.is_sparse:
            self.session._remove_state_at(self.offset)

    @classmethod
    def _find_first_inconsistency(
        cls, root_node, nodes_to_children_one, nodes_to_children_two, stop_nodes
    ):
        import supriya.nonrealtime

        for parent in cls._iterate_nodes(root_node, nodes_to_children_one):
            if parent in stop_nodes:
                continue
            children_one = nodes_to_children_one.get(parent) or ()
            children_one = [node for node in children_one if node not in stop_nodes]
            children_two = nodes_to_children_two.get(parent) or ()
            if children_one == children_two or not children_two:
                continue
            for i, child in enumerate(children_two):
                if not children_one:
                    action = "ADD_TO_HEAD"
                    target = parent
                elif len(children_one) <= i:
                    action = "ADD_AFTER"
                    target = children_one[i - 1]
                elif children_one[i] is not child:
                    action = "ADD_BEFORE"
                    target = children_one[i]
                else:
                    continue
                transition = supriya.nonrealtime.NodeTransition(
                    source=child, target=target, action=action
                )
                return transition

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

    @classmethod
    def _rebuild_transitions(cls, state_one, state_two):
        # print('REBUILDING')
        assert state_one.session.root_node is state_two.session.root_node
        a_children = state_one.nodes_to_children.copy()
        a_parents = state_one.nodes_to_parents.copy()
        b_children, b_parents = a_children.copy(), a_parents.copy()
        stop_nodes = state_two.stop_nodes
        transitions = collections.OrderedDict()
        counter = 0
        while b_children != state_two.nodes_to_children:
            # print('ROUND', counter)
            # print('C-1', b_children)
            # print('C-2', state_two.nodes_to_children)
            transition = State._find_first_inconsistency(
                state_one.session.root_node,
                b_children,
                state_two.nodes_to_children,
                stop_nodes,
            )
            if transition is not None:
                transitions[transition.source] = transition
            b_children, b_parents = State._apply_transitions(
                transitions, a_children, a_parents, stop_nodes
            )
            counter += 1
            if counter == 100:
                raise Exception
        return transitions

    ### PUBLIC METHODS ###

    def report(self):
        state = {}
        node_hierarchy = {}
        items = sorted(
            self.nodes_to_children.items(), key=lambda item: item[0].session_id
        )
        for parent, children in items:
            if not children:
                children = []
            node_hierarchy[str(parent)] = [str(child) for child in children]
        node_lifecycle = {}
        if self.start_nodes:
            node_lifecycle["start"] = sorted(str(node) for node in self.start_nodes)
        if self.stop_nodes:
            node_lifecycle["stop"] = sorted(str(node) for node in self.stop_nodes)
        if node_hierarchy:
            state["hierarchy"] = node_hierarchy
        if node_lifecycle:
            state["lifecycle"] = node_lifecycle
        state["offset"] = self.offset
        return state

    ### PUBLIC PROPERTIES ###

    @property
    def is_sparse(self):
        if self.start_nodes:
            return False
        elif self.stop_nodes:
            return False
        elif self.transitions:
            return False
        return True

    @property
    def nodes_to_children(
        self,
    ) -> Dict["supriya.nonrealtime.Node", Tuple["supriya.nonrealtime.Node"]]:
        return self._nodes_to_children

    @property
    def nodes_to_parents(
        self,
    ) -> Dict["supriya.nonrealtime.Node", Tuple["supriya.nonrealtime.Node"]]:
        return self._nodes_to_parents

    @property
    def offset(self) -> float:
        return self._offset

    @property
    def start_buffers(self):
        return self._start_buffers

    @property
    def start_nodes(self):
        return self._start_nodes

    @property
    def stop_buffers(self):
        return self._stop_buffers

    @property
    def stop_nodes(self):
        return self._stop_nodes

    @property
    def overlap_nodes(self):
        interval_tree = self.session._nodes
        intersection = interval_tree.find_intersection(self.offset)
        overlap = [_ for _ in intersection if _.start_offset < self.offset]
        return overlap

    @property
    def overlap_buffers(self):
        interval_tree = self.session._buffers
        intersection = interval_tree.find_intersection(self.offset)
        overlap = [_ for _ in intersection if _.start_offset < self.offset]
        return overlap

    @property
    def transitions(self):
        return self._transitions


class Moment(SessionObject):
    """
    A moment-in-time referencing a singleton non-realtime state.

    ::

        >>> import supriya.nonrealtime
        >>> session = supriya.nonrealtime.Session()
        >>> moment = session.at(10.5)

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_offset", "_propagate", "_session", "_state")

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
        return "<{} @{!r}>".format(type(self).__name__, self.offset)

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


class NodeTransition(SupriyaValueObject):
    """
    A non-realtime state transition.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_source", "_target", "_action")

    ### INITIALIZER ###

    def __init__(self, source=None, action=None, target=None):
        if action is not None:
            action = supriya.AddAction.from_expr(action)
            assert isinstance(action, supriya.AddAction)
            assert source is not target
        if action is None:
            assert source is not None
            assert target is None
        self._action = action
        self._source = source
        self._target = target

    ### PRIVATE METHODS ###

    def _free_node(self, nodes_to_children, nodes_to_parents):
        node = self.source
        for child in nodes_to_children.get(node, ()) or ():
            self.free_node(child, nodes_to_children, nodes_to_parents)
        parent = nodes_to_parents.get(node, None)
        if node in nodes_to_children:
            del nodes_to_children[node]
        if node in nodes_to_parents:
            del nodes_to_parents[node]
        if not parent:
            return
        children = list(nodes_to_children[parent])
        children.remove(node)
        nodes_to_children[parent] = tuple(children) or None

    def _move_node(self, nodes_to_children, nodes_to_parents):
        assert self.target in nodes_to_children
        if self.source not in nodes_to_children:
            nodes_to_children[self.source] = None
        old_parent = nodes_to_parents.get(self.source, None)
        if old_parent:
            children = list(nodes_to_children[old_parent])
            children.remove(self.source)
            nodes_to_children[old_parent] = tuple(children) or None
        if self.action in (supriya.AddAction.ADD_AFTER, supriya.AddAction.ADD_BEFORE):
            new_parent = nodes_to_parents[self.target]
        else:
            new_parent = self.target
        nodes_to_parents[self.source] = new_parent
        children = list(nodes_to_children.get(new_parent, None) or ())
        if self.action == supriya.AddAction.ADD_TO_HEAD:
            children.insert(0, self.source)
        elif self.action == supriya.AddAction.ADD_TO_TAIL:
            children.append(self.source)
        elif self.action == supriya.AddAction.ADD_BEFORE:
            index = children.index(self.target)
            children.insert(index, self.source)
        elif self.action == supriya.AddAction.ADD_AFTER:
            index = children.index(self.target) + 1
            children.insert(index, self.source)
        nodes_to_children[new_parent] = tuple(children) or None

    def _to_request(self, id_mapping):
        node_id_pair = (id_mapping[self.source], id_mapping[self.target])
        if self.action == supriya.AddAction.ADD_TO_HEAD:
            request_class = supriya.commands.GroupHeadRequest
        elif self.action == supriya.AddAction.ADD_TO_TAIL:
            request_class = supriya.commands.GroupTailRequest
        elif self.action == supriya.AddAction.ADD_BEFORE:
            request_class = supriya.commands.NodeBeforeRequest
        elif self.action == supriya.AddAction.ADD_AFTER:
            request_class = supriya.commands.NodeAfterRequest
        request = request_class(node_id_pairs=[node_id_pair])
        return request

    ### PUBLIC METHODS ###

    def apply_transform(self, nodes_to_children, nodes_to_parents):
        if self.action is None:
            self._free_node(nodes_to_children, nodes_to_parents)
        else:
            self._move_node(nodes_to_children, nodes_to_parents)

    @classmethod
    def free_node(cls, node, nodes_to_children, nodes_to_parents):
        action = cls(source=node)
        action.apply_transform(nodes_to_children, nodes_to_parents)

    ### PUBLIC PROPERTIES ###

    @property
    def action(self):
        return self._action

    @property
    def source(self):
        return self._source

    @property
    def target(self):
        return self._target


class DoNotPropagate:
    """
    Context manager which prevents propagation of node hierarchy changes across
    states.
    """

    ### CLASS VARIABLES ###

    _stack: List["DoNotPropagate"] = _local._do_not_propagate_stack

    ### SPECIAL METHODS ###

    def __enter__(self):
        self._stack.append(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._stack.pop()
