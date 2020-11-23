import supriya.osc
from supriya.enums import RequestId

from .bases import Request, RequestBundle


class BufferFreeRequest(Request):
    """
    A /b_free request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferFreeRequest(
        ...     buffer_id=23,
        ...     )
        >>> request
        BufferFreeRequest(
            buffer_id=23,
            )

    ::

        >>> request.to_osc()
        OscMessage('/b_free', 23)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.BUFFER_FREE

    ### INITIALIZER ###

    def __init__(self, buffer_id=None, callback=None):
        Request.__init__(self)
        self._buffer_id = int(buffer_id)
        if callback is not None:
            assert isinstance(callback, (Request, RequestBundle))
        self._callback = callback

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        buffer_id = int(self.buffer_id)
        contents = [request_id, buffer_id]
        if self.callback:
            contents.append(self.callback.to_osc())
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def callback(self):
        return self._callback
