from supriya import AddAction
from supriya.enums import RequestId

from .bases import Request, Response


class SynthNewRequest(Request):
    """
    A /s_new request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.SynthNewRequest(
        ...     add_action=supriya.AddAction.ADD_TO_TAIL,
        ...     node_id=1001,
        ...     synthdef="test",
        ...     target_node_id=1000,
        ...     frequency=443,
        ...     phase=0.2,
        ... )
        >>> request
        SynthNewRequest(
            add_action=AddAction.ADD_TO_TAIL,
            frequency=443,
            node_id=1001,
            phase=0.2,
            synthdef='test',
            target_node_id=1000,
        )

    ::

        >>> request.to_osc()
        OscMessage('/s_new', 'test', 1001, 1, 1000, 'frequency', 443, 'phase', 0.2)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.SYNTH_NEW

    ### INITIALIZER ###

    def __init__(
        self,
        add_action=None,
        node_id=None,
        synthdef=None,
        target_node_id=None,
        **kwargs,
    ):
        import supriya.synthdefs

        Request.__init__(self)
        self._add_action = AddAction.from_expr(add_action)
        self._node_id = node_id
        prototype = (str, supriya.synthdefs.SynthDef)
        assert isinstance(synthdef, prototype)
        self._synthdef = synthdef
        self._target_node_id = target_node_id
        self._kwargs = tuple(sorted(kwargs.items()))

    ### PRIVATE METHODS ###

    def _apply_local(self, server):
        from supriya.realtime import Node, Synth

        if isinstance(self.node_id, Synth):
            node_id = None
            synth = self.node_id
        else:
            node_id = self.node_id
            synth = Synth(synthdef=self.synthdef, **dict(self.kwargs))
        if isinstance(self.target_node_id, Node):
            target_node = self.target_node_id
        else:
            target_node = server._nodes[self.target_node_id]
        synth._register_with_local_server(
            server, node_id=node_id, node_id_is_permanent=synth.node_id_is_permanent
        )
        target_node._move_node(add_action=self.add_action, node=synth)

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        import supriya.synthdefs

        request_id = self.request_name
        synthdef = self.synthdef
        if isinstance(synthdef, supriya.synthdefs.SynthDef):
            synthdef = synthdef.actual_name
        node_id = self._sanitize_node_id(self.node_id, with_placeholders)
        add_action = int(self.add_action)
        target_node_id = self._sanitize_node_id(self.target_node_id, with_placeholders)
        if not isinstance(target_node_id, int) and with_placeholders:
            target_node_id = -1
        contents = [request_id, synthdef, node_id, add_action, target_node_id]
        for key, value in self._kwargs:
            contents.append(key)
            contents.append(value)
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def add_action(self):
        return self._add_action

    @property
    def kwargs(self):
        return self._kwargs

    @property
    def node_id(self):
        return self._node_id

    @property
    def response_patterns(self):
        return ["/n_go", int(self.node_id)], None

    @property
    def synthdef(self):
        return self._synthdef

    @property
    def target_node_id(self):
        return self._target_node_id


class TriggerResponse(Response):

    ### INITIALIZER ###

    def __init__(self, node_id=None, trigger_id=None, trigger_value=None):
        self._node_id = node_id
        self._trigger_id = trigger_id
        self._trigger_value = trigger_value

    ### PUBLIC METHODS ###

    @classmethod
    def from_osc_message(cls, osc_message):
        arguments = osc_message.contents
        response = cls(*arguments)
        return response

    ### PUBLIC PROPERTIES ###

    @property
    def node_id(self):
        return self._node_id

    @property
    def trigger_id(self):
        return self._trigger_id

    @property
    def trigger_value(self):
        return self._trigger_value
