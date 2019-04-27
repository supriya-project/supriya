import supriya.osc
from supriya.commands.BufferAllocateRequest import BufferAllocateRequest
from supriya.enums import RequestId


class BufferAllocateReadRequest(BufferAllocateRequest):
    """
    A /b_allocRead request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferAllocateReadRequest(
        ...     buffer_id=23,
        ...     file_path='pulse_44100sr_16bit_octo.wav',
        ...     )
        >>> print(request)
        BufferAllocateReadRequest(
            buffer_id=23,
            file_path='pulse_44100sr_16bit_octo.wav',
            )

    ::

        >>> message = request.to_osc()
        >>> message
        OscMessage(29, 23, '...pulse_44100sr_16bit_octo.wav', 0, -1)

    ::

        >>> message.address == supriya.RequestId.BUFFER_ALLOCATE_READ
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_file_path", "_frame_count", "_starting_frame")

    request_id = RequestId.BUFFER_ALLOCATE_READ

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        callback=None,
        file_path=None,
        frame_count=None,
        starting_frame=None,
    ):
        import supriya.nonrealtime

        BufferAllocateRequest.__init__(
            self, buffer_id=buffer_id, frame_count=frame_count, callback=callback
        )
        if not supriya.nonrealtime.Session.is_session_like(file_path):
            file_path = str(file_path)
        self._file_path = file_path
        if starting_frame is not None:
            starting_frame = int(starting_frame)
            assert 0 <= starting_frame
        self._starting_frame = starting_frame

    ### PRIVATE METHODS ###

    def _get_osc_message_contents(self, with_request_name=False):
        if with_request_name:
            request_id = self.request_name
        else:
            request_id = int(self.request_id)
        buffer_id = int(self.buffer_id)
        frame_count = self.frame_count
        if frame_count is None:
            frame_count = -1
        starting_frame = self.starting_frame
        if starting_frame is None:
            starting_frame = 0
        contents = [request_id, buffer_id, self.file_path, starting_frame, frame_count]
        return contents

    ### PUBLIC METHODS ###

    def to_osc(self, with_request_name=False):
        contents = self._get_osc_message_contents(with_request_name)
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
    def response_patterns(self):
        return ["/done", "/b_allocRead", self.buffer_id], None

    @property
    def starting_frame(self):
        return self._starting_frame
