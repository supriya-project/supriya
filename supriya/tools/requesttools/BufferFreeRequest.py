# -*- encoding: utf-8 -*-
from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class BufferFreeRequest(Request):

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
        self._buffer_id = buffer_id
        if completion_message is not None:
            prototype = (osctools.OscBundle, osctools.OscMessage)
            assert isinstance(completion_message, prototype)
        self._completion_message = completion_message

    ### PUBLIC METHODS ###

    def to_osc_message(self):
        request_id = int(self.request_id)
        buffer_id = int(self.buffer_id)
        contents = [
            request_id,
            buffer_id,
            ]
        if self.completion_message is not None:
            completion_message = self.completion_message.to_datagram()
            completion_message = bytearray(completion_message)
            contents.append(completion_message)
        message = osctools.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def completion_message(self):
        return self._completion_message

    @property
    def response_prototype(self):
        return None

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.BUFFER_FREE