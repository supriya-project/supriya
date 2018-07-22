import supriya.osc
from supriya.commands.Request import Request
from supriya.commands.RequestBundle import RequestBundle
from supriya.commands.RequestId import RequestId


class BufferAllocateRequest(Request):
    """
    A /b_alloc request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferAllocateRequest(
        ...     buffer_id=23,
        ...     frame_count=512,
        ...     channel_count=2,
        ...     )
        >>> request
        BufferAllocateRequest(
            buffer_id=23,
            channel_count=2,
            frame_count=512,
            )

    ::

        >>> message = request.to_osc()
        >>> message
        OscMessage(28, 23, 512, 2)

    ::

        >>> message.address == supriya.commands.RequestId.BUFFER_ALLOCATE
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_buffer_id',
        '_channel_count',
        '_callback',
        '_frame_count',
        )

    request_id = RequestId.BUFFER_ALLOCATE

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        frame_count=None,
        channel_count=None,
        callback=None,
    ):
        Request.__init__(self)
        self._buffer_id = int(buffer_id)
        self._frame_count = frame_count
        if channel_count is not None:
            channel_count = int(channel_count)
            assert 0 < channel_count
        self._channel_count = channel_count
        if callback is not None:
            assert isinstance(callback, (Request, RequestBundle))
        self._callback = callback

    ### PUBLIC METHODS ###

    def to_osc(self, with_request_name=False):
        if with_request_name:
            request_id = self.request_name
        else:
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
        if self.callback:
            contents.append(self.callback.to_osc())
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def channel_count(self):
        return self._channel_count

    @property
    def callback(self):
        return self._callback

    @property
    def frame_count(self):
        return self._frame_count

    @property
    def response_patterns(self):
        return [['/done', '/b_alloc', self.buffer_id]]
