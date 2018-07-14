import collections
from uqbar.containers import UniqueTreeContainer
from supriya.realtime.Node import Node


class Group(Node, UniqueTreeContainer):
    """
    A group.

    ::

        >>> import supriya.realtime
        >>> server = supriya.realtime.Server()
        >>> server.boot()
        <Server: udp://127.0.0.1:57751, 8i8o>

    ::

        >>> group = supriya.realtime.Group()
        >>> group.allocate()
        <Group: 1000>

    ::

        >>> group.free()
        <Group: ???>

    ::

        >>> server.quit()
        <Server: offline>

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Main Classes'

    __slots__ = (
        '_children',
        '_control_interface',
        '_named_children',
        )

    ### INITIALIZER ###

    def __init__(self, children=None, name=None):
        import supriya.realtime
        self._control_interface = supriya.realtime.GroupInterface(client=self)
        Node.__init__(self, name=name)
        UniqueTreeContainer.__init__(self, children=children, name=name)

    ### SPECIAL METHODS ###

    def __setitem__(self, i, expr):
        """
        Sets `expr` in self at index `i`.

        ::

            >>> group_one = Group()
            >>> group_two = Group()
            >>> group_one.append(group_two)

        """
        # TODO: lean on uqbar's __setitem__ more.
        self._validate_setitem_expr(expr)
        if isinstance(i, slice):
            assert isinstance(expr, collections.Sequence)
        if isinstance(i, str):
            i = self.index(self._named_children[i])
        if isinstance(i, int):
            if i < 0:
                i = len(self) + i
            i = slice(i, i + 1)
        if (
            i.start == i.stop and
            i.start is not None and
            i.stop is not None and
            i.start <= -len(self)
        ):
            start, stop = 0, 0
        else:
            start, stop, stride = i.indices(len(self))
        if not isinstance(expr, collections.Sequence):
            expr = [expr]
        if self.is_allocated:
            self._set_allocated(expr, start, stop)
        else:
            self._set_unallocated(expr, start, stop)

    def __str__(self):
        result = []
        node_id = self.node_id
        if node_id is None:
            node_id = '???'
        if self.name:
            string = '{node_id} group ({name})'
        else:
            string = '{node_id} group'
        string = string.format(
            name=self.name,
            node_id=node_id,
            )
        result.append(string)
        for child in self:
            assert child.parent is self
            lines = str(child).splitlines()
            for line in lines:
                result.append('    {}'.format(line))
        return '\n'.join(result)

    ### PRIVATE METHODS ###

    def _allocate_synthdefs(self, synthdefs):
        import supriya.synthdefs
        supriya.synthdefs.SynthDef._allocate_synthdefs(synthdefs, self.server)

    @staticmethod
    def _iterate_children(group):
        import supriya.realtime
        for child in group.children:
            if isinstance(child, supriya.realtime.Group):
                for subchild in Group._iterate_children(child):
                    yield subchild
            yield child

    @staticmethod
    def _iterate_setitem_expr(group, expr, start=0):
        import supriya.realtime
        if not start or not group:
            outer_target_node = group
        else:
            outer_target_node = group[start - 1]
        for outer_node in expr:
            if outer_target_node is group:
                outer_add_action = supriya.realtime.AddAction.ADD_TO_HEAD
            else:
                outer_add_action = supriya.realtime.AddAction.ADD_AFTER
            outer_node_was_allocated = outer_node.is_allocated
            yield outer_node, outer_target_node, outer_add_action
            outer_target_node = outer_node
            if (
                isinstance(outer_node, supriya.realtime.Group) and
                not outer_node_was_allocated
            ):
                for inner_node, inner_target_node, inner_add_action in (
                    Group._iterate_setitem_expr(outer_node, outer_node)
                ):
                    yield inner_node, inner_target_node, inner_add_action

    @staticmethod
    def _iterate_synths(node):
        import supriya.realtime
        if isinstance(node, supriya.realtime.Synth):
            yield node
        else:
            for child in node:
                for subchild in Group._iterate_synths(child):
                    yield subchild

    def _collect_requests_and_synthdefs(self, expr, start=0):
        import supriya.commands
        import supriya.realtime
        nodes = set()
        paused_nodes = set()
        synthdefs = set()
        requests = []
        iterator = Group._iterate_setitem_expr(self, expr, start)
        for node, target_node, add_action in iterator:
            nodes.add(node)
            if node.is_allocated:
                if add_action == supriya.realtime.AddAction.ADD_TO_HEAD:
                    request = supriya.commands.GroupHeadRequest(
                        node_id_pairs=supriya.commands.NodeIdPair(
                            node_id=node,
                            target_node_id=target_node,
                            ),
                        )
                else:
                    request = supriya.commands.NodeAfterRequest(
                        node_id_pairs=supriya.commands.NodeIdPair(
                            node_id=node,
                            target_node_id=target_node,
                            ),
                        )
                requests.append(request)
            else:
                node._register_with_local_server(server=self.server)
                if isinstance(node, supriya.realtime.Group):
                    request = supriya.commands.GroupNewRequest(
                        add_action=add_action,
                        node_id=node,
                        target_node_id=target_node,
                        )
                    requests.append(request)
                else:
                    if not node.synthdef.is_allocated:
                        synthdefs.add(node.synthdef)
                    settings, map_requests = \
                        node.controls._make_synth_new_settings()
                    request = supriya.commands.SynthNewRequest(
                        add_action=add_action,
                        node_id=node,
                        synthdef=node.synthdef,
                        target_node_id=target_node,
                        **settings
                        )
                    requests.append(request)
                    requests.extend(map_requests)
                if node.is_paused:
                    paused_nodes.add(node)
        return nodes, paused_nodes, requests, synthdefs

    def _set_allocated(self, expr, start, stop):
        import supriya.commands
        import supriya.realtime

        old_nodes = self._children[start:stop]
        self._children.__delitem__(slice(start, stop))
        for old_node in old_nodes:
            old_node._set_parent(None)
        for child in expr:
            if child in self and self.index(child) < start:
                start -= 1
            child._set_parent(self)
        self._children.__setitem__(slice(start, start), expr)

        new_nodes, paused_nodes, requests, synthdefs = \
            self._collect_requests_and_synthdefs(expr, start)
        self._allocate_synthdefs(synthdefs)

        old_node_ids = []
        for old_node in old_nodes:
            if old_node in new_nodes:
                continue
            old_node_id = old_node._unregister_with_local_server()
            old_node._set_parent(None)
            old_node_ids.append(old_node_id)
            #if isinstance(old_node, supriya.realtime.Group):
            #    for old_node_child in Group._iterate_children(old_node):
            #        old_node_child._unregister_with_local_server()
        if old_node_ids:
            node_free_request = supriya.commands.NodeFreeRequest(
                node_ids=old_node_ids,
                )
            requests.insert(0, node_free_request)

        if paused_nodes:
            pairs = sorted((node.node_id, False) for node in paused_nodes)
            request = supriya.commands.NodeRunRequest(
                node_id_run_flag_pairs=pairs,
                )
            requests.append(request)

        message_bundler = supriya.realtime.MessageBundler(
            server=self.server,
            sync=True,
            )
        message_bundler.add_messages(requests)
        message_bundler.send_messages()

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

    def _validate_setitem_expr(self, expr):
        import supriya.realtime
        assert all(isinstance(_, supriya.realtime.Node) for _ in expr)
        parentage = self.parentage
        for x in expr:
            assert isinstance(x, supriya.realtime.Node)
            if isinstance(x, supriya.realtime.Group):
                assert x not in parentage

    ### PUBLIC METHODS ###

    def allocate(
        self,
        add_action=None,
        node_id_is_permanent=False,
        sync=False,
        target_node=None,
    ):
        # TODO: Handle AddAction.REPLACE un-allocation of target node
        import supriya.commands
        import supriya.realtime
        if self.is_allocated:
            return
        add_action, node_id, target_node_id = Node.allocate(
            self,
            add_action=add_action,
            node_id_is_permanent=node_id_is_permanent,
            target_node=target_node,
            )
        group_new_request = supriya.commands.GroupNewRequest(
            add_action=add_action,
            node_id=node_id,
            target_node_id=target_node_id,
            )
        nodes, paused_nodes, requests, synthdefs = \
            self._collect_requests_and_synthdefs(self)
        if self.is_paused:
            paused_nodes.add(self)
        requests.insert(0, group_new_request)
        if synthdefs:
            self._allocate_synthdefs(synthdefs)
        if paused_nodes:
            pairs = sorted((node.node_id, False) for node in paused_nodes)
            request = supriya.commands.NodeRunRequest(
                node_id_run_flag_pairs=pairs,
                )
            requests.append(request)
        if 1 < len(requests):
            message_bundler = supriya.realtime.MessageBundler(
                server=self.server,
                sync=True,
                )
            message_bundler.add_messages(requests)
            message_bundler.add_synchronizing_request(group_new_request)
            message_bundler.send_messages()
        else:
            group_new_request.communicate(
                server=self.server,
                sync=True,
                )
        return self

    def free(self):
        for node in self:
            node._unregister_with_local_server()
        Node.free(self)
        return self

    def release(self):
        if 'gate' in self.controls:
            self.controls['gate'] = 0

    @property
    def controls(self):
        return self._control_interface
