from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class BufferProxy(SupriyaValueObject):
    """
    A buffer proxy.

    Acts as a singleton reference to a buffer on the server, tracking the state
    of a single buffer id and responding to `/b_info` messages. Multiple Buffer
    instances reference a single BufferProxy.

    BufferProxy instances are created internally by the server, and should be
    treated as an implementation detail.

    ::

        >>> server = supriya.realtime.Server()
        >>> buffer_proxy = supriya.realtime.BufferProxy(
        ...     buffer_id=0,
        ...     server=server,
        ...     channel_count=2,
        ...     frame_count=441,
        ...     sample_rate=44100,
        ...     )
        >>> buffer_proxy
        BufferProxy(
            buffer_id=0,
            channel_count=2,
            frame_count=441,
            sample_rate=44100,
            server=<Server: offline>,
            )

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Server Internals'

    __slots__ = (
        '_buffer_id',
        '_channel_count',
        '_frame_count',
        '_sample_rate',
        '_server',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        channel_count=0,
        frame_count=0,
        sample_rate=0,
        server=None,
        ):
        import supriya.realtime
        buffer_id = int(buffer_id)
        assert 0 <= buffer_id
        assert isinstance(server, supriya.realtime.Server)
        self._buffer_id = int(buffer_id)
        self._channel_count = int(channel_count)
        self._frame_count = int(frame_count)
        self._sample_rate = int(sample_rate)
        self._server = server

    ### SPECIAL METHODS ###

    def __float__(self):
        """
        Gets float representation of buffer proxy.

        ::

            >>> server = supriya.realtime.Server()
            >>> buffer_proxy = supriya.realtime.BufferProxy(
            ...     buffer_id=0,
            ...     server=server,
            ...     channel_count=2,
            ...     frame_count=441,
            ...     sample_rate=44100,
            ...     )
            >>> float(buffer_proxy)
            0.0

        Returns float.
        """
        return float(self.buffer_id)

    def __int__(self):
        """
        Gets integer representation of buffer proxy.

        ::

            >>> server = supriya.realtime.Server()
            >>> buffer_proxy = supriya.realtime.BufferProxy(
            ...     buffer_id=0,
            ...     server=server,
            ...     channel_count=2,
            ...     frame_count=441,
            ...     sample_rate=44100,
            ...     )
            >>> int(buffer_proxy)
            0

        Returns integer.
        """
        return int(self.buffer_id)

    ### PRIVATE METHODS ###

    def _handle_response(self, response):
        """
        Updates buffer proxy with buffer-info response.

        ::

            >>> server = supriya.realtime.Server()
            >>> a_buffer = supriya.realtime.BufferProxy(
            ...     buffer_id=23,
            ...     channel_count=1,
            ...     frame_count=256,
            ...     sample_rate=44100,
            ...     server=server,
            ...     )
            >>> a_buffer
            BufferProxy(
                buffer_id=23,
                channel_count=1,
                frame_count=256,
                sample_rate=44100,
                server=<Server: offline>,
                )

        ::

            >>> response = supriya.commands.BufferInfoResponse(
            ...     buffer_id=23,
            ...     channel_count=2,
            ...     frame_count=512,
            ...     sample_rate=44100,
            ...     )

        ::

            >>> a_buffer._handle_response(response)
            >>> a_buffer
            BufferProxy(
                buffer_id=23,
                channel_count=2,
                frame_count=512,
                sample_rate=44100,
                server=<Server: offline>,
                )

        Returns none.
        """
        import supriya.commands
        assert response.buffer_id == self.buffer_id
        if isinstance(response, supriya.commands.BufferInfoResponse):
            self._channel_count = response.channel_count
            self._frame_count = response.frame_count
            self._sample_rate = response.sample_rate

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        """
        Gets buffer id of buffer proxy.

        ::

            >>> server = supriya.realtime.Server()
            >>> buffer_proxy = supriya.realtime.BufferProxy(
            ...     buffer_id=0,
            ...     server=server,
            ...     channel_count=2,
            ...     frame_count=441,
            ...     sample_rate=44100,
            ...     )
            >>> buffer_proxy.buffer_id
            0

        Returns integer.
        """
        return self._buffer_id

    @property
    def channel_count(self):
        """
        Gets channel count of buffer proxy.

        ::

            >>> server = supriya.realtime.Server()
            >>> buffer_proxy = supriya.realtime.BufferProxy(
            ...     buffer_id=0,
            ...     server=server,
            ...     channel_count=2,
            ...     frame_count=441,
            ...     sample_rate=44100,
            ...     )
            >>> buffer_proxy.channel_count
            2

        Returns integer.
        """
        return self._channel_count

    @property
    def duration_in_seconds(self):
        """
        Gets duration in seconds of buffer proxy.

        ::

            >>> server = supriya.realtime.Server()
            >>> buffer_proxy = supriya.realtime.BufferProxy(
            ...     buffer_id=0,
            ...     server=server,
            ...     channel_count=2,
            ...     frame_count=441,
            ...     sample_rate=44100,
            ...     )
            >>> buffer_proxy.duration_in_seconds
            0.01

        Returns float.
        """
        return float(self._frame_count) / float(self.sample_rate)

    @property
    def frame_count(self):
        """
        Gets frame count of buffer proxy.

        ::

            >>> server = supriya.realtime.Server()
            >>> buffer_proxy = supriya.realtime.BufferProxy(
            ...     buffer_id=0,
            ...     server=server,
            ...     channel_count=2,
            ...     frame_count=441,
            ...     sample_rate=44100,
            ...     )
            >>> buffer_proxy.frame_count
            441

        Returns integer.
        """
        return self._frame_count

    @property
    def sample_count(self):
        """
        Gets sample count of buffer proxy.

        ::

            >>> server = supriya.realtime.Server()
            >>> buffer_proxy = supriya.realtime.BufferProxy(
            ...     buffer_id=0,
            ...     server=server,
            ...     channel_count=2,
            ...     frame_count=441,
            ...     sample_rate=44100,
            ...     )
            >>> buffer_proxy.sample_count
            882

        Returns integer.
        """
        return self._channel_count * self._frame_count

    @property
    def sample_rate(self):
        """
        Gets sample-rate of buffer proxy.

        ::

            >>> server = supriya.realtime.Server()
            >>> buffer_proxy = supriya.realtime.BufferProxy(
            ...     buffer_id=0,
            ...     server=server,
            ...     channel_count=2,
            ...     frame_count=441,
            ...     sample_rate=44100,
            ...     )
            >>> buffer_proxy.sample_rate
            44100

        Returns integer.
        """
        return self._sample_rate

    @property
    def server(self):
        """
        Gets server of buffer proxy.

        ::

            >>> server = supriya.realtime.Server()
            >>> buffer_proxy = supriya.realtime.BufferProxy(
            ...     buffer_id=0,
            ...     server=server,
            ...     channel_count=2,
            ...     frame_count=441,
            ...     sample_rate=44100,
            ...     )
            >>> buffer_proxy.server
            <Server: offline>

        Returns server.
        """
        return self._server
