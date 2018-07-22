import supriya.osc
from supriya.commands.Request import Request
from supriya.commands.RequestId import RequestId


class BufferCopyRequest(Request):
    """
    A `/b_gen copy` request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferCopyRequest(
        ...     source_buffer_id=23,
        ...     target_buffer_id=666,
        ...     )
        >>> print(request)
        BufferCopyRequest(
            source_buffer_id=23,
            target_buffer_id=666,
            )

    ::

        >>> message = request.to_osc()
        >>> message
        OscMessage(38, 666, 'copy', 0, 23, 0, -1)

    ::

        >>> message.address == supriya.commands.RequestId.BUFFER_GENERATE
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_frame_count',
        '_source_buffer_id',
        '_source_starting_frame',
        '_target_buffer_id',
        '_target_starting_frame',
        )

    request_id = RequestId.BUFFER_GENERATE

    ### INITIALIZER ###

    def __init__(
        self,
        frame_count=None,
        source_buffer_id=None,
        source_starting_frame=None,
        target_buffer_id=None,
        target_starting_frame=None,
    ):
        Request.__init__(self)
        self._source_buffer_id = int(source_buffer_id)
        self._target_buffer_id = int(target_buffer_id)
        if frame_count is not None:
            frame_count = int(frame_count)
            assert -1 <= frame_count
        self._frame_count = frame_count
        if source_starting_frame is not None:
            source_starting_frame = int(source_starting_frame)
            assert 0 <= source_starting_frame
        self._source_starting_frame = source_starting_frame
        if target_starting_frame is not None:
            target_starting_frame = int(target_starting_frame)
            assert 0 <= target_starting_frame
        self._target_starting_frame = target_starting_frame

    ### PUBLIC METHODS ###

    def to_osc(self, with_request_name=False):
        if with_request_name:
            request_id = self.request_name
        else:
            request_id = int(self.request_id)
        frame_count = self.frame_count
        if frame_count is None:
            frame_count = -1
        source_starting_frame = self.source_starting_frame
        if source_starting_frame is None:
            source_starting_frame = 0
        target_starting_frame = self.target_starting_frame
        if target_starting_frame is None:
            target_starting_frame = 0
        contents = [
            request_id,
            self.target_buffer_id,
            'copy',
            target_starting_frame,
            self.source_buffer_id,
            source_starting_frame,
            frame_count,
            ]
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def frame_count(self):
        return self._frame_count

    @property
    def response_patterns(self):
        return [['/done', '/b_gen', self.target_buffer_id]]

    @property
    def source_buffer_id(self):
        return self._source_buffer_id

    @property
    def source_starting_frame(self):
        return self._source_starting_frame

    @property
    def target_buffer_id(self):
        return self._target_buffer_id

    @property
    def target_starting_frame(self):
        return self._target_starting_frame
