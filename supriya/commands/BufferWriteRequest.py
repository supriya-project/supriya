import supriya.osc
from supriya.commands.Request import Request
from supriya.commands.RequestBundle import RequestBundle


class BufferWriteRequest(Request):
    """
    A /b_write request.

    ::

        >>> import supriya.commands
        >>> import supriya.soundfiles
        >>> request = supriya.commands.BufferWriteRequest(
        ...     buffer_id=23,
        ...     file_path='test.aiff',
        ...     header_format=supriya.soundfiles.HeaderFormat.AIFF,
        ...     sample_format=supriya.soundfiles.SampleFormat.INT24,
        ...     )
        >>> request
        BufferWriteRequest(
            buffer_id=23,
            file_path='test.aiff',
            frame_count=-1,
            header_format=HeaderFormat.AIFF,
            sample_format=SampleFormat.INT24,
            starting_frame=0,
            )

    ::

        >>> message = request.to_osc()
        >>> message # doctest: +SKIP
        OscMessage(31, 23, 'test.aiff', 'aiff', 'int24', -1, 0, 0)

    ::

        >>> message.address == supriya.commands.RequestId.BUFFER_WRITE
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_buffer_id',
        '_callback',
        '_file_path',
        '_frame_count',
        '_header_format',
        '_leave_open',
        '_sample_format',
        '_starting_frame',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        callback=None,
        file_path=None,
        frame_count=None,
        header_format='aiff',
        leave_open=False,
        sample_format='int24',
        starting_frame=None,
    ):
        import supriya.soundfiles
        Request.__init__(self)
        self._buffer_id = int(buffer_id)
        if callback is not None:
            assert isinstance(callback, (Request, RequestBundle))
        self._callback = callback
        self._file_path = str(file_path)
        if frame_count is None:
            frame_count = -1
        frame_count = int(frame_count)
        assert -1 <= frame_count
        self._frame_count = frame_count
        self._header_format = supriya.soundfiles.HeaderFormat.from_expr(
            header_format)
        self._leave_open = bool(leave_open)
        self._sample_format = supriya.soundfiles.SampleFormat.from_expr(
            sample_format)
        if starting_frame is None:
            starting_frame = 0
        starting_frame = int(starting_frame)
        assert 0 <= starting_frame
        self._starting_frame = starting_frame

    ### PUBLIC METHODS ###

    def to_osc(self, with_request_name=False):
        if with_request_name:
            request_id = self.request_name
        else:
            request_id = int(self.request_id)
        buffer_id = int(self.buffer_id)
        header_format = self.header_format.name.lower()
        sample_format = self.sample_format.name.lower()
        leave_open = int(bool(self.leave_open))
        contents = [
            request_id,
            buffer_id,
            self.file_path,
            header_format,
            sample_format,
            self.frame_count,
            self.starting_frame,
            leave_open,
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
    def callback(self):
        return self._callback

    @property
    def file_path(self):
        return self._file_path

    @property
    def frame_count(self):
        return self._frame_count

    @property
    def header_format(self):
        return self._header_format

    @property
    def leave_open(self):
        return self._leave_open

    @property
    def request_id(self):
        import supriya.commands
        return supriya.commands.RequestId.BUFFER_WRITE

    @property
    def sample_format(self):
        return self._sample_format

    @property
    def starting_frame(self):
        return self._starting_frame
