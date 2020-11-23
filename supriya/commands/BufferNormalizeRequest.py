import supriya.osc
from .bases import Request
from supriya.enums import RequestId


class BufferNormalizeRequest(Request):
    """
    A `/b_gen normalize` request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferNormalizeRequest(
        ...     buffer_id=23,
        ...     )
        >>> print(request)
        BufferNormalizeRequest(
            buffer_id=23,
            )

    ::

        >>> request.to_osc()
        OscMessage('/b_gen', 23, 'normalize', 1.0)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.BUFFER_GENERATE

    ### INITIALIZER ###

    def __init__(self, as_wavetable=None, buffer_id=None, new_maximum=1.0):
        Request.__init__(self)
        if as_wavetable is not None:
            as_wavetable = bool(as_wavetable)
        self._as_wavetable = as_wavetable
        self._buffer_id = int(buffer_id)
        self._new_maximum = float(new_maximum)

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        buffer_id = int(self.buffer_id)
        command_name = "normalize"
        if self.as_wavetable:
            command_name = "wnormalize"
        contents = [request_id, buffer_id, command_name, self.new_maximum]
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def as_wavetable(self):
        return self._as_wavetable

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def new_maximum(self):
        return self._new_maximum

    @property
    def response_patterns(self):
        return ["/done", "/b_gen", self.buffer_id], None
