import supriya.osc
from supriya.commands.Request import Request
from supriya.commands.RequestId import RequestId


class ControlBusSetContiguousRequest(Request):
    """
    A /c_setn request.

    ::

        >>> import supriya
        >>> server = supriya.Server().boot()
        >>> request = supriya.commands.ControlBusSetContiguousRequest(
        ...     index_values_pairs=[
        ...         (0, (0.1, 0.2, 0.3)),
        ...         (4, (0.4, 0.5, 0.6)),
        ...         ],
        ...     )
        >>> request
        ControlBusSetContiguousRequest(
            index_values_pairs=(
                (0, (0.1, 0.2, 0.3)),
                (4, (0.4, 0.5, 0.6)),
                ),
            )

    ::

        >>> request.to_osc(True)
        OscMessage('/c_setn', 0, 3, 0.1, 0.2, 0.3, 4, 3, 0.4, 0.5, 0.6)

    ::

        >>> with server.osc_io.capture() as transcript:
        ...     request.communicate(server=server)
        ...     _ = server.sync()
        ...

    ::

        >>> for entry in transcript:
        ...     entry
        ...
        ('S', OscMessage(26, 0, 3, 0.1, 0.2, 0.3, 4, 3, 0.4, 0.5, 0.6))
        ('S', OscMessage(52, 0))
        ('R', OscMessage('/synced', 0))

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_index_values_pairs",)

    request_id = RequestId.CONTROL_BUS_SET_CONTIGUOUS

    ### INITIALIZER ###

    def __init__(self, index_values_pairs=None):
        Request.__init__(self)
        if index_values_pairs:
            pairs = []
            for index, values in index_values_pairs:
                index = int(index)
                values = tuple(float(value) for value in values)
                assert 0 <= index
                assert values
                if not values:
                    continue
                pair = (index, values)
                pairs.append(pair)
            index_values_pairs = tuple(pairs)
        self._index_values_pairs = index_values_pairs

    ### PRIVATE METHODS ###

    def _apply_local(self, server):
        for starting_bus_index, values in self._index_values_pairs or ():
            for i, value in enumerate(values):
                bus_id = starting_bus_index + i
                bus_proxy = server._get_control_bus_proxy(bus_id)
                bus_proxy._value = value

    ### PUBLIC METHODS ###

    def to_osc(self, with_request_name=False):
        if with_request_name:
            request_id = self.request_name
        else:
            request_id = int(self.request_id)
        contents = [request_id]
        if self.index_values_pairs:
            for index, values in self.index_values_pairs:
                contents.append(index)
                contents.append(len(values))
                contents.extend(values)
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def index_values_pairs(self):
        return self._index_values_pairs
