import supriya.osc
from supriya.commands.Request import Request
from supriya.commands.RequestBundle import RequestBundle


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

        >>> message = request.to_osc()
        >>> message
        OscMessage(32, 23)

    ::

        >>> message.address == supriya.commands.RequestId.BUFFER_FREE
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_buffer_id',
        '_callback',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        callback=None,
    ):
        Request.__init__(self)
        self._buffer_id = int(buffer_id)
        if callback is not None:
            assert isinstance(callback, (Request, RequestBundle))
        self._callback = callback

    ### PUBLIC METHODS ###

    def to_osc(self, with_textual_osc_command=False):
        if with_textual_osc_command:
            request_id = self.request_command
        else:
            request_id = int(self.request_id)
        buffer_id = int(self.buffer_id)
        contents = [
            request_id,
            buffer_id,
            ]
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

    @property
    def request_id(self):
        import supriya.commands
        return supriya.commands.RequestId.BUFFER_FREE
