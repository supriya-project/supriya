import supriya.osc
from supriya.commands.Request import Request
from supriya.commands.RequestId import RequestId


class ControlBusGetRequest(Request):
    """
    A /c_get request.

    ::

        >>> import supriya
        >>> server = supriya.Server().boot()
        >>> request = supriya.commands.ControlBusGetRequest(
        ...     indices=(0, 4, 8, 12),
        ...     )
        >>> request
        ControlBusGetRequest(
            indices=(0, 4, 8, 12),
            )

    ::

        >>> request.to_osc(True)
        OscMessage('/c_get', 0, 4, 8, 12)

    ::

        >>> with server.osc_io.capture() as transcript:
        ...     request.communicate(server=server)
        ...
        ControlBusSetResponse(
            items=(
                Item(bus_id=0, bus_value=0.0),
                Item(bus_id=4, bus_value=0.0),
                Item(bus_id=8, bus_value=0.0),
                Item(bus_id=12, bus_value=0.0),
                ),
            )

    ::

        >>> for entry in transcript:
        ...     entry
        ...
        ('S', OscMessage(40, 0, 4, 8, 12))
        ('R', OscMessage('/c_set', 0, 0.0, 4, 0.0, 8, 0.0, 12, 0.0))

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_indices",)

    request_id = RequestId.CONTROL_BUS_GET

    ### INITIALIZER ###

    def __init__(self, indices=None):
        Request.__init__(self)
        if indices:
            indices = tuple(int(index) for index in indices)
            assert all(0 <= index for index in indices)
        self._indices = indices

    ### PUBLIC METHODS ###

    def to_osc(self, with_request_name=False):
        if with_request_name:
            request_id = self.request_name
        else:
            request_id = int(self.request_id)
        contents = [request_id]
        if self.indices:
            contents.extend(self.indices)
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def indices(self):
        return self._indices

    @property
    def response_patterns(self):
        return [["/c_set"]]
