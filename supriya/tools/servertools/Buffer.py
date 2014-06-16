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
        '_buffer_id',
        '_channel_count',
        '_frame_count',
        )

    ### INITIALIZER ###

    def __init__(self, frame_count=512, channel_count=1):
        ServerObjectProxy.__init__(self)
        assert 0 < frame_count
        assert 0 < channel_count
        self._buffer_id = None
        self._frame_count = int(frame_count)
        self._channel_count = int(channel_count)

    ### PUBLIC METHODS ###

    def allocate(self, server=None):
        ServerObjectProxy.allocate(self, server=server)
        buffer_id = self.server.buffer_allocator.allocate(1)
        if buffer_id is None:
            raise ValueError
        elif buffer_id in self._server._buffers:
            raise ValueError
        self._buffer_id = buffer_id
        self._server._buffers[self._buffer_id] = self

    def free(self):
        if self.server is not None:
            self.server.buffer_allocator.free(self.buffer_id)
            del(self.server.buffers[self.buffer_id])
        self._buffer_id = None
        ServerObjectProxy.free(self)

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
    def is_allocated(self):
        return self.server is not None