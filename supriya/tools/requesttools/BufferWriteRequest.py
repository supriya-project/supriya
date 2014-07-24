# -*- encoding: utf-8 -*-
from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class BufferWriteRequest(Request):
    r'''A /b_write request.

    ::

        >>> from supriya.tools import requesttools
        >>> from supriya.tools import soundfiletools
        >>> request = requesttools.BufferWriteRequest(
        ...     buffer_id=23,
        ...     file_path='test.aiff',
        ...     header_format=soundfiletools.HeaderFormat.AIFF,
        ...     sample_format=soundfiletools.SampleFormat.INT24,
        ...     )
        >>> request
        BufferWriteRequest(
            buffer_id=23,
            file_path='test.aiff',
            frame_count=-1,
            header_format=<HeaderFormat.AIFF: 0>,
            leave_open=False,
            sample_format=<SampleFormat.INT24: 0>,
            starting_frame=0
            )

    ::
        >>> message = request.to_osc_message()
        >>> message
        OscMessage(31, 23, 'test.aiff', 'aiff', 'int24', -1, 0, 0)

    ::

        >>> message.address == requesttools.RequestId.BUFFER_WRITE
        True

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_buffer_id',
        '_completion_message',
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
        completion_message=None,
        file_path=None,
        frame_count=None,
        header_format='aiff',
        leave_open=False,
        sample_format='int24',
        starting_frame=None,
        ):
        from supriya.tools import soundfiletools
        self._buffer_id = buffer_id
        self._completion_message = self._coerce_completion_message_input(
            completion_message)
        self._file_path = str(file_path)
        if frame_count is None:
            frame_count = -1
        frame_count = int(frame_count)
        assert -1 <= frame_count
        self._frame_count = frame_count
        self._header_format = soundfiletools.HeaderFormat.from_expr(
            header_format)
        self._leave_open = bool(leave_open)
        self._sample_format = soundfiletools.SampleFormat.from_expr(
            sample_format)
        if starting_frame is None:
            starting_frame = 0
        starting_frame = int(starting_frame)
        assert 0 <= starting_frame
        self._starting_frame = starting_frame

    ### PUBLIC METHODS ###

    def to_osc_message(self):
        request_id = int(self.request_id)
        buffer_id = int(self.buffer_id)
        file_path = str(self.file_path)
        header_format = self.header_format.name.lower()
        sample_format = self.sample_format.name.lower()
        leave_open = int(self.leave_open)
        contents = [
            request_id,
            buffer_id,
            file_path,
            header_format,
            sample_format,
            self.frame_count,
            self.starting_frame,
            leave_open,
            ]
        self._coerce_completion_message_output(contents)
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
    def response_prototype(self):
        return None

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.BUFFER_WRITE

    @property
    def sample_format(self):
        return self._sample_format

    @property
    def starting_frame(self):
        return self._starting_frame