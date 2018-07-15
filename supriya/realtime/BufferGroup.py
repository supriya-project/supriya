import os
from supriya.realtime.ServerObjectProxy import ServerObjectProxy


class BufferGroup(ServerObjectProxy):
    """
    A buffer group.

    ::

        >>> server = supriya.realtime.Server().boot()

    ::

        >>> buffer_group = supriya.realtime.BufferGroup(buffer_count=4)
        >>> buffer_group
        <BufferGroup: {4} @ None>

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

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Main Classes'

    __slots__ = (
        '_buffer_id',
        '_buffers',
        )

    ### INITIALIZER ###

    def __init__(self, buffer_count=1):
        import supriya.realtime
        ServerObjectProxy.__init__(self)
        self._buffer_id = None
        buffer_count = int(buffer_count)
        assert 0 < buffer_count
        self._buffers = tuple(
            supriya.realtime.Buffer(buffer_group_or_index=self)
            for _ in range(buffer_count)
            )

    ### SPECIAL METHODS ###

    def __contains__(self, item):
        return self.buffers.__contains__(item)

    def __float__(self):
        return float(self.buffer_id)

    def __getitem__(self, index):
        """
        Gets buffer at `index`.

        Returns buffer.
        """
        return self._buffers[index]

    def __int__(self):
        return int(self.buffer_id)

    def __iter__(self):
        return iter(self.buffers)

    def __len__(self):
        """
        Gets length of buffer group.

        Returns integer.
        """
        return len(self._buffers)

    def __repr__(self):
        """
        Gets interpreter representation of buffer group.

        Returns string.
        """
        string = '<{}: {{{}}} @ {}>'.format(
            type(self).__name__,
            len(self),
            self.buffer_id
            )
        return string

    ### PRIVATE METHODS ###

    def _register_with_local_server(self, server):
        ServerObjectProxy.allocate(
            self,
            server=server,
            )
        allocator = self.server.buffer_allocator
        buffer_id = allocator.allocate(len(self))
        if buffer_id is None:
            ServerObjectProxy.free(self)
            raise ValueError
        self._buffer_id = buffer_id
        for buffer_ in self:
            buffer_._register_with_local_server()
        return buffer_id

    ### PUBLIC METHODS ###

    def allocate(
        self,
        channel_count=1,
        frame_count=None,
        server=None,
        sync=True,
    ):
        """
        Allocates buffer group.

        Returns buffer group.
        """
        import supriya.realtime
        if self.is_allocated:
            return
        self._register_with_local_server(server)
        channel_count = int(channel_count)
        frame_count = int(frame_count)
        assert 0 < channel_count
        assert 0 < frame_count
        message_bundler = supriya.realtime.MessageBundler(
            server=server,
            sync=sync,
            )
        with message_bundler:
            for buffer_ in self:
                request = buffer_._register_with_remote_server(
                    channel_count=channel_count,
                    frame_count=frame_count,
                    )
                message_bundler.add_message(request)
        return self

    def free(self):
        """
        Frees all buffers in buffer group.

        Returns none.
        """
        if not self.is_allocated:
            return
        for buffer_ in self:
            buffer_.free()
        buffer_id = self.buffer_id
        self._buffer_id = None
        self.server.buffer_allocator.free(buffer_id)
        ServerObjectProxy.free(self)

    def index(self, item):
        return self.buffers.index(item)

    @staticmethod
    def from_file_paths(file_paths, server=None):
        """
        Create a buffer group from `file_paths`.

        ::

            >>> file_paths = Assets['audio/*mono_1s*']
            >>> len(file_paths)
            4

        ::

            >>> server = supriya.realtime.Server().boot()
            >>> buffer_group = BufferGroup.from_file_paths(file_paths)

        ::

            >>> for buffer_ in buffer_group:
            ...     buffer_, buffer_.frame_count
            ...
            (<Buffer: 0>, 44100)
            (<Buffer: 1>, 44100)
            (<Buffer: 2>, 44100)
            (<Buffer: 3>, 44100)

        Returns buffer group.
        """
        import supriya.realtime
        for file_path in file_paths:
            assert os.path.exists(file_path)
        buffer_group = BufferGroup(buffer_count=len(file_paths))
        buffer_group._register_with_local_server(server)
        message_bundler = supriya.realtime.MessageBundler(
            server=server,
            sync=True,
            )
        with message_bundler:
            for buffer_, file_path in zip(buffer_group.buffers, file_paths):
                request = buffer_._register_with_remote_server(
                    file_path=file_path,
                    )
                message_bundler.add_message(request)
        return buffer_group

    def zero(self):
        """
        Analogous to SuperCollider's Buffer.zero.
        """
        raise NotImplementedError

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        """
        Gets initial buffer id.

        Returns integer or none.
        """
        return self._buffer_id

    @property
    def buffers(self):
        """
        Gets associated buffers.

        Returns tuple or buffers.
        """
        return self._buffers

    @property
    def is_allocated(self):
        """
        Is true when buffer group is allocated. Otherwise false.

        Returns boolean.
        """
        return self.server is not None
