# -*- encoding: utf-8 -*-
from supriya.tools.servertools.Node import Node


class Group(Node):
    r'''A group.

    ::

        >>> from supriya import servertools
        >>> server = servertools.Server()
        >>> server.boot()
        <Server: udp://127.0.0.1:57751, 8i8o>

    ::

        >>> group = servertools.Group()
        >>> group.allocate()
        <Group: 1000>

    ::

        >>> group.free()
        <Group: ???>

    ::

        >>> server.quit()
        <Server: offline>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Main Classes'

    __slots__ = (
        '_children',
        '_control_interface',
        '_named_children',
        )

    ### INITIALIZER ###

    def __init__(self):
        from supriya.tools import servertools
        Node.__init__(self)
        self._children = []
        self._control_interface = servertools.GroupInterface(
            client=self,
            )
        self._named_children = {}

    ### SPECIAL METHODS ###

    def __contains__(self, expr):
        for x in self._children:
            if x is expr:
                return True
        return False

    def __delitem__(self, expr):
        if isinstance(expr, int):
            self._children[expr].free()
        elif isinstance(expr, slice):
            for child in self._children[expr]:
                child.free()
        elif isinstance(expr, str):
            self._named_children[expr].free()
        else:
            raise ValueError(expr)

    def __getitem__(self, expr):
        if isinstance(expr, (int, slice)):
            return self._children[expr]
        elif isinstance(expr, str):
            return self._named_children[expr]
        raise ValueError(expr)

    def __iter__(self):
        for child in self._children:
            yield child

    def __len__(self):
        return len(self._children)

    def __setitem__(self, i, expr):
        r'''Sets `expr` in self at index `i`.

        ::

            >>> group_one = Group()
            >>> group_two = Group()
            >>> group_one.append(group_two)

        '''
        self._validate_setitem_expr(expr)
        expr, start, stop = self._coerce_setitem_arguments(i, expr)
        if self.is_allocated:
            self._set_allocated(expr, start, stop)
        else:
            self._set_unallocated(expr, start, stop)

#    def __setitem__(self, i, expr):
#        from supriya.tools import requesttools
#        from supriya.tools import servertools
#
#        assert self.is_allocated
#
#        self._validate_setitem_expr(expr)
#        expr, start, stop = self._coerce_setitem_arguments(i, expr)
#
#        old_children = tuple(self[start:stop])
#        for child in old_children:
#            if child not in expr:
#                child.free()
#
#        message_bundler = servertools.MessageBundler(
#            server=self.server,
#            sync=True,
#            )
#
#        synthdefs = set()
#        for node in expr:
#            if not isinstance(node, servertools.Synth):
#                continue
#            if node.synthdef.is_allocated:
#                continue
#            if node.synthdef in synthdefs:
#                continue
#            synthdefs.add(node.synthdef)
#        if synthdefs:
#            node.synthdef._allocate(server=self.server)
#            request = requesttools.SynthDefReceiveRequest(
#                synthdefs=tuple(synthdefs),
#                )
#            request.communicate(server=self.server)
#
#        with message_bundler:
#
#            if not start or not self:
#                target_node = self
#            else:
#                target_node = self[start - 1]
#
#            for node in expr:
#                if node.is_allocated:
#                    node._set_parent(self)
#                    if target_node is self:
#                        request = requesttools.GroupHeadRequest(
#                            node_id_pairs=requesttools.NodeIdPair(
#                                node_id=node.node_id,
#                                target_node_id=target_node.node_id,
#                                ),
#                            )
#                    else:
#                        request = requesttools.NodeAfterRequest(
#                            node_id_pairs=requesttools.NodeIdPair(
#                                node_id=node.node_id,
#                                target_node_id=target_node.node_id,
#                                )
#                            )
#                    message_bundler.add_message(request)
#                    if target_node is self:
#                        self._children.append(node)
#                    else:
#                        index = self._children.index(target_node)
#                        self._children.insert(index + 1, node)
#                else:
#                    if target_node is self:
#                        add_action = servertools.AddAction.ADD_TO_HEAD
#                    else:
#                        add_action = servertools.AddAction.ADD_AFTER
#                    add_action, node_id, target_node_id = Node.allocate(
#                        node,
#                        add_action=add_action,
#                        target_node=target_node,
#                        )
#                    map_requests = None
#                    if isinstance(node, servertools.Group):
#                        request = requesttools.GroupNewRequest(
#                            add_action=add_action,
#                            node_id=node,
#                            target_node_id=target_node,
#                            )
#                    else:
#                        settings, map_requests = \
#                            node.controls._make_synth_new_settings()
#                        request = requesttools.SynthNewRequest(
#                            add_action=add_action,
#                            node_id=node,
#                            synthdef=node.synthdef,
#                            target_node_id=target_node,
#                            **settings
#                            )
#                    message_bundler.add_message(request)
#                    if map_requests is not None:
#                        for map_request in map_requests:
#                            message_bundler.add_message(map_request)
#                target_node = node

    ### PRIVATE METHODS ###

    def _coerce_setitem_arguments(self, i, expr):
        if isinstance(i, int):
            if i < 0:
                i = len(self) + i
            i = slice(i, i + 1)
            expr = [expr]
        start, stop, _ = i.indices(len(self))
        return expr, start, stop

    @staticmethod
    def _iterate_children(group):
        from supriya.tools import servertools
        for child in group.children:
            if isinstance(child, servertools.Group):
                for subchild in Group._iterate_children(child):
                    yield subchild
            yield child

    @staticmethod
    def _iterate_synths(node):
        from supriya.tools import servertools
        if isinstance(node, servertools.Synth):
            yield node
        else:
            for child in node:
                for subchild in Group._iterate_synths(child):
                    yield subchild

    def _set_unallocated(self, expr, start, stop):
        for node in expr:
            node.free()
        for old_child in tuple(self[start:stop]):
            old_child._set_parent(None)
        self._children[start:stop] = expr
        for new_child in expr:
            new_child._set_parent(self)

    def _validate_setitem_expr(self, expr):
        from supriya.tools import servertools
        assert all(isinstance(_, servertools.Node) for _ in expr)
        parentage = self.parentage
        for x in expr:
            assert isinstance(x, servertools.Node)
            if isinstance(x, servertools.Group):
                assert x not in parentage

    ### PUBLIC METHODS ###

    def allocate(self): pass

#    def allocate(
#        self,
#        add_action=None,
#        node_id_is_permanent=False,
#        sync=False,
#        target_node=None,
#        ):
#        from supriya.tools import requesttools
#        add_action, node_id, target_node_id = Node.allocate(
#            self,
#            add_action=add_action,
#            node_id_is_permanent=node_id_is_permanent,
#            target_node=target_node,
#            )
#        request = requesttools.GroupNewRequest(
#            add_action=add_action,
#            node_id=node_id,
#            target_node_id=target_node_id,
#            )
#        request.communicate(
#            server=self.server,
#            sync=sync,
#            )
#        return self

    def append(self, expr):
        self.__setitem__(
            slice(len(self), len(self)),
            [expr]
            )

    def extend(self, expr):
        self.__setitem__(
            slice(len(self), len(self)),
            expr
            )

    def free(self):
        for node in Node._iterate_nodes(self):
            node._unregister_with_local_server()
        Node.free(self)
        return self

    def index(self, expr):
        for i, child in enumerate(self._children):
            if child is expr:
                return i
        else:
            message = '{!r} not in {!r}.'
            message = message.format(expr, self)
            raise ValueError(message)

    def insert(self, i, expr):
        self.__setitem__(
            slice(i, i),
            [expr]
            )

    def pop(self, i=-1):
        node = self[i]
        del(self[i])
        return node

    def remove(self, node):
        i = self.index(node)
        del(self[i])

    ### PUBLIC PROPERTIES ###

    @property
    def children(self):
        return tuple(self._children)

    @property
    def controls(self):
        return self._control_interface