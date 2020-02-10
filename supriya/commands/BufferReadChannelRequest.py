import collections

import supriya.osc
from supriya.commands.BufferReadRequest import BufferReadRequest
from supriya.enums import RequestId


class BufferReadChannelRequest(BufferReadRequest):
    """
    A /b_readChannel request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferReadChannelRequest(
        ...     buffer_id=23,
        ...     channel_indices=(3, 4),
        ...     file_path='pulse_44100sr_16bit_octo.wav',
        ...     )
        >>> print(request)
        BufferReadChannelRequest(
            buffer_id=23,
            channel_indices=(3, 4),
            file_path='pulse_44100sr_16bit_octo.wav',
            )

    ::

        >>> request.to_osc()
        OscMessage('/b_readChannel', 23, '...pulse_44100sr_16bit_octo.wav', 0, -1, 0, 0, 3, 4)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.BUFFER_READ_CHANNEL

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        channel_indices=None,
        callback=None,
        file_path=None,
        frame_count=None,
        leave_open=None,
        starting_frame_in_buffer=None,
        starting_frame_in_file=None,
    ):
        BufferReadRequest.__init__(
            self,
            buffer_id=buffer_id,
            callback=callback,
            file_path=file_path,
            frame_count=frame_count,
            leave_open=leave_open,
            starting_frame_in_buffer=starting_frame_in_buffer,
            starting_frame_in_file=starting_frame_in_file,
        )
        if not isinstance(channel_indices, collections.Sequence):
            channel_indices = (channel_indices,)
        channel_indices = tuple(channel_indices)
        assert all(0 <= _ for _ in channel_indices)
        self._channel_indices = channel_indices

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        contents = self._get_osc_message_contents()
        contents.extend(self.channel_indices)
        if self.callback:
            contents.append(self.callback.to_osc())
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def channel_indices(self):
        return self._channel_indices

    @property
    def response_patterns(self):
        return ["/done", "/b_readChannel", self.buffer_id], None
