from supriya.library.controllib.Node import Node


class Group(Node):

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(
        self,
        add_action=None,
        node_id=None,
        send_to_server=True,
        server=None,
        target_node=None,
        ):
        from supriya.library import controllib
        if node_id not in (1, None):
            target_node = self.expr_as_target(target_node)
        else:
            target_node = self
        server = server or target_node.server
        add_action = add_action or 0
        add_action = controllib.AddAction.from_expr(add_action)
        Node.__init__(
            self,
            node_id=node_id,
            server=server,
            )
        if add_action.value < 2:
            self._group = target_node
        else:
            self._group = target_node.group
        message = (
            self.creation_command,
            self._group.node_id,
            add_action.value,
            target_node.node_id,
            )
        if send_to_server:
            self._server.send_message(message)

    ### PUBLIC PROPERTIES ###

    @property
    def creation_command(self):
        return 21
