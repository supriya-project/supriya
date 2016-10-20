# -*- encoding: utf-8 -*-
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

        >>> server = servertools.Server()
        >>> buffer_proxy = servertools.BufferProxy(
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
            server=Server(
                ip_address='127.0.0.1',
                port=57751
                )
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
        from supriya.tools import servertools
        buffer_id = int(buffer_id)
        assert 0 <= buffer_id
        assert isinstance(server, servertools.Server)
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

            >>> float(buffer_proxy)
            0.0

        Returns float.
        """
        return float(self.buffer_id)

    def __int__(self):
        """
        Gets integer representation of buffer proxy.

        ::

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

            >>> a_buffer = servertools.BufferProxy(
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
                server=Server(
                    ip_address='127.0.0.1',
                    port=57751
                    )
                )

        ::

            >>> response = responsetools.BufferInfoResponse(
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
                server=Server(
                    ip_address='127.0.0.1',
                    port=57751
                    )
                )

        Returns none.
        """
        from supriya.tools import responsetools
        assert response.buffer_id == self.buffer_id
        if isinstance(response, responsetools.BufferInfoResponse):
            self._channel_count = response.channel_count
            self._frame_count = response.frame_count
            self._sample_rate = response.sample_rate

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        """
        Gets buffer id of buffer proxy.

        ::

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

            >>> buffer_proxy.server
            <Server: udp://127.0.0.1:57751, 8i8o>

        Returns server.
        """
        return self._server
