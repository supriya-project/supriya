# -*- encoding: utf-8 -*-
from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class BufferCloseRequest(Request):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_buffer_id',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        ):
        self._buffer_id = buffer_id

    ### PUBLIC METHODS ###

    def to_osc_message(self):
        request_id = int(self.request_id)
        buffer_id = int(self.buffer_id)
        message = osctools.OscMessage(
            request_id,
            buffer_id,
            )
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def response_prototype(self):
        return None

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.BUFFER_CLOSE