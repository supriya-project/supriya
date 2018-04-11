import supriya.osc
from supriya.commands.Request import Request


class NodeMapToControlBusRequest(Request):
    """
    A /n_map request.

    ::

        >>> import supriya.commands
        >>> import supriya.realtime
        >>> request = supriya.commands.NodeMapToControlBusRequest(
        ...     node_id=1000,
        ...     frequency=supriya.realtime.Bus(9, 'control'),
        ...     phase=supriya.realtime.Bus(10, 'control'),
        ...     amplitude=supriya.realtime.Bus(11, 'control'),
        ...     )
        >>> request
        NodeMapToControlBusRequest(
            amplitude=11,
            frequency=9,
            node_id=1000,
            phase=10,
            )

    ::

        >>> message = request.to_osc_message()
        >>> message
        OscMessage(14, 1000, 'amplitude', 11, 'frequency', 9, 'phase', 10)

    ::

        >>> message.address == supriya.commands.RequestId.NODE_MAP_TO_CONTROL_BUS
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_kwargs',
        '_node_id',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        node_id=None,
        **kwargs
        ):
        Request.__init__(self)
        self._node_id = node_id
        self._kwargs = dict(
            (name, int(value))
            for name, value in kwargs.items()
            )

    ### SPECIAL METHODS ###

    def __getattr__(self, name):
        if name in self._kwargs:
            return self._kwargs[name]
        return object.__getattr__(self, name)

    ### PUBLIC METHODS ###

    def to_osc_message(self, with_textual_osc_command=False):
        if with_textual_osc_command:
            request_id = self.request_command
        else:
            request_id = int(self.request_id)
        node_id = int(self.node_id)
        contents = []
        for name, bus in sorted(self._kwargs.items()):
            contents.append(name)
            contents.append(int(bus))
        message = supriya.osc.OscMessage(
            request_id,
            node_id,
            *contents
            )
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def node_id(self):
        return self._node_id

    @property
    def response_specification(self):
        return None

    @property
    def request_id(self):
        import supriya.commands
        return supriya.commands.RequestId.NODE_MAP_TO_CONTROL_BUS
