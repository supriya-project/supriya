# -*- encoding: utf-8 -*-
from supriya.tools.servertools.ServerObjectProxy import ServerObjectProxy


class Buffer(ServerObjectProxy):
    r'''A buffer.

    ::

        >>> from supriya.tools import servertools
        >>> buffer_ = servertools.Buffer()
        >>> buffer_
        <Buffer: None>

    ::

        >>> server = servertools.Server()
        >>> server.boot()
        <Server: udp://127.0.0.1:57751, 8i8o>

    ::

        >>> buffer_.allocate(frame_count=8192)
        >>> server.sync()
        <Server: udp://127.0.0.1:57751, 8i8o>

    ::

        >>> buffer_
        <Buffer: 0>

    ::

        >>> buffer_.free()
        >>> server.sync()
        <Server: udp://127.0.0.1:57751, 8i8o>

    ::

        >>> server.quit()
        <Server: offline>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_buffer_group',
        '_buffer_id',
        '_buffer_id_was_set_manually',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_group_or_index=None,
        ):
        from supriya.tools import servertools
        ServerObjectProxy.__init__(self)
        buffer_group = None
        buffer_id = None
        self._buffer_id_was_set_manually = False
        if buffer_group_or_index is not None:
            self._buffer_id_was_set_manually = True
            if isinstance(buffer_group_or_index, servertools.BufferGroup):
                buffer_group = buffer_group_or_index
            elif isinstance(buffer_group_or_index, int):
                buffer_id = int(buffer_group_or_index)
        self._buffer_group = buffer_group
        self._buffer_id = buffer_id

    ### SPECIAL METHODS ###

    def __repr__(self):
        string = '<{}: {}>'.format(
            type(self).__name__,
            self.buffer_id
            )
        return string

    ### PRIVATE METHODS ###

    def _register_with_server(
        self,
        channel_count=None,
        frame_count=None,
        ):
        from supriya.tools import servertools
        if self.buffer_id not in self.server._buffers:
            self.server._buffers[self.buffer_id] = set()
        self.server._buffers[self.buffer_id].add(self)
        self.server._get_buffer_proxy(self.buffer_id)
        on_done = servertools.CommandManager.make_buffer_query_message(
            self.buffer_id,
            )
        message = servertools.CommandManager.make_buffer_allocate_message(
            buffer_id=self.buffer_id,
            frame_count=frame_count,
            channel_count=channel_count,
            completion_message=on_done,
            )
        self.server.send_message(message)

    def _unregister_with_server(self):
        from supriya.tools import servertools
        buffer_id = self.buffer_id
        buffers = self.server._buffers[buffer_id]
        buffers.remove(self)
        if not buffers:
            del(self.server._buffers[buffer_id])
        on_done = servertools.CommandManager.make_buffer_query_message(
            buffer_id,
            )
        message = servertools.CommandManager.make_buffer_free_message(
            buffer_id=buffer_id,
            completion_message=on_done,
            )
        self.server.send_message(message)

    ### PUBLIC METHODS ###

    def allocate(
        self,
        channel_count=1,
        frame_count=None,
        server=None,
        ):
        if self.buffer_group is not None:
            return
        if self.is_allocated:
            return
        ServerObjectProxy.allocate(self, server=server)
        channel_count = int(channel_count)
        frame_count = int(frame_count)
        assert 0 < channel_count
        assert 0 < frame_count
        if self.buffer_id is None:
            buffer_id = self.server.buffer_allocator.allocate(1)
            if buffer_id is None:
                ServerObjectProxy.free(self)
                raise ValueError
            self._buffer_id = buffer_id
        self._register_with_server(
            channel_count=channel_count,
            frame_count=frame_count,
            )

    def free(self):
        if not self.is_allocated:
            return
        self._unregister_with_server()
        if not self._buffer_id_was_set_manually:
            self.server.buffer_allocator.free(self.buffer_id)
        self._buffer_id = None
        ServerObjectProxy.free(self)

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_group(self):
        return self._buffer_group

    @property
    def buffer_id(self):
        if self._buffer_group is not None:
            if self._buffer_group.buffer_id is not None:
                group_id = self._buffer_group.buffer_id
                index = self._buffer_group.index(self)
                buffer_id = group_id + index
                return buffer_id
        return self._buffer_id

    @property
    def channel_count(self):
        if self.is_allocated:
            proxy = self.server._buffer_proxies[self.buffer_id]
            return proxy.channel_count
        return 0

    @property
    def frame_count(self):
        if self.is_allocated:
            proxy = self.server._buffer_proxies[self.buffer_id]
            return proxy.frame_count
        return 0

    @property
    def sample_rate(self):
        if self.is_allocated:
            proxy = self.server._buffer_proxies[self.buffer_id]
            return proxy.sample_rate
        return 0

    @property
    def is_allocated(self):
        if self.buffer_group is not None:
            return self.buffer_group.is_allocated
        return self.server is not None

    @property
    def server(self):
        if self.buffer_group is not None:
            return self.buffer_group.server
        return self._server
