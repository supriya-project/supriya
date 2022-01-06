from collections.abc import Sequence

import supriya.osc
from supriya import AddAction
from supriya.enums import RequestId
from supriya.realtime.nodes import Node, Synth

from .bases import Request, Response


class SynthInfoResponse(Response):

    ### INITIALIZER ###

    def __init__(self, node_id, synthdef_name, **synthdef_controls):
        self.node_id = node_id
        self.synthdef_name = synthdef_name
        self.synthdef_controls = synthdef_controls

    @classmethod
    def from_osc_message(cls, osc_message):
        contents = list(osc_message.contents)
        node_id = contents.pop(0)
        synthdef_name = contents.pop(0)
        pair_count = contents.pop(0)
        kwargs = {}
        for i in range(pair_count):
            kwargs[contents[i * 2]] = contents[i * 2 + 1]
        return cls(node_id=node_id, synthdef_name=synthdef_name, **kwargs)


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
            node_id=node_id,
            node_id_is_permanent=synth.node_id_is_permanent,
            server=server,
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


class SynthQueryRequest(Request):
    """
    A /s_query request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.SynthQueryRequest(1000)
        >>> request
        SynthQueryRequest(
            node_ids=(1000,),
        )

    ::

        >>> request.to_osc()
        OscMessage('/s_query', 1000)

    ::

        >>> server = supriya.Server().boot()
        >>> synth = supriya.Synth().allocate(server)
        >>> request.communicate(server)
        SynthInfoResponse(
            1000,
            'default',
            amplitude=0.100...,
            frequency=440.0,
            gate=1.0,
            out=0.0,
            pan=0.5,
        )

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.SYNTH_QUERY

    ### INITIALIZER ###

    def __init__(self, node_ids=None):
        Request.__init__(self)
        if not isinstance(node_ids, Sequence):
            node_ids = (node_ids,)
        node_ids = tuple(int(_) for _ in node_ids)
        self._node_ids = node_ids

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        contents = [self.request_name, *self.node_ids]
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def node_ids(self):
        return self._node_ids

    @property
    def response_patterns(self):
        return ["/s_info", int(self.node_ids[-1])], None


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
