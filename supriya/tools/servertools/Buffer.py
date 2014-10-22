# -*- encoding: utf-8 -*-
import collections
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

    def _register_with_local_server(self):
        if self.buffer_id not in self.server._buffers:
            self.server._buffers[self.buffer_id] = set()
        self.server._buffers[self.buffer_id].add(self)
        self.server._get_buffer_proxy(self.buffer_id)

    def _register_with_remote_server(
        self,
        channel_count=None,
        frame_count=None,
        ):
        from supriya.tools import requesttools
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
        return request

    def _unregister_with_local_server(self):
        buffer_id = self.buffer_id
        buffers = self.server._buffers[buffer_id]
        buffers.remove(self)
        if not buffers:
            del(self.server._buffers[buffer_id])
        return buffer_id

    def _unregister_with_remote_server(self, buffer_id):
        from supriya.tools import requesttools
        on_done = requesttools.BufferQueryRequest(
            buffer_ids=(buffer_id,),
            )
        on_done = on_done.to_osc_message()
        request = requesttools.BufferFreeRequest(
            buffer_id=buffer_id,
            completion_message=on_done,
            )
        return request

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
        r'''Allocates buffer on `server`.
        '''
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
            self._register_with_local_server()
            request = self._register_with_remote_server(
                channel_count=channel_count,
                frame_count=frame_count,
                )
            request.communicate(
                server=self.server,
                sync=sync,
                )
        except:
            self.free()
        return self

    def allocate_from_file(
        self,
        file_path,
        channel_indices=None,
        completion_message=None,
        frame_count=None,
        server=None,
        starting_frame=None,
        sync=False,
        ):
        r'''Allocates buffer on `server` with contents read from `file_path`.
        
        ::

            >>> from supriya.tools import servertools
            >>> from supriya.tools import systemtools
            >>> server = servertools.Server().boot()

        ::

            >>> buffer_one = servertools.Buffer().allocate_from_file(
            ...     systemtools.Media['pulse_44100sr_16bit_octo.wav'],
            ...     sync=True,
            ...     )

        ::

            >>> buffer_one.query()
            BufferInfoResponse(
                buffer_id=0,
                frame_count=8,
                channel_count=8,
                sample_rate=44100.0
                )

        ::

            >>> buffer_two = servertools.Buffer().allocate_from_file(
            ...     systemtools.Media['pulse_44100sr_16bit_octo.wav'],
            ...     channel_indices=(3, 4),
            ...     frame_count=4,
            ...     starting_frame=1,
            ...     sync=True,
            ...     )

        ::

            >>> buffer_two.query()
            BufferInfoResponse(
                buffer_id=1,
                frame_count=4,
                channel_count=2,
                sample_rate=44100.0
                )

        ::

            >>> for frame_id in range(buffer_two.frame_count):
            ...     buffer_two.get_frame(frame_id).as_dict()
            ...
            OrderedDict([(0, (0.0, 0.0))])
            OrderedDict([(2, (0.0, 0.0))])
            OrderedDict([(4, (0.999969482421875, 0.0))])
            OrderedDict([(6, (0.0, 0.999969482421875))])

        ::

            >>> server.quit()
            <Server: offline>

        '''
        from supriya.tools import requesttools
        if self.buffer_group is not None:
            return
        if self.is_allocated:
            return
        try:
            ServerObjectProxy.allocate(self, server=server)
            if self.buffer_id is None:
                buffer_id = self.server.buffer_allocator.allocate(1)
                if buffer_id is None:
                    ServerObjectProxy.free(self)
                    raise ValueError
                self._buffer_id = buffer_id
            self._register_with_local_server()
            on_done = requesttools.BufferQueryRequest(
                buffer_ids=(self.buffer_id,),
                )
            on_done = on_done.to_osc_message()
            if channel_indices is not None:
                if not isinstance(channel_indices, collections.Sequence):
                    channel_indices = (channel_indices,)
                channel_indices = tuple(channel_indices)
                assert all(0 <= _ for _ in channel_indices)
                request = requesttools.BufferAllocateReadChannelRequest(
                    buffer_id=self.buffer_id,
                    channel_indices=channel_indices,
                    file_path=file_path,
                    frame_count=frame_count,
                    starting_frame=starting_frame,
                    completion_message=on_done,
                    )
            else:
                request = requesttools.BufferAllocateReadRequest(
                    buffer_id=self.buffer_id,
                    file_path=file_path,
                    frame_count=frame_count,
                    starting_frame=starting_frame,
                    completion_message=on_done,
                    )
            request.communicate(
                server=self.server,
                sync=sync,
                )
        except:
            ServerObjectProxy.allocate(self, server=server)
        return self

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
        r'''Frees buffer.
        '''
        if not self.is_allocated:
            return
        buffer_id = self._unregister_with_local_server()
        request = self._unregister_with_remote_server(buffer_id)
        if self.server.is_running:
            request.communicate(
                server=self.server,
                sync=False,
                )
        if not self._buffer_id_was_set_manually:
            self.server.buffer_allocator.free(self.buffer_id)
        self._buffer_id = None
        ServerObjectProxy.free(self)

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
        from supriya.tools import responsetools
        if not self.is_allocated:
            raise Exception
        if isinstance(indices, int):
            indices = [indices]
        request = requesttools.BufferGetRequest(
            buffer_id=self,
            indices=indices,
            )
        if callable(completion_callback):
            raise NotImplementedError
        response = request.communicate(server=self.server)
        if isinstance(response, responsetools.FailResponse):
            raise IndexError('Index out of range.')
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
        from supriya.tools import responsetools
        if not self.is_allocated:
            raise Exception
        request = requesttools.BufferGetContiguousRequest(
            buffer_id=self,
            index_count_pairs=index_count_pairs,
            )
        if callable(completion_callback):
            raise NotImplementedError
        response = request.communicate(server=self.server)
        if isinstance(response, responsetools.FailResponse):
            raise IndexError('Index out of range.')
        return response

    def get_frame(
        self,
        frame_ids=None,
        completion_callback=None,
        ):
        r'''Gets frames at `frame_ids`.

        ::

            >>> from supriya import servertools
            >>> from supriya import systemtools
            >>> with servertools.Server() as server:
            ...     buffer_ = servertools.Buffer().allocate_from_file(
            ...         systemtools.Media['pulse_44100sr_16bit_octo.wav'],
            ...         sync=True,
            ...         )
            ...     for frame_id in range(buffer_.frame_count):
            ...         buffer_.get_frame(frame_id).as_dict()
            ...
            OrderedDict([(0, (0.999969482421875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))])
            OrderedDict([(8, (0.0, 0.999969482421875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))])
            OrderedDict([(16, (0.0, 0.0, 0.999969482421875, 0.0, 0.0, 0.0, 0.0, 0.0))])
            OrderedDict([(24, (0.0, 0.0, 0.0, 0.999969482421875, 0.0, 0.0, 0.0, 0.0))])
            OrderedDict([(32, (0.0, 0.0, 0.0, 0.0, 0.999969482421875, 0.0, 0.0, 0.0))])
            OrderedDict([(40, (0.0, 0.0, 0.0, 0.0, 0.0, 0.999969482421875, 0.0, 0.0))])
            OrderedDict([(48, (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.999969482421875, 0.0))])
            OrderedDict([(56, (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.999969482421875))])

        Returns response.
        '''
        if not self.is_allocated:
            raise Exception
        if isinstance(frame_ids, int):
            frame_ids = [frame_ids]
        index_count_pairs = [
            (frame_id * self.channel_count, self.channel_count)
            for frame_id in frame_ids
            ]
        response = self.get_contiguous(index_count_pairs=index_count_pairs)
        return response

    def query(self):
        r'''Queries buffer.

        Returns buffer info response.
        '''
        from supriya.tools import requesttools
        if not self.is_allocated:
            raise Exception
        buffer_ids = [self.buffer_id]
        request = requesttools.BufferQueryRequest(
            buffer_ids=buffer_ids,
            )
        response = request.communicate(
            server=self.server,
            )
        return response

    def read(self):
        raise NotImplementedError

    def set(
        self,
        index_value_pairs=None,
        sync=False,
        ):
        from supriya.tools import requesttools
        if not self.is_allocated:
            raise Exception
        request = requesttools.BufferSetRequest(
            buffer_id=self,
            index_value_pairs=index_value_pairs,
            )
        request.communicate(
            server=self.server,
            sync=sync,
            )

    def set_contiguous(
        self,
        index_values_pairs=None,
        sync=False,
        ):
        from supriya.tools import requesttools
        if not self.is_allocated:
            raise Exception
        request = requesttools.BufferSetContiguousRequest(
            buffer_id=self,
            index_values_pairs=index_values_pairs,
            )
        request.communicate(
            server=self.server,
            sync=sync,
            )

    def write(
        self,
        completion_message=None,
        file_path=None,
        frame_count=None,
        header_format='aiff',
        leave_open=False,
        sample_format='int24',
        starting_frame=None,
        sync=True,
        ):
        from supriya.tools import requesttools
        if not self.is_allocated:
            raise Exception
        request = requesttools.BufferWriteRequest(
            buffer_id=self.buffer_id,
            completion_message=completion_message,
            file_path=file_path,
            frame_count=frame_count,
            header_format='aiff',
            leave_open=leave_open,
            sample_format='int24',
            starting_frame=starting_frame,
            )
        request.communicate(
            server=self.server,
            sync=sync,
            )

    def zero(
        self,
        completion_message=None,
        sync=True,
        ):
        r'''Zero all samples in buffer.

        ::

            >>> from supriya.tools import servertools
            >>> server = servertools.Server().boot()

        ::

            >>> buffer_ = servertools.Buffer().allocate(
            ...     frame_count=8,
            ...     sync=True,
            ...     )

        ::

            >>> buffer_.set_contiguous(
            ...     index_values_pairs=[(0, (1, 2, 3, 4, 5, 6, 7, 8))],
            ...     sync=True,
            ...     )

        ::

            >>> buffer_.get_contiguous([(0, 8)]).as_dict()
            OrderedDict([(0, (1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0))])

        ::

            >>> buffer_.zero()

        ::

            >>> buffer_.get_contiguous([(0, 8)]).as_dict()
            OrderedDict([(0, (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))])

        ::

            >>> server.quit()
            <Server: offline>

        '''
        from supriya.tools import requesttools
        if not self.is_allocated:
            raise Exception
        request = requesttools.BufferZeroRequest(
            buffer_id=self.buffer_id,
            completion_message=completion_message,
            )
        request.communicate(
            server=self.server,
            sync=sync,
            )

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