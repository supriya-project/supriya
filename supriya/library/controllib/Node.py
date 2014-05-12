import enum


class Node(object):

    ### CLASS VARIABLES ###

    class AddAction(enum.IntEnum):
        ADD_TO_HEAD = 0
        ADD_TO_TAIL = 1
        ADD_BEFORE = 2
        ADD_AFTER = 3
        ADD_REPLACE = 4

    __slots__ = (
        '_group',
        '_is_playing',
        '_is_running',
        '_node_id',
        '_server',
        )

    ### INITIALIZER ###

    def __init__(self, node_id=None, server=None):
        from supriya.library import controllib
        server = server or controllib.Server()
        if node_id is None:
            node_id = server.next_node_id()
        self._group = None
        self._is_playing = False
        self._is_running = False
        self._node_id = int(node_id)
        self._server = server

    ### PUBLIC METHODS ###

    @staticmethod
    def expr_to_node_id(expr):
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
    def expr_to_target(expr):
        from supriya.library import controllib
        if isinstance(expr, (controllib.Server, type(None))):
            return controllib.Group(
                node_id=1,
                server=expr,
                )
        elif isinstance(expr, Node):
            return expr
        elif isinstance(expr, int):
            return controllib.Group(
                node_id=expr,
                server=controllib.Server(),
                )
        raise TypeError(expr)

    def free(self):
        message = [11, self.node_id]
        self.server.send_message(*message)
        self._group = None
        self._is_playing = False
        self._is_running = False

    def run(self):
        message = [12, self.node_id, 0x1]
        self.server.send_message(*message)

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
