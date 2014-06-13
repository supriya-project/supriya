from supriya.tools.servertools.Node import Node


class Synth(Node):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_synthdef',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        synthdef,
        ):
        from supriya.tools import synthdeftools
        assert isinstance(synthdef, synthdeftools.SynthDef)
        Node.__init__(self)
        self._synthdef = synthdef

    ### PUBLIC METHODS ###

    def allocate(
        self,
        add_action=None,
        target_node=None,
        **kwargs
        ):
        from supriya.tools import servertools
        add_action, node_id, target_node_id = Node.allocate(
            self,
            add_action=add_action,
            target_node=target_node,
            )
        message = servertools.CommandManager.make_synth_new_message(
            add_action=add_action,
            node_id=node_id,
            synthdef_name=self.synthdef.name,
            target_node_id=target_node_id,
            **kwargs
            )
        self.server.send_message(message)
        return self

    ### PUBLIC PROPERTIES ###

    @property
    def synthdef(self):
        return self._synthdef
