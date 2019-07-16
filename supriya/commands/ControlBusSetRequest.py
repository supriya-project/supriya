import supriya.osc
from supriya.commands.Request import Request
from supriya.enums import RequestId


class ControlBusSetRequest(Request):
    """
    A /c_set request.

    ::

        >>> import supriya
        >>> server = supriya.Server.default().boot()
        >>> request = supriya.commands.ControlBusSetRequest(
        ...     index_value_pairs=[
        ...         (0, 0.1),
        ...         (1, 0.2),
        ...         (2, 0.3),
        ...         (3, 0.4),
        ...         ],
        ...     )
        >>> request
        ControlBusSetRequest(
            index_value_pairs=(
                (0, 0.1),
                (1, 0.2),
                (2, 0.3),
                (3, 0.4),
                ),
            )

    ::

        >>> request.to_osc(with_request_name=True)
        OscMessage('/c_set', 0, 0.1, 1, 0.2, 2, 0.3, 3, 0.4)

    ::

        >>> with server.osc_io.capture() as transcript:
        ...     request.communicate(server=server)
        ...     _ = server.sync()
        ...

    ::

        >>> for entry in transcript:
        ...     (entry.label, entry.message)
        ...
        ('S', OscMessage(25, 0, 0.1, 1, 0.2, 2, 0.3, 3, 0.4))
        ('S', OscMessage(52, 0))
        ('R', OscMessage('/synced', 0))


    """

    ### CLASS VARIABLES ###

    __slots__ = ("_index_value_pairs",)

    request_id = RequestId.CONTROL_BUS_SET

    ### INITIALIZER ###

    def __init__(self, index_value_pairs=None):
        Request.__init__(self)
        if index_value_pairs:
            pairs = []
            for index, value in index_value_pairs:
                index = int(index)
                value = float(value)
                assert 0 <= index
                pair = (index, value)
                pairs.append(pair)
            index_value_pairs = tuple(pairs)
        self._index_value_pairs = index_value_pairs

    ### PRIVATE METHODS ###

    def _apply_local(self, server):
        for bus_id, value in self.index_value_pairs or ():
            bus_proxy = server._get_control_bus_proxy(bus_id)
            bus_proxy._value = value

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False, with_request_name=False):
        if with_request_name:
            request_id = self.request_name
        else:
            request_id = int(self.request_id)
        contents = [request_id]
        if self.index_value_pairs:
            for pair in self.index_value_pairs:
                contents.extend(pair)
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def index_value_pairs(self):
        return self._index_value_pairs
