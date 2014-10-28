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

        >>> buffer_group.allocate(
        ...     frame_count=8192,
        ...     server=server,
        ...     sync=True,
        ...     )
        <BufferGroup: {4} @ 0>

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

    def __float__(self):
        return float(self.buffer_id)

    def __getitem__(self, index):
        r'''Gets buffer at `index`.

        Returns buffer.
        '''
        return self._buffers[index]

    def __int__(self):
        return int(self.buffer_id)

    def __len__(self):
        r'''Gets length of buffer group.

        Returns integer.
        '''
        return len(self._buffers)

    def __repr__(self):
        r'''Gets interpreter representation of buffer group.

        Returns string.
        '''
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
        sync=True,
        ):
        r'''Allocates buffer group.

        Returns buffer group.
        '''
        from supriya.tools import servertools
        if self.is_allocated:
            return
        ServerObjectProxy.allocate(
            self,
            server=server,
            )
        buffer_id = self.server.buffer_allocator.allocate(len(self))
        if buffer_id is None:
            ServerObjectProxy.free(self)
            raise ValueError
        self._buffer_id = buffer_id
        channel_count = int(channel_count)
        frame_count = int(frame_count)
        assert 0 < channel_count
        assert 0 < frame_count
        message_bundler = servertools.MessageBundler(
            server=server,
            sync=sync,
            )
        with message_bundler:
            for i in range(len(self)):
                buffer_id = self.buffer_id + i
                self[i]._register_with_local_server()
                request = self[i]._register_with_remote_server(
                    channel_count=channel_count,
                    frame_count=frame_count,
                    )
                message_bundler.add_message(request)
        return self

    def free(self):
        r'''Frees all buffers in buffer group.

        Returns none.
        '''
        if not self.is_allocated:
            return
        for buffer_ in self:
            buffer_.free()
        buffer_id = self.buffer_id
        self._buffer_id = None
        self.server.buffer_allocator.free(buffer_id)
        ServerObjectProxy.free(self)

    def zero(self):
        r'''Analogous to SuperCollider's Buffer.zero.
        '''
        raise NotImplementedError

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets initial buffer id.

        Returns integer or none.
        '''
        return self._buffer_id

    @property
    def buffers(self):
        r'''Gets associated buffers.

        Returns tuple or buffers.
        '''
        return self._buffers

    @property
    def is_allocated(self):
        r'''Is true when buffer group is allocated. Otherwise false.

        Returns boolean.
        '''
        return self.server is not None