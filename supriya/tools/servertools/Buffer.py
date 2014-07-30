# -*- encoding: utf-8 -*-
from supriya.tools.servertools.BufferMixin import BufferMixin
from supriya.tools.servertools.ServerObjectProxy import ServerObjectProxy


class Buffer(ServerObjectProxy, BufferMixin):
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

        >>> buffer_ = buffer_.allocate(frame_count=8192)
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

    def _generate(
        self,
        generate_command=None,
        frequencies=None,
        amplitudes=None,
        phases=None,
        as_wavetable=True,
        clear_first=True,
        normalize=True,
        ):
        r'''Analogous to SuperCollider's Buffer.gen family of commands.
        '''
        raise NotImplementedError

    def _register_with_server(
        self,
        channel_count=None,
        execution_context=None,
        frame_count=None,
        ):
        from supriya.tools import requesttools
        if self.buffer_id not in self.server._buffers:
            self.server._buffers[self.buffer_id] = set()
        self.server._buffers[self.buffer_id].add(self)
        self.server._get_buffer_proxy(self.buffer_id)
        on_done = requesttools.BufferQueryRequest(
            buffer_ids=(self.buffer_id,),
            )
        on_done = on_done.to_osc_message()
        request = requesttools.BufferAllocateRequest(
            buffer_id=self.buffer_id,
            frame_count=frame_count,
            channel_count=channel_count,
            completion_message=on_done,
            )
        message = request.to_osc_message()
        execution_context = execution_context or self.server
        execution_context.send_message(message)

    def _unregister_with_server(
        self,
        execution_context=None,
        ):
        from supriya.tools import requesttools
        buffer_id = self.buffer_id
        buffers = self.server._buffers[buffer_id]
        buffers.remove(self)
        if not buffers:
            del(self.server._buffers[buffer_id])
        on_done = requesttools.BufferQueryRequest(
            buffer_ids=(buffer_id,),
            )
        on_done = on_done.to_osc_message()
        request = requesttools.BufferFreeRequest(
            buffer_id=buffer_id,
            completion_message=on_done,
            )
        message = request.to_osc_message()
        execution_context = execution_context or self.server
        execution_context.send_message(message)

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            is_bracketted=True,
            keyword_argument_names=(
                'buffer_id',
                ),
            )

    ### PUBLIC METHODS ###

    def allocate(
        self,
        channel_count=1,
        frame_count=None,
        server=None,
        sync=False,
        ):
        if self.buffer_group is not None:
            return
        if self.is_allocated:
            return
        try:
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
        except:
            self.free()
        if sync:
            self.server.sync()
        return self

    def allocate_from_file(
        self,
        server=None,
        sync=False,
        ):
        r'''Analogous to SuperCollider's Buffer.allocRead.
        '''
        raise NotImplementedError

    def allocate_from_sequence(
        self,
        server=None,
        sync=False,
        ):
        r'''Analogous to SuperCollider's Buffer.loadCollection.
        '''
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def copy_data(self):
        raise NotImplementedError

    def free(self):
        if not self.is_allocated:
            return
        self._unregister_with_server()
        if not self._buffer_id_was_set_manually:
            self.server.buffer_allocator.free(self.buffer_id)
        self._buffer_id = None
        ServerObjectProxy.free(self)

    @classmethod
    def from_file(cls):
        raise NotImplementedError

    def generate_from_sines(self):
        raise NotImplementedError

    def generate_from_chebyshev(self):
        raise NotImplementedError

    def get(
        self,
        indices=None,
        completion_callback=None,
        ):
        r'''Gets sample values at `indices`.

        ::

            >>> from supriya import servertools
            >>> with servertools.Server() as server:
            ...     buffer_ = servertools.Buffer().allocate(
            ...         frame_count=4,
            ...         server=server,
            ...         sync=True,
            ...         )
            ...     response = buffer_.get(indices=(1, 2))
            ...     response.as_dict()
            ...
            OrderedDict([(1, 0.0), (2, 0.0)])

        Returns response.
        '''
        from supriya.tools import requesttools
        if not self.is_allocated:
            raise Exception
        request = requesttools.BufferGetRequest(
            buffer_id=self,
            indices=indices,
            )
        if callable(completion_callback):
            raise NotImplementedError
        response = request.communicate(server=self.server)
        return response

    def get_contiguous(
        self,
        index_count_pairs=None,
        completion_callback=None,
        ):
        r'''Gets contiguous sample values.

        ::

            >>> from supriya import servertools
            >>> with servertools.Server() as server:
            ...     buffer_ = servertools.Buffer().allocate(
            ...         frame_count=4,
            ...         server=server,
            ...         sync=True,
            ...         )
            ...     response = buffer_.get_contiguous(
            ...         index_count_pairs=((0, 2), (1, 3))
            ...         )
            ...     response.as_dict()
            ...
            OrderedDict([(0, (0.0, 0.0)), (1, (0.0, 0.0, 0.0))])

        Returns response.
        '''

        from supriya.tools import requesttools
        if not self.is_allocated:
            raise Exception
        request = requesttools.BufferGetContiguousRequest(
            buffer_id=self,
            index_count_pairs=index_count_pairs,
            )
        if callable(completion_callback):
            raise NotImplementedError
        response = request.communicate(server=self.server)
        return response

    def query(self):
        raise NotImplementedError

    def read(self):
        raise NotImplementedError

    def set(
        self,
        execution_context=None,
        index_value_pairs=None,
        ):
        from supriya.tools import requesttools
        if not self.is_allocated:
            raise Exception
        request = requesttools.BufferSetRequest(
            buffer_id=self,
            index_value_pairs=index_value_pairs,
            )
        message = request.to_osc_message()
        execution_context = execution_context or self.server
        execution_context.send_message(message)

    def set_contiguous(
        self,
        execution_context=None,
        index_values_pairs=None,
        ):
        from supriya.tools import requesttools
        if not self.is_allocated:
            raise Exception
        request = requesttools.BufferSetContiguousRequest(
            buffer_id=self,
            index_values_pairs=index_values_pairs,
            )
        message = request.to_osc_message()
        execution_context = execution_context or self.server
        execution_context.send_message(message)

    def write(self):
        raise NotImplementedError

    def zero(
        self,
        completion_message=None,
        ):
        r'''Analogous to SuperCollider's Buffer.zero.
        '''
        raise NotImplementedError

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
    def duration_in_seconds(self):
        if self.is_allocated:
            proxy = self.server._buffer_proxies[self.buffer_id]
            return proxy.duration_in_seconds
        return 0

    @property
    def frame_count(self):
        if self.is_allocated:
            proxy = self.server._buffer_proxies[self.buffer_id]
            return proxy.frame_count
        return 0

    @property
    def sample_count(self):
        if self.is_allocated:
            proxy = self.server._buffer_proxies[self.buffer_id]
            return proxy.sample_count
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