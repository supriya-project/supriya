import supriya.osc
from .bases import Request
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

        >>> request.to_osc()
        OscMessage('/b_close', 23)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.BUFFER_CLOSE

    ### INITIALIZER ###

    def __init__(self, buffer_id=None):
        Request.__init__(self)
        self._buffer_id = int(buffer_id)

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
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
