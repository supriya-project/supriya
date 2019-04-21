import supriya.osc
from supriya.commands.Request import Request
from supriya.enums import RequestId


class BufferCloseRequest(Request):
    """
    A /b_close request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferCloseRequest(
        ...     buffer_id=23,
        ...     )
        >>> request
        BufferCloseRequest(
            buffer_id=23,
            )

    ::

        >>> message = request.to_osc()
        >>> message
        OscMessage(33, 23)

    ::

        >>> message.address == supriya.RequestId.BUFFER_CLOSE
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_buffer_id",)

    request_id = RequestId.BUFFER_CLOSE

    ### INITIALIZER ###

    def __init__(self, buffer_id=None):
        Request.__init__(self)
        self._buffer_id = int(buffer_id)

    ### PUBLIC METHODS ###

    def to_osc(self, with_request_name=False):
        if with_request_name:
            request_id = self.request_name
        else:
            request_id = int(self.request_id)
        buffer_id = int(self.buffer_id)
        message = supriya.osc.OscMessage(request_id, buffer_id)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def response_patterns(self):
        return ["/done", "/b_close", self.buffer_id], None
