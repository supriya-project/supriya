import supriya.osc
from supriya.commands.Request import Request


class NodeSetRequest(Request):
    """
    A /n_set request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.NodeSetRequest(
        ...     1000,
        ...     frequency=443.1,
        ...     phase=0.5,
        ...     amplitude=0.1,
        ...     )
        >>> request
        NodeSetRequest(
            amplitude=0.1,
            frequency=443.1,
            node_id=1000,
            phase=0.5,
            )

    ::

        >>> message = request.to_osc()
        >>> message
        OscMessage(15, 1000, 'amplitude', 0.1, 'frequency', 443.1, 'phase', 0.5)

    ::

        >>> message.address == supriya.commands.RequestId.NODE_SET
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_kwargs',
        '_node_id',
        )

    ### INITIALIZER ###

    def __init__(self, node_id=None, **kwargs):
        Request.__init__(self)
        self._node_id = node_id
        self._kwargs = kwargs

    ### SPECIAL METHODS ###

    def __getattr__(self, name):
        if name in self._kwargs:
            return self._kwargs[name]
        return object.__getattr__(self, name)

    ### PUBLIC METHODS ###

    def to_osc(self, with_textual_osc_command=False):
        if with_textual_osc_command:
            request_id = self.request_command
        else:
            request_id = int(self.request_id)
        node_id = int(self.node_id)
        contents = [
            request_id,
            node_id,
            ]
        for key, value in sorted(self._kwargs.items()):
            contents.append(key)
            contents.append(value)
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def node_id(self):
        return self._node_id

    @property
    def request_id(self):
        import supriya.commands
        return supriya.commands.RequestId.NODE_SET
