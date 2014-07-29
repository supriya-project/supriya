# -*- encoding: utf-8 -*-
from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class BufferGetRequest(Request):
    r'''A /b_get request.

    ::

        >>> from supriya.tools import requesttools
        >>> request = requesttools.BufferGetRequest(
        ...     buffer_id=23,
        ...     indices=(0, 4, 8, 16),
        ...     )
        >>> request
        BufferGetRequest(
            buffer_id=23,
            indices=(0, 4, 8, 16)
            )

    ::

        >>> message = request.to_osc_message()
        >>> message
        OscMessage(42, 23, 0, 4, 8, 16)

    ::

        >>> message.address == requesttools.RequestId.BUFFER_GET
        True

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_buffer_id',
        '_indices',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        indices=None,
        ):
        Request.__init__(self)
        self._buffer_id = buffer_id
        self._indices = tuple(int(index) for index in indices)

    ### PUBLIC METHODS ###

    def to_osc_message(self):
        request_id = int(self.request_id)
        buffer_id = int(self.buffer_id)
        contents = [
            request_id,
            buffer_id,
            ]
        if self.indices:
            for index in self.indices:
                contents.append(index)
        message = osctools.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def indices(self):
        return self._indices

    @property
    def response_specification(self):
        return None

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.BUFFER_GET