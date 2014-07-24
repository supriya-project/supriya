# -*- encoding: utf-8 -*-
from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class BufferAllocateRequest(Request):
    r'''A /b_alloc request.

    ::

        >>> from supriya.tools import requesttools
        >>> request = requesttools.BufferAllocateRequest(
        ...     buffer_id=23,
        ...     frame_count=512,
        ...     channel_count=2,
        ...     )
        >>> request
        BufferAllocateRequest(
            buffer_id=23,
            frame_count=512,
            channel_count=2
            )

    ::

        >>> message = request.to_osc_message()
        >>> message
        OscMessage(28, 23, 512, 2)

    ::

        >>> message.address == requesttools.RequestId.BUFFER_ALLOCATE
        True

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_buffer_id',
        '_frame_count',
        '_channel_count',
        '_completion_message',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        frame_count=None,
        channel_count=1,
        completion_message=None,
        ):
        self._buffer_id = buffer_id
        self._frame_count = frame_count
        self._channel_count = channel_count
        if completion_message is not None:
            prototype = (osctools.OscBundle, osctools.OscMessage)
            assert isinstance(completion_message, prototype)
        self._completion_message = completion_message

    ### PUBLIC METHODS ###

    def to_osc_message(self):
        request_id = int(self.request_id)
        buffer_id = int(self.buffer_id)
        frame_count = int(self.frame_count)
        channel_count = int(self.channel_count)
        contents = [
            request_id,
            buffer_id,
            frame_count,
            channel_count,
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
    def channel_count(self):
        return self._channel_count

    @property
    def completion_message(self):
        return self._completion_message

    @property
    def frame_count(self):
        return self._frame_count

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.BUFFER_ALLOCATE

    @property
    def response_prototype(self):
        return None