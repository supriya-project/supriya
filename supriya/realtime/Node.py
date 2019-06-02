import abc
import collections
import pathlib
import tempfile

import uqbar.graphs
import uqbar.strings
from uqbar.containers import UniqueTreeNode
from uqbar.objects import new

from supriya.enums import AddAction, NodeAction
from supriya.realtime.ServerObject import ServerObject


class Node(ServerObject, UniqueTreeNode):

    ### CLASS VARIABLES ###

    __slots__ = ("_is_paused", "_name", "_node_id", "_node_id_is_permanent", "_parent")

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, name=None, node_id_is_permanent=False):
        ServerObject.__init__(self)
        UniqueTreeNode.__init__(self, name=name)
        self._is_paused = False
        self._node_id = None
        self._node_id_is_permanent = bool(node_id_is_permanent)

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
        allocation_indicator = "+" if self.is_allocated else "-"
        if self.name is None:
            string = "<{allocated} {class_name}: {node_id}>".format(
                allocated=allocation_indicator, class_name=class_name, node_id=node_id
            )
        else:
            string = "<{allocated} {class_name}: {node_id} ({name})>".format(
                allocated=allocation_indicator,
                class_name=class_name,
                name=self.name,
                node_id=node_id,
            )
        return string

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

    def _as_node_target(self):
        return self

    def _cache_control_interface(self):
        return self._control_interface.as_dict()

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
            new_parent = self.server._nodes[response.parent_group_id]
            if new_parent is self.parent:
                new_index = 0
                if response.previous_node_id is not None:
                    previous_node = self.server._nodes[response.previous_node_id]
                    new_index = new_parent.index(previous_node) + 1
                elif response.next_node_id is not None:
                    next_node = self.server._nodes[response.next_node_id]
                    new_index = new_parent.index(next_node)
                old_index = self.parent.index(self)
                if new_index != self.parent.index(self):
                    if new_index < old_index:
                        self.parent._children.remove(self)
                        self.parent._children.insert(new_index, self)
                    else:
                        self.parent._children.insert(new_index, self)
                        self.parent._children.pop(old_index)
            else:
                self._set_parent(new_parent)
                index = 0
                if response.previous_node_id is not None:
                    previous_node = self.server._nodes[response.previous_node_id]
                    index = new_parent.index(previous_node) + 1
                elif response.next_node_id is not None:
                    next_node = self.server._nodes[response.next_node_id]
                    index = new_parent.index(next_node)
                new_parent._children.insert(index, self)

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
        self, node_id=None, node_id_is_permanent=False, server=None
    ):
        id_allocator = server.node_id_allocator
        if node_id is None:
            if node_id_is_permanent:
                node_id = id_allocator.allocate_permanent_node_id()
            else:
                node_id = server.node_id_allocator.allocate_node_id()
        else:
            node_id = int(node_id)
        ServerObject.allocate(self, server=server)
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
        ServerObject.free(self)
        return node_id

    ### PUBLIC METHODS ###

    @staticmethod
    def expr_as_target(expr):
        import supriya.realtime

        if expr is None:
            expr = Node.expr_as_target(supriya.realtime.Server.default())
        if hasattr(expr, "_as_node_target"):
            return expr._as_node_target()
        if isinstance(expr, (float, int)):
            server = supriya.realtime.Server.default()
            return server._nodes[int(expr)]
        if expr is None:
            raise supriya.exceptions.ServerOffline
        raise TypeError(expr)

    def free(self):
        import supriya.commands

        self._set_parent(None)
        server = self.server
        if self.node_id is not None and server.is_running:
            node_id = self._unregister_with_local_server()
            node_free_request = supriya.commands.NodeFreeRequest(node_ids=(node_id,))
            node_free_request.communicate(server=server, sync=False)
        return self

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
        if not isinstance(expr, collections.Sequence):
            expr = [expr]
        index = self.parent.index(self)
        self.parent[index:index] = expr

    def replace_with(self, expr):
        if not isinstance(expr, collections.Sequence):
            expr = [expr]
        index = self.parent.index(self)
        self.parent[index : index + 1] = expr

    def succeed_by(self, expr):
        if not isinstance(expr, collections.Sequence):
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
    def is_allocated(self):
        if self.server is not None:
            return self in self.server
        return False

    @property
    def is_paused(self):
        return self._is_paused

    @property
    def node_id(self):
        return self._node_id

    @property
    def node_id_is_permanent(self):
        return self._node_id_is_permanent
