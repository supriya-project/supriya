import abc
import pathlib
import tempfile
from collections.abc import Sequence
from typing import Optional, Tuple, cast

import uqbar.graphs
import uqbar.strings
from uqbar.containers import UniqueTreeList, UniqueTreeNode
from uqbar.objects import new

import supriya
from supriya.enums import AddAction, NodeAction
from supriya.exceptions import ServerOffline

from ..synthdefs.synthdefs import SynthDef
from ..typing import AddActionLike
from .interfaces import GroupInterface, SynthInterface  # noqa


class Node(UniqueTreeNode):

    ### CLASS VARIABLES ###

    _valid_add_actions: Tuple[int, ...] = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, name=None, node_id_is_permanent=False):
        UniqueTreeNode.__init__(self, name=name)
        self._is_paused = False
        self._node_id = None
        self._node_id_is_permanent = bool(node_id_is_permanent)
        self._server = None

    ### SPECIAL METHODS ###

    def __float__(self):
        return float(self.node_id)

    def __graph__(self):
        graph = uqbar.graphs.Graph(
            attributes={
                "bgcolor": "transparent",
                "color": "lightslategrey",
                "dpi": 72,
                "fontname": "Arial",
                "outputorder": "edgesfirst",
                "overlap": "prism",
                "penwidth": 2,
                "rankdir": "TB",
                "ranksep": 0.5,
                "splines": "spline",
                "style": ("dotted", "rounded"),
            },
            edge_attributes={"penwidth": 2},
            node_attributes={
                "fontname": "Arial",
                "fontsize": 12,
                "penwidth": 2,
                "shape": "Mrecord",
                "style": ("filled", "rounded"),
            },
            children=[self._as_graphviz_node()],
        )
        return graph

    def __int__(self):
        return int(self.node_id)

    def __repr__(self):
        class_name = type(self).__name__
        node_id = "???"
        if self.node_id is not None:
            node_id = self.node_id
        allocated = "+" if self.is_allocated else "-"
        if self.name is None:
            return f"<{allocated} {class_name}: {node_id}>"
        return "<{allocated} {class_name}: {node_id} ({name})>"

    ### PRIVATE METHODS ###

    def _allocate(self, paused_nodes, requests, server, synthdefs):
        import supriya.commands

        if paused_nodes:
            requests.append(
                supriya.commands.NodeRunRequest(
                    node_id_run_flag_pairs=[(node, False) for node in paused_nodes]
                )
            )
        if not requests:
            return self
        elif 1 < len(requests):
            request = supriya.commands.RequestBundle(contents=requests)
        else:
            request = requests[0]
        requests[:] = [request]
        if synthdefs:
            synthdef_request = supriya.commands.SynthDefReceiveRequest(
                synthdefs=synthdefs, callback=requests[0]
            )
            if len(synthdef_request.to_datagram(with_placeholders=True)) > 8192:
                directory_path = pathlib.Path(tempfile.mkdtemp())
                synthdef_request = supriya.commands.SynthDefLoadDirectoryRequest(
                    directory_path=directory_path, callback=requests[0]
                )
                for synthdef in synthdefs:
                    file_name = "{}.scsyndef".format(synthdef.anonymous_name)
                    synthdef_path = directory_path / file_name
                    synthdef_path.write_bytes(synthdef.compile())
            requests[:] = [synthdef_request]
            if len(requests[0].to_datagram(with_placeholders=True)) > 8192:
                node_allocate_request = requests[0].callback
                synthdef_request = new(requests[0], callback=None)
                requests[:] = [node_allocate_request, synthdef_request]
        for request in requests:
            request.communicate(server=server, sync=True)
        return self

    def _as_graphviz_node(self):
        node = uqbar.graphs.Node(name=self._get_graphviz_name())
        group = uqbar.graphs.RecordGroup()
        group.append(uqbar.graphs.RecordField(label=type(self).__name__))
        if self.name:
            group.append(uqbar.graphs.RecordField(label="name: " + self.name))
        if self.node_id is not None:
            label = "id: " + str(self.node_id)
        else:
            label = "id: " + "-".join(str(_) for _ in (0,) + self.graph_order)
        group.append(uqbar.graphs.RecordField(label=label))
        node.append(group)
        return node

    def _cache_control_interface(self):
        return self._control_interface.as_dict()

    @staticmethod
    def _expr_as_target(expr):
        from supriya import Server

        if isinstance(expr, Server):
            expr = expr.default_group
        if not isinstance(expr, Node):
            raise ValueError
        if not expr.is_allocated:
            raise ServerOffline
        return expr

    def _get_graphviz_name(self):
        parts = [uqbar.strings.to_dash_case(type(self).__name__)]
        if self.is_allocated:
            parts.append(str(self.node_id))
        else:
            parts.extend(str(_) for _ in self.graph_order)
        return "-".join(parts)

    def _handle_response(self, response):
        import supriya.commands

        if not isinstance(response, supriya.commands.NodeInfoResponse):
            return
        if response.action == NodeAction.NODE_REMOVED:
            self._set_parent(None)
            self._unregister_with_local_server()
        elif response.action == NodeAction.NODE_ACTIVATED:
            self._is_paused = False
        elif response.action == NodeAction.NODE_DEACTIVATED:
            self._is_paused = True
        elif response.action == NodeAction.NODE_MOVED:
            old_parent = self.parent
            new_parent = self.server._nodes[response.parent_id]
            old_index = self.parent.index(self)
            new_index = None
            previous_node = self.server._nodes.get(response.previous_node_id)
            if previous_node is not None:
                try:
                    new_index = new_parent.index(previous_node) + 1
                except ValueError:
                    pass
            next_node = self.server._nodes.get(response.next_node_id)
            if next_node is not None:
                try:
                    new_index = new_parent.index(next_node)
                except ValueError:
                    pass
            if new_parent is old_parent:
                if new_index is not None and new_index != old_index:
                    if new_index < old_index:
                        self.parent._children.remove(self)
                        self.parent._children.insert(new_index, self)
                    else:
                        self.parent._children.insert(new_index, self)
                        self.parent._children.pop(old_index)
            else:
                self._set_parent(new_parent)
                new_index = new_index or 0
                new_parent._children.insert(new_index, self)

    def _move_node(self, *, add_action, node):
        target_node = self
        if add_action in (AddAction.ADD_TO_HEAD, AddAction.ADD_TO_TAIL):
            parent_node = target_node
        else:
            parent_node = target_node._parent
        node._set_parent(parent_node)
        if add_action == AddAction.ADD_TO_HEAD:
            parent_node._children.insert(0, node)
        elif add_action == AddAction.ADD_TO_TAIL:
            parent_node._children.append(node)
        elif add_action == AddAction.ADD_BEFORE:
            index = parent_node.index(target_node)
            parent_node._children.insert(index, node)
        elif add_action == AddAction.ADD_AFTER:
            index = parent_node.index(target_node)
            parent_node._children.insert(index + 1, node)
        elif add_action == AddAction.REPLACE:
            index = parent_node.index(target_node)
            parent_node._children[index] = node
            target_node._set_parent(None)
            target_node._unregister_with_local_server()

    def _register_with_local_server(
        self,
        server: "supriya.realtime.servers.Server",
        node_id: Optional[int] = None,
        node_id_is_permanent: bool = False,
    ):
        id_allocator = server.node_id_allocator
        if node_id is None:
            if node_id_is_permanent:
                node_id = id_allocator.allocate_permanent_node_id()
            else:
                node_id = server.node_id_allocator.allocate_node_id()
        else:
            node_id = int(node_id)
        if not self.is_allocated or self.server is not server:
            self._server = server
        self._node_id = node_id
        self._node_id_is_permanent = bool(node_id_is_permanent)
        self._server._nodes[self._node_id] = self
        return node_id

    def _remove_control_interface_from_parentage(self, old_parent, name_dictionary):
        if old_parent is None or not name_dictionary:
            return
        for parent in old_parent.parentage:
            parent._control_interface.remove_controls(name_dictionary)

    def _restore_control_interface_to_parentage(self, new_parent, name_dictionary):
        if new_parent is None or not name_dictionary:
            return
        for parent in new_parent.parentage:
            parent._control_interface.add_controls(name_dictionary)

    def _run(self, run_flag):
        self._is_paused = not bool(run_flag)

    def _set_parent(self, new_parent):
        old_parent = self._parent
        named_children = self._cache_named_children()
        control_interface = self._cache_control_interface()
        self._remove_from_parent()
        self._remove_named_children_from_parentage(old_parent, named_children)
        self._remove_control_interface_from_parentage(old_parent, control_interface)
        self._parent = new_parent
        self._restore_named_children_to_parentage(new_parent, named_children)
        self._restore_control_interface_to_parentage(new_parent, control_interface)

    def _unregister_with_local_server(self):
        node_id = self.node_id
        if self.server is not None:
            if self._node_id in self._server._nodes:
                del self._server._nodes[self._node_id]
            if self.node_id_is_permanent:
                self.server.node_id_allocator.free_permanent_node_id(self.node_id)
        self._node_id = None
        self._node_id_is_permanent = None
        self._server = None
        return node_id

    ### PUBLIC METHODS ###

    def add_group(self, add_action: AddActionLike = None) -> "Group":
        """
        Add a group relative to this node via ``add_action``.

        ::

            >>> server = supriya.Server().boot()
            >>> print(server.query())
            NODE TREE 0 group
                1 group

        ::

            >>> node = server.add_group()
            >>> group = node.add_group()
            >>> print(server.query())
            NODE TREE 0 group
                1 group
                    1000 group
                        1001 group

        """
        if add_action is None:
            add_action = self._valid_add_actions[0]
        add_action = AddAction.from_expr(add_action)
        if add_action not in self._valid_add_actions:
            raise ValueError("Invalid add action: {add_action}")
        group = Group()
        group.allocate(add_action=add_action, target_node=self)
        return group

    def add_synth(
        self,
        synthdef: Optional[SynthDef] = None,
        add_action: AddActionLike = None,
        **kwargs,
    ) -> "Synth":
        """
        Add a synth relative to this node via ``add_action``.

        ::

            >>> server = supriya.Server().boot()
            >>> print(server.query())
            NODE TREE 0 group
                1 group

        ::

            >>> node = server.add_group()
            >>> synth = node.add_synth()
            >>> print(server.query())
            NODE TREE 0 group
                1 group
                    1000 group
                        1001 default
                            out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5

        """
        if add_action is None:
            add_action = self._valid_add_actions[0]
        add_action = AddAction.from_expr(add_action)
        if add_action not in self._valid_add_actions:
            raise ValueError("Invalid add action: {add_action}")
        synth = Synth(synthdef=synthdef, **kwargs)
        synth.allocate(add_action=add_action, target_node=self)
        return synth

    def free(self) -> "Node":
        import supriya.commands

        self._set_parent(None)
        server = self.server
        if self.node_id is not None and server is not None and server.is_running:
            node_id = self._unregister_with_local_server()
            node_free_request = supriya.commands.NodeFreeRequest(node_ids=(node_id,))
            node_free_request.communicate(server=server, sync=False)
        return self

    def move_node(self, node: "Node", add_action: AddActionLike = None) -> "Node":
        """
        Move ``node`` relative to this node via ``add_action``.

        ::

            >>> server = supriya.Server().boot()
            >>> group_one = server.add_group()
            >>> group_two = server.add_group()
            >>> print(server.query())
            NODE TREE 0 group
                1 group
                    1001 group
                    1000 group

        ::

            >>> _ = group_two.move_node(group_one, "add_to_head")
            >>> print(server.query())
            NODE TREE 0 group
                1 group
                    1001 group
                        1000 group

        """
        if add_action is None:
            add_action = self._valid_add_actions[0]
        add_action = AddAction.from_expr(add_action)
        if add_action not in self._valid_add_actions:
            raise ValueError("Invalid add action: {add_action}")
        elif node in self.parentage:
            raise ValueError("Node in parentage")
        if add_action == AddAction.ADD_BEFORE:
            if self.parent is None:
                raise ValueError("Cannot move before without parent")
            index = self.parent.index(self)
            self.parent.insert(index, node)
        elif add_action == AddAction.ADD_AFTER:
            if self.parent is None:
                raise ValueError("Cannot move after without parent")
            index = self.parent.index(self)
            self.parent.insert(index + 1, node)
        elif add_action == AddAction.ADD_TO_HEAD:
            cast(Group, self).prepend(node)
        elif add_action == AddAction.ADD_TO_TAIL:
            cast(Group, self).append(node)
        elif add_action == AddAction.REPLACE:
            self.replace_with(node)
        return node

    def pause(self):
        import supriya.commands

        if self.is_paused:
            return
        self._is_paused = True
        if self.is_allocated:
            request = supriya.commands.NodeRunRequest(
                node_id_run_flag_pairs=((self.node_id, False),)
            )
            request.communicate(server=self.server, sync=False)

    def precede_by(self, expr):
        if not isinstance(expr, Sequence):
            expr = [expr]
        index = self.parent.index(self)
        self.parent[index:index] = expr

    def query(self):
        from supriya.commands import NodeQueryRequest
        from supriya.querytree import QueryTreeGroup, QueryTreeSynth

        query_tree = {}
        stack = [self.node_id]
        while stack:
            node_id = stack.pop()
            if node_id in query_tree:
                continue
            request = NodeQueryRequest(node_id)
            response = request.communicate(server=self.server)
            if (response.next_node_id or -1) > 0:
                stack.append(response.next_node_id)
            if (response.head_node_id or -1) > 0:
                stack.append(response.head_node_id)
            if response.is_group:
                query_tree[node_id] = QueryTreeGroup.from_response(response)
            else:
                query_tree[node_id] = QueryTreeSynth.from_response(response)
            if response.parent_id in query_tree:
                query_tree[response.parent_id]._children += (query_tree[node_id],)
        return query_tree[self.node_id]

    def replace_with(self, expr):
        if not isinstance(expr, Sequence):
            expr = [expr]
        index = self.parent.index(self)
        self.parent[index : index + 1] = expr

    def succeed_by(self, expr):
        if not isinstance(expr, Sequence):
            expr = [expr]
        index = self.parent.index(self)
        self.parent[index + 1 : index + 1] = expr

    def unpause(self):
        import supriya.commands

        if not self.is_paused:
            return
        self._is_paused = False
        if self.is_allocated:
            request = supriya.commands.NodeRunRequest(
                node_id_run_flag_pairs=((self.node_id, True),)
            )
            request.communicate(server=self.server, sync=False)

    ### PUBLIC PROPERTIES ###

    @property
    def is_allocated(self) -> bool:
        if self.server is not None:
            return self in self.server
        return False

    @property
    def is_paused(self) -> bool:
        return self._is_paused

    @property
    def node_id(self) -> Optional[int]:
        return self._node_id

    @property
    def node_id_is_permanent(self) -> bool:
        return self._node_id_is_permanent

    @property
    def server(self) -> Optional["supriya.realtime.servers.Server"]:
        return self._server


class Group(Node, UniqueTreeList):
    """
    A group.

    ::

        >>> import supriya.realtime
        >>> server = supriya.Server()
        >>> server.boot()
        <Server: udp://127.0.0.1:57110, 8i8o>

    ::

        >>> group = supriya.realtime.Group()
        >>> group.allocate(server)
        <+ Group: 1000>

    ::

        >>> group.free()
        <- Group: ???>

    ::

        >>> server.quit()
        <Server: offline>

    """

    ### CLASS VARIABLES ###

    _valid_add_actions: Tuple[int, ...] = (
        AddAction.ADD_TO_HEAD,
        AddAction.ADD_TO_TAIL,
        AddAction.ADD_AFTER,
        AddAction.ADD_BEFORE,
        AddAction.REPLACE,
    )

    ### INITIALIZER ###

    def __init__(self, children=None, name=None, node_id_is_permanent=False):
        self._control_interface = GroupInterface(client=self)
        Node.__init__(self, name=name, node_id_is_permanent=node_id_is_permanent)
        UniqueTreeList.__init__(self, children=children, name=name)

    ### SPECIAL METHODS ###

    def __graph__(self):
        graph = super().__graph__()
        parent_node = graph[self._get_graphviz_name()]
        for child in self:
            graph.extend(child.__graph__())
            child_node = graph[child._get_graphviz_name()]
            parent_node.attach(child_node)
        return graph

    def __setitem__(self, i, expr):
        """
        Sets `expr` in self at index `i`.

        ::

            >>> group_one = supriya.realtime.Group()
            >>> group_two = supriya.realtime.Group()
            >>> group_one.append(group_two)

        """
        # TODO: lean on uqbar's __setitem__ more.
        self._validate(expr)
        if isinstance(i, slice):
            assert isinstance(expr, Sequence)
        if isinstance(i, str):
            i = self.index(self._named_children[i])
        if isinstance(i, int):
            if i < 0:
                i = len(self) + i
            i = slice(i, i + 1)
        if (
            i.start == i.stop
            and i.start is not None
            and i.stop is not None
            and i.start <= -len(self)
        ):
            start, stop = 0, 0
        else:
            start, stop, stride = i.indices(len(self))
        if not isinstance(expr, Sequence):
            expr = [expr]
        if self.is_allocated:
            self._set_allocated(expr, start, stop)
        else:
            self._set_unallocated(expr, start, stop)

    def __str__(self):
        result = []
        node_id = self.node_id
        if node_id is None:
            node_id = "???"
        if self.name:
            string = f"{node_id} group ({self.name})"
        else:
            string = f"{node_id} group"
        result.append(string)
        for child in self:
            lines = str(child).splitlines()
            for line in lines:
                result.append(f"    {line}")
        return "\n".join(result)

    ### PRIVATE METHODS ###

    def _as_graphviz_node(self):
        node = super()._as_graphviz_node()
        node.attributes["fillcolor"] = "lightsteelblue2"
        return node

    @staticmethod
    def _iterate_setitem_expr(group, expr, start=0):
        if not start or not group:
            outer_target_node = group
        else:
            outer_target_node = group[start - 1]
        for outer_node in expr:
            if outer_target_node is group:
                outer_add_action = AddAction.ADD_TO_HEAD
            else:
                outer_add_action = AddAction.ADD_AFTER
            outer_node_was_allocated = outer_node.is_allocated
            yield outer_node, outer_target_node, outer_add_action
            outer_target_node = outer_node
            if isinstance(outer_node, Group) and not outer_node_was_allocated:
                for (
                    inner_node,
                    inner_target_node,
                    inner_add_action,
                ) in Group._iterate_setitem_expr(outer_node, outer_node):
                    yield inner_node, inner_target_node, inner_add_action

    def _collect_requests_and_synthdefs(self, expr, server, start=0):
        import supriya.commands

        nodes = set()
        paused_nodes = set()
        synthdefs = set()
        requests = []
        iterator = Group._iterate_setitem_expr(self, expr, start)
        for node, target_node, add_action in iterator:
            nodes.add(node)
            if node.is_allocated:
                if add_action == AddAction.ADD_TO_HEAD:
                    request = supriya.commands.GroupHeadRequest(
                        node_id_pairs=[(node, target_node)]
                    )
                else:
                    request = supriya.commands.NodeAfterRequest(
                        node_id_pairs=[(node, target_node)]
                    )
                requests.append(request)
            else:
                if isinstance(node, Group):
                    request = supriya.commands.GroupNewRequest(
                        items=[
                            supriya.commands.GroupNewRequest.Item(
                                add_action=add_action,
                                node_id=node,
                                target_node_id=target_node,
                            )
                        ]
                    )
                    requests.append(request)
                else:
                    if node.synthdef not in server:
                        synthdefs.add(node.synthdef)
                    (settings, map_requests) = node.controls._make_synth_new_settings()
                    request = supriya.commands.SynthNewRequest(
                        add_action=add_action,
                        node_id=node,
                        synthdef=node.synthdef,
                        target_node_id=target_node,
                        **settings,
                    )
                    requests.append(request)
                    requests.extend(map_requests)
                if node.is_paused:
                    paused_nodes.add(node)
        return nodes, paused_nodes, requests, synthdefs

    def _set_allocated(self, expr, start, stop):
        # TODO: Consolidate this with Group.allocate()
        # TODO: Perform tree mutations via command apply methods, not here
        import supriya.commands

        old_nodes = self._children[start:stop]
        self._children.__delitem__(slice(start, stop))
        for old_node in old_nodes:
            old_node._set_parent(None)
        for child in expr:
            if child in self and self.index(child) < start:
                start -= 1
            child._set_parent(self)
        self._children.__setitem__(slice(start, start), expr)
        (
            new_nodes,
            paused_nodes,
            requests,
            synthdefs,
        ) = self._collect_requests_and_synthdefs(expr, self.server, start=start)
        nodes_to_free = [_ for _ in old_nodes if _ not in new_nodes]
        if nodes_to_free:
            requests.append(
                supriya.commands.NodeFreeRequest(
                    node_ids=sorted(nodes_to_free, key=lambda x: x.node_id)
                )
            )
        return self._allocate(paused_nodes, requests, self.server, synthdefs)

    def _set_unallocated(self, expr, start, stop):
        for node in expr:
            node.free()
        for old_child in tuple(self[start:stop]):
            old_child._set_parent(None)
        self._children[start:stop] = expr
        for new_child in expr:
            new_child._set_parent(self)

    def _unregister_with_local_server(self):
        for child in self:
            child._unregister_with_local_server()
        return Node._unregister_with_local_server(self)

    def _validate(self, expr):
        assert all(isinstance(_, supriya.realtime.Node) for _ in expr)
        parentage = self.parentage
        for x in expr:
            assert isinstance(x, Node)
            if isinstance(x, Group):
                assert x not in parentage

    ### PUBLIC METHODS ###

    def allocate(
        self, target_node, add_action=None, node_id_is_permanent=False, sync=False
    ):
        # TODO: Consolidate this with Group.allocate()
        import supriya.commands

        if self.is_allocated:
            return
        self._node_id_is_permanent = bool(node_id_is_permanent)
        target_node = Node._expr_as_target(target_node)
        server = target_node.server
        group_new_request = supriya.commands.GroupNewRequest(
            items=[
                supriya.commands.GroupNewRequest.Item(
                    add_action=add_action,
                    node_id=self,
                    target_node_id=target_node.node_id,
                )
            ]
        )
        (
            nodes,
            paused_nodes,
            requests,
            synthdefs,
        ) = self._collect_requests_and_synthdefs(self, server)
        requests = [group_new_request, *requests]
        if self.is_paused:
            paused_nodes.add(self)
        return self._allocate(paused_nodes, requests, server, synthdefs)

    def free(self):
        for node in self:
            node._unregister_with_local_server()
        Node.free(self)
        return self

    def prepend(self, expr: Node):
        self[0:0] = [expr]

    ### PUBLIC PROPERTIES ###

    @property
    def controls(self) -> GroupInterface:
        return self._control_interface


class Synth(Node):
    """
    A synth.

    ::

        >>> import supriya.realtime
        >>> server = supriya.Server()
        >>> server.boot()
        <Server: udp://127.0.0.1:57110, 8i8o>

    ::

        >>> import supriya.synthdefs
        >>> import supriya.ugens
        >>> with supriya.synthdefs.SynthDefBuilder(
        ...     amplitude=0.0,
        ...     frequency=440.0,
        ... ) as builder:
        ...     sin_osc = supriya.ugens.SinOsc.ar(
        ...         frequency=builder["frequency"],
        ...     )
        ...     sin_osc *= builder["amplitude"]
        ...     out = supriya.ugens.Out.ar(
        ...         bus=0,
        ...         source=[sin_osc, sin_osc],
        ...     )
        ...
        >>> synthdef = builder.build()
        >>> synthdef.allocate(server)
        <SynthDef: e41193ac8b7216f49ff0d477876a3bf3>

    ::

        >>> synth = supriya.realtime.Synth(amplitude=0.5, frequency=443, synthdef=synthdef)
        >>> synth
        <- Synth: ??? e41193ac8b7216f49ff0d477876a3bf3>

    ::

        >>> synth.allocate(server)
        <+ Synth: 1000 e41193ac8b7216f49ff0d477876a3bf3>

    ::

        >>> synth["frequency"] = 666.0
        >>> synth["frequency"]
        666.0

    ::

        >>> server.quit()
        <Server: offline>

    """

    ### CLASS VARIABLES ###

    _valid_add_actions = (AddAction.ADD_BEFORE, AddAction.ADD_AFTER, AddAction.REPLACE)

    ### INITIALIZER ###

    def __init__(
        self,
        synthdef: Optional[SynthDef] = None,
        name=None,
        node_id_is_permanent=False,
        **kwargs,
    ):
        synthdef = synthdef or supriya.assets.synthdefs.default
        if not isinstance(synthdef, SynthDef):
            raise ValueError(synthdef)
        Node.__init__(self, name=name, node_id_is_permanent=node_id_is_permanent)
        self._synthdef = synthdef
        self._control_interface = SynthInterface(client=self, synthdef=self._synthdef)
        self._control_interface._set(**kwargs)

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self._control_interface[item].value

    def __iter__(self):
        return iter(self._control_interface)

    def __repr__(self):
        class_name = type(self).__name__
        node_id = "???"
        if self.node_id is not None:
            node_id = self.node_id
        allocated = "+" if self.is_allocated else "-"
        synthdef_name = "???"
        if self.synthdef is not None:
            synthdef_name = self.synthdef.actual_name
        if self.name is None:
            return f"<{allocated} {class_name}: {node_id} {synthdef_name}>"
        return f"<{allocated} {class_name}: {node_id} {synthdef_name} ({self.name})>"

    def __setitem__(self, items, values):
        self.controls.__setitem__(items, values)

    def __str__(self):
        result = []
        node_id = self.node_id
        if node_id is None:
            node_id = "???"
        if self.name:
            string = "{node_id} {synthdef} ({name})"
        else:
            string = "{node_id} {synthdef}"
        string = string.format(
            name=self.name, node_id=node_id, synthdef=self.synthdef.actual_name
        )
        result.append(string)
        control_pieces = []
        for _, parameter in sorted(self.synthdef.indexed_parameters):
            control = self.controls[parameter.name]
            control_piece = "{}: {!s}".format(control.name, control.value)
            control_pieces.append(control_piece)
        control_pieces = "    " + ", ".join(control_pieces)
        result.append(control_pieces)
        result = "\n".join(result)
        return result

    ### PRIVATE METHODS ###

    def _as_graphviz_node(self):
        node = super()._as_graphviz_node()
        node.attributes["fillcolor"] = "lightgoldenrod2"
        return node

    def _unregister_with_local_server(self):
        node_id = Node._unregister_with_local_server(self)
        if "gate" in self.controls:
            self.controls["gate"].reset()
        return node_id

    ### PUBLIC METHODS ###

    def allocate(
        self,
        target_node,
        add_action=None,
        node_id_is_permanent=False,
        sync=True,
        **kwargs,
    ):
        import supriya.commands

        if self.is_allocated:
            return
        self._node_id_is_permanent = bool(node_id_is_permanent)
        target_node = Node._expr_as_target(target_node)
        server = target_node.server
        if not server.is_running:
            raise ServerOffline
        self.controls._set(**kwargs)
        # TODO: Map requests aren't necessary during /s_new
        settings, map_requests = self.controls._make_synth_new_settings()
        synth_request = supriya.commands.SynthNewRequest(
            add_action=add_action,
            node_id=self,
            synthdef=self.synthdef,
            target_node_id=target_node.node_id,
            **settings,
        )
        requests = [synth_request, *map_requests]
        paused_nodes = set()
        synthdefs = set()
        if self.is_paused:
            paused_nodes.add(self)
        if self.synthdef not in server:
            synthdefs.add(self.synthdef)
        return self._allocate(paused_nodes, requests, server, synthdefs)

    def release(self):
        if self.is_allocated and "gate" in self.controls:
            self["gate"] = 0
        else:
            self.free()
        return self

    ### PUBLIC PROPERTIES ###

    @property
    def controls(self) -> SynthInterface:
        return self._control_interface

    @property
    def synthdef(self) -> SynthDef:
        return self._synthdef


class RootNode(Group):

    ### CLASS VARIABLES ###

    _valid_add_actions: Tuple[int, ...] = (AddAction.ADD_TO_HEAD, AddAction.ADD_TO_TAIL)

    ### INITIALIZER ###

    def __init__(self, server):
        super().__init__()
        self._server = server

    ### SPECIAL METHODS ###

    def __str__(self):
        return "NODE TREE " + super().__str__()

    ### PRIVATE METHODS ###

    def _as_graphviz_node(self):
        node = super()._as_graphviz_node()
        node.attributes["fillcolor"] = "lightsalmon2"
        return node

    ### PUBLIC METHODS ###

    def allocate(self):
        pass

    def free(self):
        pass

    def pause(self):
        pass

    def unpause(self):
        pass

    ### PUBLIC PROPERTIES ###

    @property
    def node_id(self) -> int:
        return 0

    @property
    def parent(self) -> None:
        return None
