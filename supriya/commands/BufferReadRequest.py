import supriya.osc
from supriya.commands.Request import Request


class BufferReadRequest(Request):
    """
    A /b_read request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferReadRequest(
        ...     buffer_id=23,
        ...     file_path='pulse_44100sr_16bit_octo.wav',
        ...     )
        >>> print(request)
        BufferReadRequest(
            buffer_id=23,
            file_path='pulse_44100sr_16bit_octo.wav',
            )

    ::

        >>> message = request.to_osc_message()
        >>> message
        OscMessage(30, 23, '...pulse_44100sr_16bit_octo.wav', 0, -1, 0, 0)

    ::

        >>> message.address == supriya.commands.RequestId.BUFFER_READ
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_buffer_id',
        '_callback',
        '_file_path',
        '_frame_count',
        '_leave_open',
        '_starting_frame_in_buffer',
        '_starting_frame_in_file',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        callback=None,
        file_path=None,
        frame_count=None,
        leave_open=None,
        starting_frame_in_buffer=None,
        starting_frame_in_file=None,
        ):
        import supriya.nonrealtime
        Request.__init__(self)
        self._buffer_id = int(buffer_id)
        self._callback = self._coerce_callback_input(
            callback)
        if not supriya.nonrealtime.Session.is_session_like(file_path):
            file_path = str(file_path)
        self._file_path = file_path
        if frame_count is not None:
            frame_count = int(frame_count)
            assert -1 <= frame_count
        self._frame_count = frame_count
        if leave_open is not None:
            leave_open = bool(leave_open)
        self._leave_open = leave_open
        if starting_frame_in_buffer is not None:
            starting_frame_in_buffer = int(starting_frame_in_buffer)
            assert 0 <= starting_frame_in_buffer
        self._starting_frame_in_buffer = starting_frame_in_buffer
        if starting_frame_in_file is not None:
            starting_frame_in_file = int(starting_frame_in_file)
            assert 0 <= starting_frame_in_file
        self._starting_frame_in_file = starting_frame_in_file

    ### PRIVATE METHODS ###

    def _get_osc_message_contents(self, with_textual_osc_command=False):
        if with_textual_osc_command:
            request_id = self.request_command
        else:
            request_id = int(self.request_id)
        buffer_id = int(self.buffer_id)
        starting_frame_in_buffer = self.starting_frame_in_buffer
        if starting_frame_in_buffer is None:
            starting_frame_in_buffer = 0
        frame_count = self.frame_count
        if frame_count is None:
            frame_count = -1
        starting_frame_in_file = self.starting_frame_in_file
        if starting_frame_in_file is None:
            starting_frame_in_file = 0
        leave_open = int(bool(self.leave_open))
        contents = [
            request_id,
            buffer_id,
            self.file_path,
            starting_frame_in_file,
            frame_count,
            starting_frame_in_buffer,
            leave_open,
            ]
        return contents

    ### PUBLIC METHODS ###

    def to_osc_message(self, with_textual_osc_command=False):
        contents = self._get_osc_message_contents(with_textual_osc_command)
        self._coerce_callback_output(contents)
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
    def leave_open(self):
        return self._leave_open

    @property
    def response_patterns(self):
        return [['/done', '/b_read', self.buffer_id]]

    @property
    def response_specification(self):
        import supriya.commands
        return {
            supriya.commands.DoneResponse: {
                'action': ('/b_read', self.buffer_id),
                },
            }

    @property
    def request_id(self):
        import supriya.commands
        return supriya.commands.RequestId.BUFFER_READ

    @property
    def starting_frame_in_buffer(self):
        return self._starting_frame_in_buffer

    @property
    def starting_frame_in_file(self):
        return self._starting_frame_in_file
