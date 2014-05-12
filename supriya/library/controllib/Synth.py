from supriya.library.controllib.Node import Node


class Synth(Node):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_synthdef_name',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        synthdef_name,
        add_action=None,
        target_node=None,
        ):
        from supriya.library import controllib
        self._synthdef_name = synthdef_name
        add_action = controllib.Node.AddAction(add_action)
        target_node = controllib.Node.expr_to_target_node(target_node)
        server = target_node.server
        Node.__init__(
            self,
            server=server,
            )
        if add_action.value < 2:
            self._group = target_node
        else:
            self._group = target_node.group
        message = (
            9,
            's_new',
            self.synthdef_name,
            self.node_id,
            self.add_action.value,
            self.target_node.node_id,
            )
        self._server.send_message(*message)

    ### PUBLIC PROPERTIES ###

    @property
    def synthdef_name(self):
        return self._synthdef_name
