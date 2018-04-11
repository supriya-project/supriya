import supriya.osc
from supriya.commands.Request import Request


class BufferZeroRequest(Request):
    """
    A /b_zero request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferZeroRequest(
        ...     buffer_id=23,
        ...     )
        >>> request
        BufferZeroRequest(
            buffer_id=23,
            )

    ::

        >>> message = request.to_osc_message()
        >>> message
        OscMessage(34, 23)

    ::

        >>> message.address == supriya.commands.RequestId.BUFFER_ZERO
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
        completion_message=None
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
        import supriya.commands
        return {
            supriya.commands.DoneResponse: {
                'action': ('/b_zero', self.buffer_id),
                },
            }

    @property
    def request_id(self):
        import supriya.commands
        return supriya.commands.RequestId.BUFFER_ZERO
