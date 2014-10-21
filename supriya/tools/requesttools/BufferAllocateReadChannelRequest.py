# -*- encoding: utf-8 -*-
import collections
import os
from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class BufferAllocateReadChannelRequest(Request):
    r'''A /b_allocRead request.

    ::

        >>> from supriya.tools import requesttools
        >>> request = requesttools.BufferAllocateReadChannelRequest(
        ...     buffer_id=23,
        ...     channel_indices=(3, 4),
        ...     file_path='pulse_44100sr_16bit_octo.wav',
        ...     )
        >>> print(request)
        BufferAllocateReadChannelRequest(
            buffer_id=23,
            channel_indices=(3, 4),
            file_path='pulse_44100sr_16bit_octo.wav'
            )

    ::

        >>> message = request.to_osc_message()
        >>> message
        OscMessage(54, 23, '...pulse_44100sr_16bit_octo.wav', 0, -1, 3, 4)

    ::

        >>> message.address == requesttools.RequestId.BUFFER_ALLOCATE_READ_CHANNEL
        True

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_buffer_id',
        '_channel_indices',
        '_completion_message',
        '_file_path',
        '_frame_count',
        '_starting_frame',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        channel_indices=None,
        completion_message=None,
        file_path=None,
        frame_count=None,
        starting_frame=None,
        ):
        Request.__init__(self)
        self._buffer_id = int(buffer_id)
        if not isinstance(channel_indices, collections.Sequence):
            channel_indices = (channel_indices,)
        channel_indices = tuple(int(_) for _ in channel_indices)
        assert all(0 <= _ for _ in channel_indices)
        self._channel_indices = channel_indices
        self._completion_message = self._coerce_completion_message_input(
            completion_message)
        self._file_path = str(file_path)
        if frame_count is not None:
            frame_count = int(frame_count)
            assert -1 <= frame_count
        self._frame_count = frame_count
        if starting_frame is not None:
            starting_frame = int(starting_frame)
            assert 0 <= starting_frame
        self._starting_frame = starting_frame

    ### PUBLIC METHODS ###

    def to_osc_message(self):
        request_id = int(self.request_id)
        buffer_id = int(self.buffer_id)
        frame_count = self.frame_count
        if frame_count is None:
            frame_count = -1
        starting_frame = self.starting_frame
        if starting_frame is None:
            starting_frame = 0
        file_path = os.path.abspath(os.path.expanduser(str(self.file_path)))
        contents = [
            request_id,
            buffer_id,
            file_path,
            starting_frame,
            frame_count,
            ]
        contents.extend(self.channel_indices)
        self._coerce_completion_message_output(contents)
        message = osctools.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def channel_indices(self):
        return self._channel_indices

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
    def response_specification(self):
        from supriya.tools import responsetools
        return {
            responsetools.DoneResponse: {
                'action': ('/b_allocReadChannel', self.buffer_id),
                },
            }

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.BUFFER_ALLOCATE_READ_CHANNEL

    @property
    def starting_frame(self):
        return self._starting_frame