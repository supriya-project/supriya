# -*- encoding: utf-8 -*-
import collections
from supriya.tools import osctools
from supriya.tools.requesttools.BufferAllocateReadRequest import BufferAllocateReadRequest


class BufferAllocateReadChannelRequest(BufferAllocateReadRequest):
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
        '_channel_indices',
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
        BufferAllocateReadRequest.__init__(
            self,
            buffer_id=buffer_id,
            completion_message=completion_message,
            file_path=file_path,
            frame_count=frame_count,
            starting_frame=starting_frame,
            )
        if not isinstance(channel_indices, collections.Sequence):
            channel_indices = (channel_indices,)
        channel_indices = tuple(int(_) for _ in channel_indices)
        assert all(0 <= _ for _ in channel_indices)
        self._channel_indices = channel_indices

    ### PUBLIC METHODS ###

    def to_osc_message(self):
        contents = self._get_osc_message_contents()
        contents.extend(self.channel_indices)
        self._coerce_completion_message_output(contents)
        message = osctools.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def channel_indices(self):
        return self._channel_indices

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