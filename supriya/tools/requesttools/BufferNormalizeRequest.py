from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class BufferNormalizeRequest(Request):
    """
    A `/b_gen normalize` request.

    ::

        >>> from supriya.tools import requesttools
        >>> request = requesttools.BufferNormalizeRequest(
        ...     buffer_id=23,
        ...     )
        >>> print(request)
        BufferNormalizeRequest(
            buffer_id=23,
            )

    ::

        >>> message = request.to_osc_message()
        >>> message
        OscMessage(38, 23, 'normalize', 1.0)

    ::

        >>> message.address == requesttools.RequestId.BUFFER_GENERATE
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_as_wavetable',
        '_buffer_id',
        '_new_maximum',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        as_wavetable=None,
        buffer_id=None,
        new_maximum=1.0,
        ):
        Request.__init__(self)
        if as_wavetable is not None:
            as_wavetable = bool(as_wavetable)
        self._as_wavetable = as_wavetable
        self._buffer_id = int(buffer_id)
        self._new_maximum = float(new_maximum)

    ### PUBLIC METHODS ###

    def to_osc_message(self, with_textual_osc_command=False):
        if with_textual_osc_command:
            request_id = self.request_command
        else:
            request_id = int(self.request_id)
        buffer_id = int(self.buffer_id)
        command_name = 'normalize'
        if self.as_wavetable:
            command_name = 'wnormalize'
        contents = [
            request_id,
            buffer_id,
            command_name,
            self.new_maximum,
            ]
        message = osctools.OscMessage(*contents)
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
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.BUFFER_GENERATE

    @property
    def response_specification(self):
        from supriya.tools import responsetools
        return {
            responsetools.DoneResponse: {
                'action': ('/b_gen', self.buffer_id),
                },
            }
