from supriya.commands.Response import Response


class BufferInfoResponse(Response):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_buffer_id',
        '_channel_count',
        '_frame_count',
        '_sample_rate',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        frame_count=None,
        channel_count=None,
        sample_rate=None,
        osc_message=None,
    ):
        Response.__init__(
            self,
            osc_message=osc_message,
            )
        self._buffer_id = buffer_id
        self._frame_count = frame_count
        self._channel_count = channel_count
        self._sample_rate = sample_rate

    ### PUBLIC METHODS ###

    @classmethod
    def from_osc_message(cls, osc_message):
        """
        Create response(s) from OSC message.

        ::

            >>> message = supriya.osc.OscMessage('/b_info', 1100, 512, 1, 44100.0)
            >>> supriya.commands.BufferInfoResponse.from_osc_message(message)[0]
            BufferInfoResponse(
                buffer_id=1100,
                channel_count=1,
                frame_count=512,
                sample_rate=44100.0,
                )

        """
        # TODO: Return one single thing
        responses = []
        for group in cls._group_items(osc_message.contents, 4):
            response = cls(*group)
            responses.append(response)
        responses = tuple(responses)
        return responses

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def channel_count(self):
        return self._channel_count

    @property
    def frame_count(self):
        return self._frame_count

    @property
    def sample_rate(self):
        return self._sample_rate
