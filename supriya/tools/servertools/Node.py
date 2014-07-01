# -*- encoding: utf-8 -*-
import abc
from supriya.tools.servertools.ServerObjectProxy import ServerObjectProxy


class Node(ServerObjectProxy):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_is_playing',
        '_node_id',
        '_node_id_is_permanent',
        '_parent',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        ServerObjectProxy.__init__(self)
        self._parent = None
        self._is_playing = False
        self._node_id = None
        self._node_id_is_permanent = None

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
        string = '<{class_name}: {node_id}>'.format(
            class_name=class_name,
            node_id=node_id,
            )
        return string

    ### PRIVATE METHODS ###

    def _remove_from_parent(self):
        if self.parent is not None:
            self.parent._children.remove(self)
        self._parent = None

    def _set_parent(self, new_parent):
        self._remove_from_parent()
        self._parent = new_parent

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def allocate(
        self,
        add_action=None,
        node_id_is_permanent=False,
        target_node=None,
        ):

        from supriya.tools import servertools
        if self.server is not None:
            raise ValueError

        target_node = Node.expr_as_target(target_node)
        server = target_node.server
        if server is None or not server.is_running:
            raise ValueError

        id_allocator = server.node_id_allocator
        if node_id_is_permanent:
            node_id = id_allocator.allocate_permanent_node_id()
        else:
            node_id = server.node_id_allocator.allocate_node_id()
        if node_id is None:
            raise ValueError
        elif node_id in server._nodes:
            raise ValueError
        ServerObjectProxy.allocate(self, server=server)
        self._node_id = node_id
        self._node_id_is_permanent = bool(node_id_is_permanent)
        self._server._nodes[self._node_id] = self

        add_action = servertools.AddAction.from_expr(add_action)
        if add_action == servertools.AddAction['ADD_TO_HEAD']:
            assert isinstance(target_node, servertools.Group)
            self._set_parent(target_node)
            target_node._children.insert(0, self)
        elif add_action == servertools.AddAction['ADD_TO_TAIL']:
            assert isinstance(target_node, servertools.Group)
            self._set_parent(target_node)
            target_node._children.append(self)
        elif add_action == servertools.AddAction['ADD_BEFORE']:
            self._set_parent(target_node.parent)
            index = self.parent._children.index(target_node)
            self._parent._children.insert(index, self)
        elif add_action == servertools.AddAction['ADD_AFTER']:
            self._set_parent(target_node.parent)
            index = self.parent._children.index(target_node)
            self._parent._children.insert(index + 1, self)
        elif add_action == servertools.AddAction['REPLACE']:
            assert target_node.parent is not self.server.root_node
            self._set_parent(target_node.parent)
            index = self.parent._children.index(target_node)
            target_node.free()
        else:
            raise ValueError

        self._is_playing = True

        return add_action, node_id, target_node.node_id

    @staticmethod
    def expr_as_node_id(expr):
        from supriya.tools import servertools
        if isinstance(expr, servertools.Server):
            return 0
        elif isinstance(expr, Node):
            return expr.node_id
        elif expr is None:
            return None
        elif isinstance(expr, int):
            return expr
        raise TypeError(expr)

    @staticmethod
    def expr_as_target(expr):
        from supriya.tools import servertools
        if expr is None:
            return Node.expr_as_target(servertools.Server())
        elif isinstance(expr, servertools.Server):
            return expr.default_group
        elif isinstance(expr, Node):
            return expr
        elif isinstance(expr, int):
            raise NotImplementedError
        raise TypeError(expr)

    def free(self, send_to_server=True):
        from supriya.tools import servertools
        self._set_parent(None)
        self._is_playing = False
        if self.server is not None:
            del(self._server._nodes[self._node_id])
            if send_to_server:
                message = servertools.CommandManager.make_node_free_message(
                    self.node_id,
                    )
                self.server.send_message(message)
            if self.node_id_is_permanent and self.server.node_id_allocator:
                self.server.node_id_allocator.free_permanent_node_id(
                    self.node_id,
                    )
        self._node_id = None
        self._node_id_is_permanent = None
        ServerObjectProxy.free(self)
        return self

    ### PUBLIC PROPERTIES ###

    @property
    def is_allocated(self):
        if self.server is not None:
            return self in self.server
        return False

    @property
    def is_playing(self):
        return self._is_playing

    @property
    def is_running(self):
        return self.server is not None

    @property
    def node_id(self):
        return self._node_id

    @property
    def node_id_is_permanent(self):
        return self._node_id_is_permanent

    @property
    def parent(self):
        return self._parent
