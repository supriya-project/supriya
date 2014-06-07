# -*- encoding: utf-8 -*-
from supriya.library.controllib.ServerObjectProxy import ServerObjectProxy


class Node(ServerObjectProxy):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_group',
        '_is_playing',
        '_is_running',
        '_node_id',
        '_server',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        node_id=None,
        server=None,
        ):
        from supriya.library import controllib
        server = server or controllib.Server()
        if node_id is None:
            node_id = server.next_node_id
        self._group = None
        self._is_playing = False
        self._is_running = False
        self._node_id = int(node_id)
        self._server = server

    ### PUBLIC METHODS ###

    @staticmethod
    def expr_as_node_id(expr):
        from supriya.library import controllib
        if isinstance(expr, controllib.Server):
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
        from supriya.library import controllib
        if expr is None:
            return Node.expr_as_target(controllib.Server())
        elif isinstance(expr, Node):
            return expr
        elif isinstance(expr, int):
            return controllib.Group(
                node_id=expr,
                server=controllib.Server(),
                send_to_server=True,
                )
        elif isinstance(expr, controllib.Server):
            return expr.default_group
        raise TypeError(expr)

    def free(self, send_to_server=True):
        message = self.make_free_message()
        if send_to_server:
            self.server.send_message(message)
        self._group = None
        self._is_playing = False
        self._is_running = False

    def make_free_message(self):
        message = (11, self.node_id)
        return message

    def make_query_message(self):
        message = (46, self.node_id)
        return message

    def make_run_message(self, should_run=True):
        message = (12, self.node_id, int(should_run))
        return message

    def make_set_message(self, **kwargs):
        message = (15, self.node_id)
        for key, value in kwargs.items():
            message += (key, value)
        return message

    def make_trace_message(self):
        message = (10, self.node_id)
        return message

    def query(self):
        message = self.make_query_message()
        self.server.send_message(message)

    def run(self, should_run=True):
        message = self.make_run_message(should_run=should_run)
        self.server.send_message(message)

    def set(self, **kwargs):
        message = self.make_set_message(**kwargs)
        self.server.send_message(message)

    def trace(self):
        message = self.make_trace_message()
        self.server.send_message(message)

    ### PUBLIC PROPERTIES ###

    @property
    def group(self):
        return self._group

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
    def server(self):
        return self._server
