# -*- encoding: utf-8 -*-
import abc
from supriya.tools.servertools.ServerObjectProxy import ServerObjectProxy


class Node(ServerObjectProxy):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_is_playing',
        '_is_running',
        '_node_id',
        '_parent',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        ServerObjectProxy.__init__(self)
        self._parent = None
        self._is_playing = False
        self._is_running = False
        self._node_id = None

    ### PRIVATE METHODS ###

    def add_to_group_head(self, group):
        from supriya.tools import servertools
        assert isinstance(group, servertools.Group)
        assert self.server is None
        assert group.server is self.server

    def add_to_group_tail(self, group):
        from supriya.tools import servertools
        assert isinstance(group, servertools.Group)
        assert group.server is self.server
        assert self.server is not None and self.server.is_running

    def add_before_node(self, node):
        from supriya.tools import servertools
        assert isinstance(node, servertools.Node)
        assert not isinstance(node, servertools.RootNode)
        assert node.server is self.server
        assert self.server is not None and self.server.is_running

    def move_after_node(self, node):
        from supriya.tools import servertools
        assert isinstance(node, servertools.Node)
        assert not isinstance(node, servertools.RootNode)
        assert node.server is self.server
        assert self.server is not None and self.server.is_running

    def move_before_node(self, node):
        from supriya.tools import servertools
        assert isinstance(node, servertools.Node)
        assert not isinstance(node, servertools.RootNode)
        assert node.server is self.server
        assert self.server is not None and self.server.is_running

    def move_to_head_node(self, group):
        from supriya.tools import servertools
        assert isinstance(group, servertools.Group)
        assert group.server is self.server
        assert self.server is not None and self.server.is_running

    def move_to_tail_node(self, group):
        from supriya.tools import servertools
        assert isinstance(group, servertools.Group)
        assert group.server is self.server
        assert self.server is not None and self.server.is_running

    def add_after_node(self, node):
        from supriya.tools import servertools
        assert isinstance(node, servertools.Node)
        assert not isinstance(node, servertools.RootNode)
        assert node.server is self.server
        assert self.server is not None and self.server.is_running

    def replace_node(self, node):
        from supriya.tools import servertools
        assert isinstance(node, servertools.Node)
        assert not isinstance(node, servertools.RootNode)
        assert node.server is self.server
        assert self.server is not None and self.server.is_running

    ### PUBLIC METHODS ###

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
            return Node.expr_as_target(servertools.Server.get_default_server())
        elif isinstance(expr, servertools.Server):
            return expr.default_group
        elif isinstance(expr, Node):
            return expr
        elif isinstance(expr, int):
            raise NotImplementedError
        raise TypeError(expr)

    def free(self, send_to_server=True):
        message = self.make_free_message()
        if send_to_server:
            self.server.send_message(message)
        self._is_playing = False
        self._is_running = False
        self._node_id = None
        self._parent = None

    ### PUBLIC PROPERTIES ###

    @property
    def is_playing(self):
        return self._is_playing

    @property
    def is_running(self):
        return self._is_running

    @property
    def node_id(self):
        return self._node_id

    @property
    def parent(self):
        return self._parent
