# -*- encoding: utf-8 -*-
from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class BufferQueryRequest(Request):
    r'''A /b_query request.

    ::

        >>> from supriya.tools import requesttools
        >>> request = requesttools.BufferQueryRequest(
        ...     buffer_ids=(1, 23, 41)
        ...     )
        >>> request
        BufferQueryRequest(
            buffer_ids=(1, 23, 41)
            )

    ::

        >>> message = request.to_osc_message()
        >>> message
        OscMessage(47, 1, 23, 41)

    ::

        >>> message.address == requesttools.RequestId.BUFFER_QUERY
        True

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_buffer_ids',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_ids=None,
        ):
        Request.__init__(self)
        if buffer_ids:
            buffer_ids = tuple(int(buffer_id) for buffer_id in buffer_ids)
        self._buffer_ids = buffer_ids

    ### PUBLIC METHODS ###

    def to_osc_message(self):
        request_id = int(self.request_id)
        contents = [
            request_id,
            ]
        for buffer_id in self.buffer_ids:
            contents.append(buffer_id)
        message = osctools.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_ids(self):
        return self._buffer_ids

    @property
    def response_specification(self):
        return None

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.BUFFER_QUERY