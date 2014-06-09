# -*- encoding: utf-8 -*-
from supriya.tools.servertools.ServerObjectProxy import ServerObjectProxy


class Buffer(ServerObjectProxy):
    r'''A buffer.

    ::

        >>> from supriya import servertools
        >>> stereo_buffer = servertools.Buffer(
        ...     frame_count=1024,
        ...     channel_count=2,
        ...     )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_channel_count',
        '_frame_count',
        )

    ### INITIALIZER ###

    def __init__(self, frame_count=512, channel_count=1):
        ServerObjectProxy.__init__(self)
        assert 0 < frame_count
        assert 0 < channel_count
        self._frame_count = int(frame_count)
        self._channel_count = int(channel_count)

    ### PUBLIC METHODS ###

    def allocate(self, server_session=None):
        ServerObjectProxy.allocate(self)
        self._buffer_index = server_session.buffer_allocator.allocate(1)

    def free(self):
        ServerObjectProxy.free(self)

    ### PUBLIC PROPERTIES ###

    @property
    def channel_count(self):
        return self._channel_count

    @property
    def frame_count(self):
        return self._frame_count
