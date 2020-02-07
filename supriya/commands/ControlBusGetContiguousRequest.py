import supriya.osc
from supriya.commands.Request import Request
from supriya.enums import RequestId


class ControlBusGetContiguousRequest(Request):
    """
    A /c_getn request.

    ::

        >>> import supriya
        >>> server = supriya.Server.default().boot()
        >>> request = supriya.commands.ControlBusGetContiguousRequest(
        ...     index_count_pairs=[
        ...         (0, 2),
        ...         (4, 1),
        ...         (8, 2),
        ...         (12, 1),
        ...         ],
        ...     )
        >>> request
        ControlBusGetContiguousRequest(
            index_count_pairs=(
                (0, 2),
                (4, 1),
                (8, 2),
                (12, 1),
                ),
            )

    ::

        >>> request.to_osc(with_request_name=True)
        OscMessage('/c_getn', 0, 2, 4, 1, 8, 2, 12, 1)

    ::

        >>> with server.osc_protocol.capture() as transcript:
        ...     request.communicate(server=server)
        ...
        ControlBusSetContiguousResponse(
            items=(
                Item(bus_values=(0.0, 0.0), starting_bus_id=0),
                Item(bus_values=(0.0,), starting_bus_id=4),
                Item(bus_values=(0.0, 0.0), starting_bus_id=8),
                Item(bus_values=(0.0,), starting_bus_id=12),
                ),
            )

    ::

        >>> for entry in transcript:
        ...     (entry.label, entry.message)
        ...
        ('S', OscMessage('/c_getn', 0, 2, 4, 1, 8, 2, 12, 1))
        ('R', OscMessage('/c_setn', 0, 2, 0.0, 0.0, 4, 1, 0.0, 8, 2, 0.0, 0.0, 12, 1, 0.0))

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_index_count_pairs",)

    request_id = RequestId.CONTROL_BUS_GET_CONTIGUOUS

    ### INITIALIZER ###

    def __init__(self, index_count_pairs=None):
        Request.__init__(self)
        if index_count_pairs:
            pairs = []
            for index, count in index_count_pairs:
                index = int(index)
                count = int(count)
                assert 0 <= index
                assert 0 < count
                pair = (index, count)
                pairs.append(pair)
            index_count_pairs = tuple(pairs)
        self._index_count_pairs = index_count_pairs

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False, with_request_name=False):
        if with_request_name:
            request_id = self.request_name
        else:
            request_id = int(self.request_id)
        contents = [request_id]
        if self.index_count_pairs:
            for pair in self.index_count_pairs:
                contents.extend(pair)
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def index_count_pairs(self):
        return self._index_count_pairs

    @property
    def response_patterns(self):
        return ["/c_setn"], None
