import supriya.osc
from supriya.tools.requesttools.Request import Request


class BufferFreeRequest(Request):
    """
    A /b_free request.

    ::

        >>> from supriya.tools import requesttools
        >>> request = requesttools.BufferFreeRequest(
        ...     buffer_id=23,
        ...     )
        >>> request
        BufferFreeRequest(
            buffer_id=23,
            )

    ::

        >>> message = request.to_osc_message()
        >>> message
        OscMessage(32, 23)

    ::

        >>> message.address == requesttools.RequestId.BUFFER_FREE
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_buffer_id',
        '_completion_message',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        completion_message=None,
        ):
        Request.__init__(self)
        self._buffer_id = int(buffer_id)
        self._completion_message = self._coerce_completion_message_input(
            completion_message)

    ### PUBLIC METHODS ###

    def to_osc_message(self, with_textual_osc_command=False):
        if with_textual_osc_command:
            request_id = self.request_command
        else:
            request_id = int(self.request_id)
        buffer_id = int(self.buffer_id)
        contents = [
            request_id,
            buffer_id,
            ]
        self._coerce_completion_message_output(contents)
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def completion_message(self):
        return self._completion_message

    @property
    def response_specification(self):
        return None

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.BUFFER_FREE
