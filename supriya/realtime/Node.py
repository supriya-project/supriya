import abc
from uqbar.containers import UniqueTreeNode
from supriya.realtime.AddAction import AddAction
from supriya.realtime.ServerObjectProxy import ServerObjectProxy


class Node(ServerObjectProxy, UniqueTreeNode):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_is_paused',
        '_name',
        '_node_id',
        '_node_id_is_permanent',
        '_parent',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, name=None, node_id_is_permanent=False):
        ServerObjectProxy.__init__(self)
        UniqueTreeNode.__init__(self, name=name)
        self._is_paused = False
        self._node_id = None
        self._node_id_is_permanent = bool(node_id_is_permanent)

    ### SPECIAL METHODS ###

    def __float__(self):
        return float(self.node_id)

    def __int__(self):
        return int(self.node_id)

    def __repr__(self):
        class_name = type(self).__name__
        node_id = '???'
        if self.node_id is not None:
            node_id = self.node_id
        if self.name is None:
            string = '<{class_name}: {node_id}>'.format(
                class_name=class_name,
                node_id=node_id,
                )
        else:
            string = '<{class_name}: {node_id} ({name})>'.format(
                class_name=class_name,
                name=self.name,
                node_id=node_id,
                )
        return string

    ### PRIVATE METHODS ###

    def _allocate(
        self,
        paused_nodes,
        requests,
        server,
        synthdefs,
    ):
        import supriya.commands
        if paused_nodes:
            requests.append(supriya.commands.NodeRunRequest(
                node_id_run_flag_pairs=[
                    (node, False) for node in paused_nodes
                ]))
        if not requests:
            return self
        elif 1 < len(requests):
            request = supriya.commands.RequestBundle(contents=requests)
        else:
            request = requests[0]
        if synthdefs:
            request = supriya.commands.SynthDefReceiveRequest(
                synthdefs=synthdefs,
                callback=request,
                )
        request.communicate(server=server, sync=True)
        return self

    def _as_node_target(self):
        return self

    def _cache_control_interface(self):
        return self._control_interface.as_dict()

    def _handle_response(self, response):
        import supriya.commands
        if not isinstance(response, supriya.commands.NodeInfoResponse):
            return
        if response.action == supriya.commands.NodeAction.NODE_REMOVED:
            self._set_parent(None)
            self._unregister_with_local_server()
        elif response.action == supriya.commands.NodeAction.NODE_ACTIVATED:
            self._is_paused = False
        elif response.action == supriya.commands.NodeAction.NODE_DEACTIVATED:
            self._is_paused = True
        elif response.action == supriya.commands.NodeAction.NODE_MOVED:
            new_parent = self.server._nodes[response.parent_group_id]
            if new_parent is self.parent:
                new_index = 0
                if response.previous_node_id is not None:
                    previous_node = \
                        self.server._nodes[response.previous_node_id]
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
                    previous_node = \
                        self.server._nodes[response.previous_node_id]
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
        self,
        node_id=None,
        node_id_is_permanent=False,
        server=None,
    ):
        id_allocator = server.node_id_allocator
        if node_id is None:
            if node_id_is_permanent:
                node_id = id_allocator.allocate_permanent_node_id()
            else:
                node_id = server.node_id_allocator.allocate_node_id()
        else:
            node_id = int(node_id)
        ServerObjectProxy.allocate(self, server=server)
        self._node_id = node_id
        self._node_id_is_permanent = bool(node_id_is_permanent)
        self._server._nodes[self._node_id] = self
        return node_id

    def _remove_control_interface_from_parentage(self, name_dictionary):
        if self._parent is not None and name_dictionary:
            for parent in self.parentage[1:]:
                parent._control_interface.remove_controls(name_dictionary)

    def _restore_control_interface_to_parentage(self, name_dictionary):
        if self._parent is not None and name_dictionary:
            for parent in self.parentage[1:]:
                parent._control_interface.add_controls(name_dictionary)

    def _run(self, run_flag):
        self._is_paused = not bool(run_flag)

    def _set_parent(self, new_parent):
        named_children = self._cache_named_children()
        control_interface = self._cache_control_interface()
        self._remove_named_children_from_parentage(named_children)
        self._remove_control_interface_from_parentage(control_interface)
        self._remove_from_parent()
        self._parent = new_parent
        self._restore_named_children_to_parentage(named_children)
        self._restore_control_interface_to_parentage(control_interface)

    def _unregister_with_local_server(self):
        node_id = self.node_id
        if self.server is not None:
            if self._node_id in self._server._nodes:
                del(self._server._nodes[self._node_id])
            if self.node_id_is_permanent:
                self.server.node_id_allocator.free_permanent_node_id(
                    self.node_id,
                    )
        self._node_id = None
        self._node_id_is_permanent = None
        ServerObjectProxy.free(self)
        return node_id

    ### PUBLIC METHODS ###

    @staticmethod
    def expr_as_target(expr):
        import supriya.realtime
        if expr is None:
            return Node.expr_as_target(supriya.realtime.Server())
        elif hasattr(expr, '_as_node_target'):
            return expr._as_node_target()
        elif isinstance(expr, (float, int)):
            server = supriya.realtime.Server.get_default_server()
            return server._nodes[int(expr)]
        raise TypeError(expr)

    def free(self):
        import supriya.commands
        self._set_parent(None)
        server = self.server
        if self.node_id is not None and server.is_running:
            node_id = self._unregister_with_local_server()
            node_free_request = supriya.commands.NodeFreeRequest(
                node_ids=(node_id,),
                )
            node_free_request.communicate(
                server=server,
                sync=False,
                )
        return self

    def pause(self):
        import supriya.commands
        if self.is_paused:
            return
        self._is_paused = True
        if self.is_allocated:
            request = supriya.commands.NodeRunRequest(
                node_id_run_flag_pairs=(
                    (self.node_id, False),
                    ),
                )
            request.communicate(
                server=self.server,
                sync=False,
                )

    def unpause(self):
        import supriya.commands
        if not self.is_paused:
            return
        self._is_paused = False
        if self.is_allocated:
            request = supriya.commands.NodeRunRequest(
                node_id_run_flag_pairs=(
                    (self.node_id, True),
                    ),
                )
            request.communicate(
                server=self.server,
                sync=False,
                )

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
