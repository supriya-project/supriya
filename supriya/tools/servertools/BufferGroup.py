# -*- encoding: utf-8 -*-
import collections
from supriya.tools.servertools.ServerObjectProxy import ServerObjectProxy


class BufferGroup(ServerObjectProxy, collections.Sequence):
    r'''A buffer group.

    ::

        >>> from supriya.tools import servertools
        >>> buffer_group = servertools.BufferGroup(buffer_count=4)
        >>> buffer_group
        <BufferGroup: {4} @ None>

    ::

        >>> server = servertools.Server()
        >>> server.boot()
        <Server: udp://127.0.0.1:57751, 8i8o>

    ::

        >>> buffer_group.allocate(frame_count=8192)
        >>> server.sync()
        <Server: udp://127.0.0.1:57751, 8i8o>

    ::

        >>> buffer_group
        <BufferGroup: {4} @ 0>

    ::

        >>> buffer_group.free()
        >>> server.sync()
        <Server: udp://127.0.0.1:57751, 8i8o>

    ::

        >>> server.quit()
        <Server: offline>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_buffer_id',
        '_buffers',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_count=1,
        ):
        from supriya.tools import servertools
        ServerObjectProxy.__init__(self)
        self._buffer_id = None
        buffer_count = int(buffer_count)
        assert 0 < buffer_count
        self._buffers = tuple(
            servertools.Buffer(buffer_group_or_index=self)
            for _ in range(buffer_count)
            )

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self._buffers[item]

    def __len__(self):
        return len(self._buffers)

    def __repr__(self):
        string = '<{}: {{{}}} @ {}>'.format(
            type(self).__name__,
            len(self),
            self.buffer_id
            )
        return string

    ### PUBLIC METHODS ###

    def allocate(
        self,
        channel_count=1,
        frame_count=None,
        server=None,
        ):
        from supriya.tools import servertools
        if self.is_allocated:
            return
        ServerObjectProxy.allocate(self, server=server)
        channel_count = int(channel_count)
        frame_count = int(frame_count)
        assert 0 < channel_count
        assert 0 < frame_count
        buffer_id = self.server.buffer_allocator.allocate(len(self))
        if buffer_id is None:
            ServerObjectProxy.free(self)
            raise ValueError
        self._buffer_id = buffer_id
        for i in range(len(self)):
            buffer_id = self.buffer_id + i

            if buffer_id not in self.server._buffers:
                self.server._buffers[buffer_id] = set()
            self.server._buffers[buffer_id].add(self[i])

            if buffer_id not in self.server._buffer_proxies:
                buffer_proxy = servertools.BufferProxy(
                    buffer_id=buffer_id,
                    server=self.server,
                    )
                self.server._buffer_proxies[buffer_id] = buffer_proxy

            on_done = servertools.CommandManager.make_buffer_query_message(
                buffer_id,
                )
            message = servertools.CommandManager.make_buffer_allocate_message(
                buffer_id=buffer_id,
                frame_count=frame_count,
                channel_count=channel_count,
                completion_message=on_done,
                )
            self.server.send_message(message)

    def free(self):
        if not self.is_allocated:
            return
        for buffer_ in self:
            buffer_.free()
        self._buffer_id = None
        ServerObjectProxy.free(self)

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def buffers(self):
        return self._buffers

    @property
    def is_allocated(self):
        return self.server is not None
