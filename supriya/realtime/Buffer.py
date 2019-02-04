import collections

import supriya.exceptions
from supriya.realtime.ServerObjectProxy import ServerObjectProxy


class Buffer(ServerObjectProxy):
    """
    A buffer.

    ::

        >>> server = supriya.realtime.Server().boot()

    ::

        >>> buffer_ = supriya.realtime.Buffer()
        >>> buffer_
        <- Buffer: ???>

    ::

        >>> buffer_ = buffer_.allocate(frame_count=8192)
        >>> server.sync()
        <Server: udp://127.0.0.1:57751, 8i8o>

    ::

        >>> buffer_
        <+ Buffer: 0>

    ::

        >>> buffer_ = buffer_.free()
        >>> buffer_
        <- Buffer: ???>

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Main Classes"

    __slots__ = ("_buffer_group", "_buffer_id", "_buffer_id_was_set_manually")

    ### INITIALIZER ###

    def __init__(self, buffer_group_or_index=None):
        import supriya.realtime

        ServerObjectProxy.__init__(self)
        buffer_group = None
        buffer_id = None
        self._buffer_id_was_set_manually = False
        if buffer_group_or_index is not None:
            self._buffer_id_was_set_manually = True
            if isinstance(buffer_group_or_index, supriya.realtime.BufferGroup):
                buffer_group = buffer_group_or_index
            elif isinstance(buffer_group_or_index, int):
                buffer_id = int(buffer_group_or_index)
        self._buffer_group = buffer_group
        self._buffer_id = buffer_id

    ### SPECIAL METHODS ###

    def __float__(self):
        """
        Gets float representation of buffer.

        ::

            >>> server = supriya.realtime.Server().boot()
            >>> buffer_one = supriya.realtime.Buffer().allocate(frame_count=8)
            >>> buffer_two = supriya.realtime.Buffer().allocate(frame_count=8)

        ::

            >>> buffer_one
            <+ Buffer: 0>

        ::

            >>> float(buffer_one)
            0.0

        ::

            >>> buffer_two
            <+ Buffer: 1>

        ::

            >>> float(buffer_two)
            1.0

        ::

            >>> buffer_one = buffer_one.free()
            >>> buffer_two = buffer_two.free()

        ::

            >>> buffer_three = supriya.realtime.Buffer()
            >>> float(buffer_three)
            Traceback (most recent call last):
            ...
            supriya.exceptions.BufferNotAllocated

        Returns float.
        """
        if not self.is_allocated:
            raise supriya.exceptions.BufferNotAllocated
        return float(self.buffer_id)

    def __int__(self):
        """
        Gets integer representation of buffer.

        ::

            >>> server = supriya.realtime.Server().boot()
            >>> buffer_one = supriya.realtime.Buffer().allocate(frame_count=8)
            >>> buffer_two = supriya.realtime.Buffer().allocate(frame_count=8)

        ::

            >>> buffer_one
            <+ Buffer: 0>

        ::

            >>> int(buffer_one)
            0

        ::

            >>> buffer_two
            <+ Buffer: 1>

        ::

            >>> int(buffer_two)
            1

        ::

            >>> buffer_one = buffer_one.free()
            >>> buffer_two = buffer_two.free()

        ::

            >>> buffer_three = supriya.realtime.Buffer()
            >>> int(buffer_three)
            Traceback (most recent call last):
            ...
            supriya.exceptions.BufferNotAllocated

        Returns integer.
        """
        if not self.is_allocated:
            raise supriya.exceptions.BufferNotAllocated
        return int(self.buffer_id)

    def __repr__(self):
        """
        Gets interpreter representation of buffer.

        ::

            >>> server = supriya.realtime.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer()
            >>> repr(buffer_)
            '<- Buffer: ???>'

        ::

            >>> buffer_ = buffer_.allocate(frame_count=8)
            >>> repr(buffer_)
            '<+ Buffer: 0>'

        ::

            >>> buffer_ = buffer_.free()
            >>> repr(buffer_)
            '<- Buffer: ???>'

        Returns string.
        """
        buffer_id = self.buffer_id
        if buffer_id is None:
            buffer_id = "???"
        string = "<{} {}: {}>".format(
            "+" if self.is_allocated else "-", type(self).__name__, buffer_id
        )
        return string

    ### PRIVATE METHODS ###

    def _allocate_buffer_id(self):
        if self.buffer_id is None:
            buffer_id = self.server.buffer_allocator.allocate(1)
            if buffer_id is None:
                ServerObjectProxy.free(self)
                raise ValueError
            self._buffer_id = buffer_id

    def _register_with_local_server(self):
        if self.buffer_id not in self.server._buffers:
            self.server._buffers[self.buffer_id] = set()
        self.server._buffers[self.buffer_id].add(self)
        self.server._get_buffer_proxy(self.buffer_id)

    def _register_with_remote_server(
        self,
        channel_count=None,
        frame_count=None,
        file_path=None,
        channel_indices=None,
        starting_frame=None,
    ):
        import supriya.commands

        on_done = supriya.commands.BufferQueryRequest(buffer_ids=(self.buffer_id,))
        if file_path and channel_indices is not None:
            if not isinstance(channel_indices, collections.Sequence):
                channel_indices = (channel_indices,)
            channel_indices = tuple(channel_indices)
            assert all(0 <= _ for _ in channel_indices)
            request = supriya.commands.BufferAllocateReadChannelRequest(
                buffer_id=self.buffer_id,
                channel_indices=channel_indices,
                file_path=file_path,
                frame_count=frame_count,
                starting_frame=starting_frame,
                callback=on_done,
            )
        elif file_path:
            request = supriya.commands.BufferAllocateReadRequest(
                buffer_id=self.buffer_id,
                file_path=file_path,
                frame_count=frame_count,
                starting_frame=starting_frame,
                callback=on_done,
            )
        else:
            request = supriya.commands.BufferAllocateRequest(
                buffer_id=self.buffer_id,
                frame_count=frame_count,
                channel_count=channel_count,
                callback=on_done,
            )
        return request

    def _unregister_with_local_server(self):
        buffer_id = self.buffer_id
        buffers = self.server._buffers[buffer_id]
        buffers.remove(self)
        if not buffers:
            del (self.server._buffers[buffer_id])
        return buffer_id

    def _unregister_with_remote_server(self, buffer_id):
        import supriya.commands

        on_done = supriya.commands.BufferQueryRequest(buffer_ids=(buffer_id,))
        request = supriya.commands.BufferFreeRequest(
            buffer_id=buffer_id, callback=on_done
        )
        return request

    ### PUBLIC METHODS ###

    def allocate(self, channel_count=1, frame_count=1, server=None, sync=True):
        """
        Allocates buffer on `server`.

        ::

            >>> server = supriya.realtime.Server().boot()
            >>> buffer_one = supriya.realtime.Buffer().allocate()
            >>> buffer_one.query()
            BufferInfoResponse(
                items=(
                    Item(buffer_id=0, frame_count=1, channel_count=1, sample_rate=44100.0),
                    ),
                )

        ::

            >>> buffer_two = supriya.realtime.Buffer().allocate(
            ...     frame_count=16,
            ...     )
            >>> buffer_two.query()
            BufferInfoResponse(
                items=(
                    Item(buffer_id=1, frame_count=16, channel_count=1, sample_rate=44100.0),
                    ),
                )

        ::

            >>> buffer_three = supriya.realtime.Buffer().allocate(
            ...     channel_count=2,
            ...     frame_count=32,
            ...     )
            >>> buffer_three.query()
            BufferInfoResponse(
                items=(
                    Item(buffer_id=2, frame_count=32, channel_count=2, sample_rate=44100.0),
                    ),
                )

        ::

            >>> buffer_three.allocate()
            Traceback (most recent call last):
            ...
            supriya.exceptions.BufferAlreadyAllocated

        ::

            >>> buffer_one = buffer_one.free()
            >>> buffer_two = buffer_two.free()
            >>> buffer_three = buffer_three.free()

        Returns buffer.
        """
        if self.is_allocated:
            raise supriya.exceptions.BufferAlreadyAllocated
        try:
            ServerObjectProxy.allocate(self, server=server)
            channel_count = int(channel_count)
            frame_count = int(frame_count)
            assert 0 < channel_count
            assert 0 < frame_count
            self._allocate_buffer_id()
            self._register_with_local_server()
            request = self._register_with_remote_server(
                channel_count=channel_count, frame_count=frame_count
            )
            request.communicate(server=self.server, sync=sync)
        except Exception:
            self.free()
        return self

    def allocate_from_file(
        self,
        file_path,
        channel_indices=None,
        callback=None,
        frame_count=None,
        server=None,
        starting_frame=None,
        sync=True,
    ):
        """
        Allocates buffer on `server` with contents read from `file_path`.

        ::

            >>> server = supriya.realtime.Server().boot()
            >>> buffer_one = supriya.realtime.Buffer().allocate_from_file(
            ...     supriya.system.Assets['audio/pulse_44100sr_16bit_octo.wav'],
            ...     )
            >>> buffer_one.query()
            BufferInfoResponse(
                items=(
                    Item(buffer_id=0, frame_count=8, channel_count=8, sample_rate=44100.0),
                    ),
                )

        ::

            >>> buffer_two = supriya.realtime.Buffer().allocate_from_file(
            ...     supriya.system.Assets['audio/pulse_44100sr_16bit_octo.wav'],
            ...     channel_indices=(3, 4),
            ...     frame_count=4,
            ...     starting_frame=1,
            ...     sync=True,
            ...     )
            >>> buffer_two.query()
            BufferInfoResponse(
                items=(
                    Item(buffer_id=1, frame_count=4, channel_count=2, sample_rate=44100.0),
                    ),
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

            >>> buffer_two.allocate()
            Traceback (most recent call last):
            ...
            supriya.exceptions.BufferAlreadyAllocated

        ::

            >>> buffer_one = buffer_one.free()
            >>> buffer_two = buffer_two.free()

        Returns buffer.
        """
        if self.is_allocated:
            raise supriya.exceptions.BufferAlreadyAllocated
        try:
            ServerObjectProxy.allocate(self, server=server)
            self._allocate_buffer_id()
            self._register_with_local_server()
            request = self._register_with_remote_server(
                frame_count=frame_count,
                channel_indices=channel_indices,
                file_path=file_path,
                starting_frame=starting_frame,
            )
            request.communicate(server=self.server, sync=sync)
        except Exception:
            ServerObjectProxy.allocate(self, server=server)
        return self

    def close(self, sync=True):
        """
        Closes buffer, if it was open during a read or write process by
        the DiskIn or DiskOut UGens.

        ::

            >>> server = supriya.realtime.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer().allocate(
            ...     channel_count=8,
            ...     frame_count=8,
            ...     )
            >>> buffer_.read(
            ...     supriya.system.Assets['audio/pulse_44100sr_16bit_octo.wav'],
            ...     leave_open=True,
            ...     )
            >>> buffer_.close()
            >>> buffer_ = buffer_.free()

        ::

            >>> buffer_.close()
            Traceback (most recent call last):
            ...
            supriya.exceptions.BufferNotAllocated

        Returns none.
        """
        import supriya.commands

        if not self.is_allocated:
            raise supriya.exceptions.BufferNotAllocated
        request = supriya.commands.BufferCloseRequest(buffer_id=self.buffer_id)
        request.communicate(server=self.server, sync=sync)

    def copy_to(
        self,
        frame_count=None,
        source_starting_frame=None,
        target_buffer_id=None,
        target_starting_frame=None,
        sync=True,
    ):
        """
        Copies data in this buffer into another buffer.

        ::

            >>> server = supriya.realtime.Server().boot()
            >>> buffer_one = supriya.realtime.Buffer().allocate(frame_count=4)
            >>> buffer_two = supriya.realtime.Buffer().allocate(frame_count=4)
            >>> buffer_one.fill([(0, 4, 0.5)])
            >>> buffer_one.copy_to(target_buffer_id=buffer_two)
            >>> buffer_two.get_contiguous([(0, 4)]).as_dict()
            OrderedDict([(0, (0.5, 0.5, 0.5, 0.5))])

        ::

            >>> buffer_one = buffer_one.free()
            >>> buffer_two = buffer_two.free()

        ::

            >>> buffer_one.copy_to(target_buffer_id=666)
            Traceback (most recent call last):
            ...
            supriya.exceptions.BufferNotAllocated

        Returns none.
        """
        import supriya.commands

        if not self.is_allocated:
            raise supriya.exceptions.BufferNotAllocated
        request = supriya.commands.BufferCopyRequest(
            frame_count=frame_count,
            source_buffer_id=self.buffer_id,
            source_starting_frame=source_starting_frame,
            target_buffer_id=target_buffer_id,
            target_starting_frame=target_starting_frame,
        )
        request.communicate(server=self.server, sync=sync)

    def copy_from(
        self,
        frame_count=None,
        source_buffer_id=None,
        source_starting_frame=None,
        target_starting_frame=None,
        sync=True,
    ):
        """
        Copies data from another buffer into this buffer.

        ::

            >>> server = supriya.realtime.Server().boot()
            >>> buffer_one = supriya.realtime.Buffer().allocate(frame_count=4)
            >>> buffer_two = supriya.realtime.Buffer().allocate(frame_count=4)
            >>> buffer_one.fill([(0, 4, 0.5)])
            >>> buffer_two.copy_from(
            ...     frame_count=2,
            ...     source_buffer_id=buffer_one,
            ...     target_starting_frame=1,
            ...     )
            >>> buffer_two.get_contiguous([(0, 4)]).as_dict()
            OrderedDict([(0, (0.0, 0.5, 0.5, 0.0))])

        ::

            >>> buffer_one = buffer_one.free()
            >>> buffer_two = buffer_two.free()

        ::

            >>> buffer_one.copy_from(source_buffer_id=666)
            Traceback (most recent call last):
            ...
            supriya.exceptions.BufferNotAllocated

        Returns none.
        """
        import supriya.commands

        if not self.is_allocated:
            raise supriya.exceptions.BufferNotAllocated
        request = supriya.commands.BufferCopyRequest(
            frame_count=frame_count,
            source_buffer_id=source_buffer_id,
            source_starting_frame=source_starting_frame,
            target_buffer_id=self.buffer_id,
            target_starting_frame=target_starting_frame,
        )
        request.communicate(server=self.server, sync=sync)

    def fill(self, index_count_value_triples=None):
        """
        Fills contiguous blocks of samples with values.

        ::

            >>> server = supriya.realtime.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer().allocate(
            ...     frame_count=8,
            ...     server=server,
            ...     sync=True,
            ...     )
            >>> buffer_.fill([(0, 2, 0.5), (3, 3, 1.)])
            >>> buffer_.get_contiguous([(0, 8)]).as_dict()
            OrderedDict([(0, (0.5, 0.5, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0))])

        ::

            >>> buffer_ = buffer_.free()

        ::

            >>> buffer_.fill()
            Traceback (most recent call last):
            ...
            supriya.exceptions.BufferNotAllocated

        Returns none.
        """
        import supriya.commands

        if not self.is_allocated:
            raise supriya.exceptions.BufferNotAllocated
        request = supriya.commands.BufferFillRequest(
            buffer_id=self.buffer_id,
            index_count_value_triples=index_count_value_triples,
        )
        request.communicate(server=self.server, sync=False)

    def free(self) -> "Buffer":
        """
        Frees buffer.
        """
        if not self.is_allocated:
            raise supriya.exceptions.BufferNotAllocated
        buffer_id = self._unregister_with_local_server()
        request = self._unregister_with_remote_server(buffer_id)
        if self.server.is_running:
            request.communicate(server=self.server, sync=False)
        if not self._buffer_id_was_set_manually:
            self.server.buffer_allocator.free(self.buffer_id)
        self._buffer_id = None
        ServerObjectProxy.free(self)
        return self

    def fill_via_chebyshev(
        self,
        amplitudes,
        as_wavetable=True,
        should_normalize=True,
        should_clear_first=True,
        sync=True,
    ):
        """
        Fills buffer with Chebyshev polynomial.

        ::

            >>> server = supriya.realtime.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer().allocate(
            ...     frame_count=8,
            ...     server=server,
            ...     )
            >>> buffer_.fill_via_chebyshev(
            ...     amplitudes=(1, 0.5, 0.25),
            ...     as_wavetable=False,
            ...     )
            >>> for x in buffer_.get_contiguous([(0, 8)]).as_dict()[0]:
            ...     x
            ...
            -0.2133333384990692
            -0.03999999910593033
            4.7369516864363795e-17
            -0.013333333656191826
            0.0
            0.12000000476837158
            0.4266666769981384
            1.0

        ::

            >>> buffer_ = buffer_.free()

        ::

            >>> buffer_.fill_via_chebyshev(amplitudes=(1, 0.5, 0.25))
            Traceback (most recent call last):
            ...
            supriya.exceptions.BufferNotAllocated

        Returns none.
        """
        import supriya.commands

        if not self.is_allocated:
            raise supriya.exceptions.BufferNotAllocated
        request = supriya.commands.BufferGenerateRequest.chebyshev(
            amplitudes=amplitudes,
            as_wavetable=as_wavetable,
            buffer_id=self.buffer_id,
            should_clear_first=should_clear_first,
            should_normalize=should_normalize,
        )
        request.communicate(server=self.server, sync=sync)

    def fill_via_sine_1(
        self,
        amplitudes=None,
        as_wavetable=True,
        should_clear_first=True,
        should_normalize=True,
        sync=True,
    ):
        """
        Fills buffer with sum of sinusoids via `/b_gen sine1`.

        ::

            >>> server = supriya.realtime.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer().allocate(
            ...     frame_count=8,
            ...     server=server,
            ...     )
            >>> buffer_.fill_via_sine_1(
            ...     amplitudes=(1, 1, 1),
            ...     as_wavetable=False,
            ...     )
            >>> for x in buffer_.get_contiguous([(0, 8)]).as_dict()[0]:
            ...     x
            ...
            0.0
            1.0
            0.0
            0.17157284915447235
            1.014530602374735e-16
            -0.17157284915447235
            0.0
            -1.0

        ::

            >>> buffer_ = buffer_.free()

        ::

            >>> buffer_.fill_via_sine_1(amplitudes=(1, 1, 1))
            Traceback (most recent call last):
            ...
            supriya.exceptions.BufferNotAllocated

        Returns none.
        """
        import supriya.commands

        if not self.is_allocated:
            raise supriya.exceptions.BufferNotAllocated
        request = supriya.commands.BufferGenerateRequest.sine1(
            amplitudes=amplitudes,
            as_wavetable=as_wavetable,
            buffer_id=self.buffer_id,
            should_clear_first=should_clear_first,
            should_normalize=should_normalize,
        )
        request.communicate(server=self.server, sync=sync)

    def fill_via_sine_2(
        self,
        amplitudes,
        frequencies,
        as_wavetable=True,
        should_clear_first=True,
        should_normalize=True,
        sync=True,
    ):
        """
        Fills buffer with sum of sinusoids via `/b_gen sine2`.

        ::

            >>> server = supriya.realtime.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer().allocate(
            ...     frame_count=8,
            ...     server=server,
            ...     )
            >>> buffer_.fill_via_sine_2(
            ...     amplitudes=(1, 0.5, 0.25),
            ...     as_wavetable=False,
            ...     frequencies=(1, 2, 4),
            ...     )
            >>> for x in buffer_.get_contiguous([(0, 8)]).as_dict()[0]:
            ...     x
            ...
            0.0
            0.46657732129096985
            0.8170253038406372
            0.9893794655799866
            1.0
            0.9250487685203552
            0.8511532545089722
            0.8245751261711121

        ::

            >>> buffer_ = buffer_.free()

        ::

            >>> buffer_.fill_via_sine_2(
            ...     amplitudes=(1, 0.5, 0.25),
            ...     frequencies=(1, 2, 4),
            ...     )
            Traceback (most recent call last):
            ...
            supriya.exceptions.BufferNotAllocated

        Returns none.
        """
        import supriya.commands

        if not self.is_allocated:
            raise supriya.exceptions.BufferNotAllocated
        request = supriya.commands.BufferGenerateRequest.sine2(
            amplitudes=amplitudes,
            frequencies=frequencies,
            as_wavetable=as_wavetable,
            buffer_id=self.buffer_id,
            should_clear_first=should_clear_first,
            should_normalize=should_normalize,
        )
        request.communicate(server=self.server, sync=sync)

    def fill_via_sine_3(
        self,
        amplitudes,
        frequencies,
        phases,
        as_wavetable=True,
        should_clear_first=True,
        should_normalize=True,
        sync=True,
    ):
        """
        Fills buffer with sum of sinusoids via `/b_gen sine3`.

        ::

            >>> server = supriya.realtime.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer().allocate(
            ...     frame_count=8,
            ...     server=server,
            ...     )
            >>> buffer_.fill_via_sine_3(
            ...     amplitudes=(1, 0.5, 0.25),
            ...     as_wavetable=False,
            ...     frequencies=(1, 2, 3),
            ...     phases=(0, 0.5, 0),
            ...     )
            >>> for x in buffer_.get_contiguous([(0, 8)]).as_dict()[0]:
            ...     x
            ...
            0.21980325877666473
            0.6533028483390808
            0.9323374032974243
            1.0
            0.8886302709579468
            0.6973193287849426
            0.5352014899253845
            0.46329957246780396

        ::

            >>> buffer_ = buffer_.free()

        ::

            >>> buffer_.fill_via_sine_3(
            ...     amplitudes=(1, 0.5, 0.25),
            ...     frequencies=(1, 2, 3),
            ...     phases=(0, 0.5, 0),
            ...     )
            Traceback (most recent call last):
            ...
            supriya.exceptions.BufferNotAllocated

        Returns none.
        """
        import supriya.commands

        if not self.is_allocated:
            raise supriya.exceptions.BufferNotAllocated
        request = supriya.commands.BufferGenerateRequest.sine3(
            amplitudes=amplitudes,
            frequencies=frequencies,
            phases=phases,
            as_wavetable=as_wavetable,
            buffer_id=self.buffer_id,
            should_clear_first=should_clear_first,
            should_normalize=should_normalize,
        )
        request.communicate(server=self.server, sync=sync)

    def get(self, indices=None):
        """
        Gets sample values at `indices`.

        ::

            >>> server = supriya.realtime.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer().allocate(
            ...     frame_count=4,
            ...     server=server,
            ...     sync=True,
            ...     )
            >>> response = buffer_.get(indices=(1, 2))
            >>> response.as_dict()
            OrderedDict([(1, 0.0), (2, 0.0)])

        ::

            >>> buffer_ = buffer_.free()

        ::

            >>> buffer_.get()
            Traceback (most recent call last):
            ...
            supriya.exceptions.BufferNotAllocated

        Returns buffer-set response.
        """
        import supriya.commands

        if not self.is_allocated:
            raise supriya.exceptions.BufferNotAllocated
        if isinstance(indices, int):
            indices = [indices]
        request = supriya.commands.BufferGetRequest(buffer_id=self, indices=indices)
        response = request.communicate(server=self.server)
        if isinstance(response, supriya.commands.FailResponse):
            raise IndexError("Index out of range.")
        return response

    def get_contiguous(self, index_count_pairs=None):
        """
        Gets contiguous sample values.

        ::

            >>> server = supriya.realtime.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer().allocate(
            ...     frame_count=4,
            ...     server=server,
            ...     sync=True,
            ...     )
            >>> response = buffer_.get_contiguous(
            ...     index_count_pairs=((0, 2), (1, 3))
            ...     )
            >>> response.as_dict()
            OrderedDict([(0, (0.0, 0.0)), (1, (0.0, 0.0, 0.0))])

        ::

            >>> buffer_ = buffer_.free()

        ::

            >>> buffer_.get_contiguous()
            Traceback (most recent call last):
            ...
            supriya.exceptions.BufferNotAllocated

        Returns buffer-set-contiguous response.
        """
        import supriya.commands

        if not self.is_allocated:
            raise supriya.exceptions.BufferNotAllocated
        request = supriya.commands.BufferGetContiguousRequest(
            buffer_id=self, index_count_pairs=index_count_pairs
        )
        response = request.communicate(server=self.server)
        if isinstance(response, supriya.commands.FailResponse):
            raise IndexError("Index out of range.")
        return response

    def get_frame(self, frame_ids=None, completion_callback=None):
        """
        Gets frames at `frame_ids`.

        ::

            >>> server = supriya.realtime.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer().allocate_from_file(
            ...     supriya.system.Assets['audio/pulse_44100sr_16bit_octo.wav'],
            ...     )
            >>> for frame_id in range(buffer_.frame_count):
            ...     buffer_.get_frame(frame_id).as_dict()
            ...
            OrderedDict([(0, (0.999969482421875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))])
            OrderedDict([(8, (0.0, 0.999969482421875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))])
            OrderedDict([(16, (0.0, 0.0, 0.999969482421875, 0.0, 0.0, 0.0, 0.0, 0.0))])
            OrderedDict([(24, (0.0, 0.0, 0.0, 0.999969482421875, 0.0, 0.0, 0.0, 0.0))])
            OrderedDict([(32, (0.0, 0.0, 0.0, 0.0, 0.999969482421875, 0.0, 0.0, 0.0))])
            OrderedDict([(40, (0.0, 0.0, 0.0, 0.0, 0.0, 0.999969482421875, 0.0, 0.0))])
            OrderedDict([(48, (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.999969482421875, 0.0))])
            OrderedDict([(56, (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.999969482421875))])

        ::

            >>> buffer_ = buffer_.free()

        ::

            >>> buffer_.get_frame()
            Traceback (most recent call last):
            ...
            supriya.exceptions.BufferNotAllocated

        Returns buffer-set-contiguous response.
        """
        if not self.is_allocated:
            raise supriya.exceptions.BufferNotAllocated
        if isinstance(frame_ids, int):
            frame_ids = [frame_ids]
        index_count_pairs = [
            (frame_id * self.channel_count, self.channel_count)
            for frame_id in frame_ids
        ]
        response = self.get_contiguous(index_count_pairs=index_count_pairs)
        return response

    def normalize(self, as_wavetable=None, new_maximum=1.0, sync=False):
        request = supriya.commands.BufferNormalizeRequest(
            as_wavetable=as_wavetable, buffer_id=self, new_maximum=new_maximum
        )
        request.communicate(server=self.server, sync=sync)

    def play(
        self, add_action=None, bus=0, level=1, loop=False, rate=1, target_node=None
    ):
        import supriya.synthdefs
        import supriya.ugens

        if not self.is_allocated:
            raise supriya.exceptions.BufferNotAllocated
        with supriya.synthdefs.SynthDefBuilder(level=1, rate=1) as builder:
            player = supriya.ugens.PlayBuf.ar(
                buffer_id=self.buffer_id,
                channel_count=self.channel_count,
                loop=loop,
                rate=supriya.ugens.BufRateScale.kr(self.buffer_id) * builder["rate"],
            )
            if not loop:
                supriya.ugens.FreeSelfWhenDone.kr(player)
            source = player * builder["level"]
            supriya.ugens.Out.ar(bus=bus, source=source)
        synthdef = builder.build()
        return synthdef.play(
            add_action=add_action, level=level, rate=rate, target_node=target_node
        )

    def query(self):
        """
        Queries buffer.

        ::

            >>> server = supriya.realtime.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer().allocate(
            ...     channel_count=2,
            ...     frame_count=16,
            ...     )
            >>> buffer_.query()
            BufferInfoResponse(
                items=(
                    Item(buffer_id=0, frame_count=16, channel_count=2, sample_rate=44100.0),
                    ),
                )

        ::

            >>> buffer_ = buffer_.free()

        ::

            >>> buffer_.query()
            Traceback (most recent call last):
            ...
            supriya.exceptions.BufferNotAllocated

        Returns buffer-info response.
        """
        import supriya.commands

        if not self.is_allocated:
            raise supriya.exceptions.BufferNotAllocated
        buffer_ids = [self.buffer_id]
        request = supriya.commands.BufferQueryRequest(buffer_ids=buffer_ids)
        response = request.communicate(server=self.server)
        return response

    def read(
        self,
        file_path,
        channel_indices=None,
        callback=None,
        frame_count=None,
        leave_open=None,
        starting_frame_in_buffer=None,
        starting_frame_in_file=None,
        sync=True,
    ):
        """
        Reads contents of `file_path` into buffer.

        ::

            >>> server = supriya.realtime.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer().allocate(
            ...     channel_count=2,
            ...     frame_count=8,
            ...     )
            >>> for frame_id in range(buffer_.frame_count):
            ...     buffer_.get_frame(frame_id).as_dict()
            ...
            OrderedDict([(0, (0.0, 0.0))])
            OrderedDict([(2, (0.0, 0.0))])
            OrderedDict([(4, (0.0, 0.0))])
            OrderedDict([(6, (0.0, 0.0))])
            OrderedDict([(8, (0.0, 0.0))])
            OrderedDict([(10, (0.0, 0.0))])
            OrderedDict([(12, (0.0, 0.0))])
            OrderedDict([(14, (0.0, 0.0))])

        ::

            >>> file_path = supriya.system.Assets['audio/pulse_44100sr_16bit_octo.wav']
            >>> buffer_.read(file_path, channel_indices=(0, 1))

        ::

            >>> for frame_id in range(buffer_.frame_count):
            ...     buffer_.get_frame(frame_id).as_dict()
            ...
            OrderedDict([(0, (0.999969482421875, 0.0))])
            OrderedDict([(2, (0.0, 0.999969482421875))])
            OrderedDict([(4, (0.0, 0.0))])
            OrderedDict([(6, (0.0, 0.0))])
            OrderedDict([(8, (0.0, 0.0))])
            OrderedDict([(10, (0.0, 0.0))])
            OrderedDict([(12, (0.0, 0.0))])
            OrderedDict([(14, (0.0, 0.0))])

        ::

            >>> buffer_ = buffer_.free()

        ::

            >>> buffer_.read(file_path)
            Traceback (most recent call last):
            ...
            supriya.exceptions.BufferNotAllocated

        Returns none.
        """
        import supriya.commands

        if not self.is_allocated:
            raise supriya.exceptions.BufferNotAllocated
        on_done = supriya.commands.BufferQueryRequest(buffer_ids=(self.buffer_id,))
        if channel_indices is not None:
            request = supriya.commands.BufferReadChannelRequest(
                buffer_id=self.buffer_id,
                channel_indices=channel_indices,
                callback=on_done,
                file_path=file_path,
                frame_count=frame_count,
                leave_open=leave_open,
                starting_frame_in_buffer=starting_frame_in_buffer,
                starting_frame_in_file=starting_frame_in_file,
            )
        else:
            request = supriya.commands.BufferReadRequest(
                buffer_id=self.buffer_id,
                callback=on_done,
                file_path=file_path,
                frame_count=frame_count,
                leave_open=leave_open,
                starting_frame_in_buffer=starting_frame_in_buffer,
                starting_frame_in_file=starting_frame_in_file,
            )
        request.communicate(server=self.server, sync=sync)

    def set(self, index_value_pairs=None, sync=False):
        """
        Sets samples.

        ::

            >>> server = supriya.realtime.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer().allocate(
            ...     frame_count=8,
            ...     )

        ::

            >>> buffer_.set([
            ...     (0, 0.25),
            ...     (1, 0.5),
            ...     (4, 0.75),
            ...     (5, 1.0),
            ...     ])
            >>> buffer_.get_contiguous([(0, 8)]).as_dict()[0]
            (0.25, 0.5, 0.0, 0.0, 0.75, 1.0, 0.0, 0.0)

        ::

            >>> buffer_ = buffer_.free()

        ::

            >>> buffer_.set()
            Traceback (most recent call last):
            ...
            supriya.exceptions.BufferNotAllocated

        Returns none.
        """
        import supriya.commands

        if not self.is_allocated:
            raise supriya.exceptions.BufferNotAllocated
        request = supriya.commands.BufferSetRequest(
            buffer_id=self, index_value_pairs=index_value_pairs
        )
        request.communicate(server=self.server, sync=sync)

    def set_contiguous(self, index_values_pairs=None, sync=False):
        """
        Sets contiguous blocks of samples.

        ::

            >>> server = supriya.realtime.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer().allocate(
            ...     frame_count=8,
            ...     )

        ::

            >>> buffer_.set_contiguous([
            ...     (1, [1, 2, 3]),
            ...     (4, [-3, 2, -1]),
            ...     ])
            >>> buffer_.get_contiguous([(0, 8)]).as_dict()[0]
            (0.0, 1.0, 2.0, 3.0, -3.0, 2.0, -1.0, 0.0)

        ::

            >>> buffer_ = buffer_.free()

        ::

            >>> buffer_.set_contiguous()
            Traceback (most recent call last):
            ...
            supriya.exceptions.BufferNotAllocated

        Returns none.
        """
        import supriya.commands

        if not self.is_allocated:
            raise supriya.exceptions.BufferNotAllocated
        request = supriya.commands.BufferSetContiguousRequest(
            buffer_id=self, index_values_pairs=index_values_pairs
        )
        request.communicate(server=self.server, sync=sync)

    def write(
        self,
        file_path,
        callback=None,
        frame_count=None,
        header_format="aiff",
        leave_open=False,
        sample_format="int24",
        starting_frame=None,
        sync=True,
    ):
        """
        Writes buffer to disk.

        ::

            >>> server = supriya.realtime.Server().boot()
            >>> buffer_one = supriya.realtime.Buffer().allocate_from_file(
            ...     supriya.system.Assets['audio/pulse_44100sr_16bit_octo.wav'],
            ...     channel_indices=(0,),
            ...     )
            >>> buffer_one.get_contiguous([(0, 8)]).as_dict()[0]
            (0.999969482421875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

        ::

            >>> import os
            >>> file_path = os.path.expanduser('~')
            >>> file_path = os.path.join(file_path, 'temp.wav')
            >>> if os.path.exists(file_path):
            ...     os.remove(file_path)

        ::

            >>> buffer_one.write(
            ...     file_path,
            ...     header_format='wav',
            ...     )

        ::

            >>> buffer_two = supriya.realtime.Buffer().allocate_from_file(file_path)
            >>> buffer_two.get_contiguous([(0, 8)]).as_dict()[0]
            (0.999969482421875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

        ::

            >>> os.remove(file_path)
            >>> buffer_one = buffer_one.free()
            >>> buffer_two = buffer_two.free()

        ::

            >>> buffer_one.write(file_path=file_path)
            Traceback (most recent call last):
            ...
            supriya.exceptions.BufferNotAllocated

        Returns none.
        """
        import supriya.commands

        if not self.is_allocated:
            raise supriya.exceptions.BufferNotAllocated
        request = supriya.commands.BufferWriteRequest(
            buffer_id=self.buffer_id,
            callback=callback,
            file_path=file_path,
            frame_count=frame_count,
            header_format=header_format,
            leave_open=leave_open,
            sample_format=sample_format,
            starting_frame=starting_frame,
        )
        request.communicate(server=self.server, sync=sync)

    def zero(self, callback=None, sync=True):
        """
        Zero all samples in buffer.

        ::

            >>> server = supriya.realtime.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer().allocate(
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

            >>> buffer_ = buffer_.free()

        ::

            >>> buffer_.zero()
            Traceback (most recent call last):
            ...
            supriya.exceptions.BufferNotAllocated

        Returns none.
        """
        import supriya.commands

        if not self.is_allocated:
            raise supriya.exceptions.BufferNotAllocated
        request = supriya.commands.BufferZeroRequest(
            buffer_id=self.buffer_id, callback=callback
        )
        request.communicate(server=self.server, sync=sync)

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_group(self):
        """
        Gets buffer group.

        ::

            >>> server = supriya.realtime.Server().boot()
            >>> buffer_one = supriya.realtime.Buffer().allocate(frame_count=8)
            >>> buffer_one.buffer_group is None
            True

        ::

            >>> buffer_group = supriya.realtime.BufferGroup(buffer_count=1)
            >>> buffer_group.allocate(frame_count=8)
            <+ BufferGroup{1}: 1>

        ::

            >>> buffer_two = buffer_group[0]
            >>> buffer_two.buffer_group is buffer_group
            True

        ::

            >>> buffer_one = buffer_one.free()
            >>> buffer_one.buffer_group is None
            True

        ::

            >>> buffer_group = buffer_group.free()
            >>> buffer_two.buffer_group is buffer_group
            True

        Returns BufferGroup or none.
        """
        return self._buffer_group

    @property
    def buffer_id(self):
        """
        Gets buffer id.

        ::

            >>> server = supriya.realtime.Server().boot()
            >>> buffer_one = supriya.realtime.Buffer()
            >>> buffer_one.buffer_id is None
            True

        ::

            >>> buffer_group = supriya.realtime.BufferGroup(buffer_count=4)
            >>> for buffer_ in buffer_group:
            ...     print(buffer_.buffer_id)
            ...
            None
            None
            None
            None

        ::

            >>> buffer_one = buffer_one.allocate(frame_count=8)
            >>> buffer_one.buffer_id
            0

        ::

            >>> buffer_group.allocate(frame_count=8)
            <+ BufferGroup{4}: 1>

        ::

            >>> for buffer_ in  buffer_group:
            ...     buffer_.buffer_id
            ...
            1
            2
            3
            4

        ::

            >>> buffer_one = buffer_one.free()
            >>> buffer_one.buffer_id is None
            True

        ::

            >>> buffer_group = buffer_group.free()
            >>> for buffer_ in buffer_group:
            ...     print(buffer_.buffer_id)
            ...
            None
            None
            None
            None

        Returns integer or none.
        """
        if self._buffer_group is not None:
            if self._buffer_group.buffer_id is not None:
                group_id = self._buffer_group.buffer_id
                index = self._buffer_group.index(self)
                buffer_id = group_id + index
                return buffer_id
        return self._buffer_id

    @property
    def channel_count(self):
        """
        Gets channel count.

        ::

            >>> server = supriya.realtime.Server().boot()
            >>> buffer_one = supriya.realtime.Buffer().allocate(
            ...     frame_count=8,
            ...     )

        ::

            >>> buffer_two = supriya.realtime.Buffer().allocate(
            ...     channel_count=4,
            ...     frame_count=8,
            ...     )

        ::

            >>> buffer_one.channel_count
            1

        ::

            >>> buffer_two.channel_count
            4

        ::

            >>> buffer_one = buffer_one.free()
            >>> buffer_two = buffer_two.free()

        Returns integer.
        """
        if self.is_allocated:
            proxy = self.server._buffer_proxies[self.buffer_id]
            return proxy.channel_count
        return 0

    @property
    def duration_in_seconds(self):
        """
        Gets duration in seconds.

        ::

            >>> server = supriya.realtime.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer()
            >>> buffer_.duration_in_seconds
            0.0

        ::

            >>> buffer_ = buffer_.allocate(frame_count=44100)
            >>> buffer_.duration_in_seconds
            1.0

        ::

            >>> buffer_ = buffer_.free()
            >>> buffer_.duration_in_seconds
            0.0

        Returns float.
        """
        if self.is_allocated:
            proxy = self.server._buffer_proxies[self.buffer_id]
            return proxy.duration_in_seconds
        return 0.0

    @property
    def frame_count(self):
        """
        Gets frame count.

        ::

            >>> server = supriya.realtime.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer()
            >>> buffer_.frame_count
            0

        ::

            >>> buffer_ = buffer_.allocate(frame_count=512)
            >>> buffer_.frame_count
            512

        ::

            >>> buffer_ = buffer_.free()
            >>> buffer_.frame_count
            0

        Returns integer.
        """
        if self.is_allocated:
            proxy = self.server._buffer_proxies[self.buffer_id]
            return proxy.frame_count
        return 0

    @property
    def sample_count(self):
        """
        Gets sample count.

        ::

            >>> server = supriya.realtime.Server().boot()
            >>> buffer_one = supriya.realtime.Buffer().allocate(frame_count=16)
            >>> buffer_two = supriya.realtime.Buffer().allocate(
            ...     channel_count=2,
            ...     frame_count=16,
            ...     )
            >>> buffer_three = supriya.realtime.Buffer().allocate(
            ...     channel_count=8,
            ...     frame_count=16,
            ...     )

        ::

            >>> buffer_one.sample_count
            16

        ::

            >>> buffer_two.sample_count
            32

        ::

            >>> buffer_three.sample_count
            128

        ::

            >>> buffer_one = buffer_one.free()
            >>> buffer_two = buffer_two.free()
            >>> buffer_three = buffer_three.free()

        ::

            >>> buffer_one.sample_count
            0

        ::

            >>> buffer_two.sample_count
            0

        ::

            >>> buffer_three.sample_count
            0

        Returns integer.
        """
        if self.is_allocated:
            proxy = self.server._buffer_proxies[self.buffer_id]
            return proxy.sample_count
        return 0

    @property
    def sample_rate(self):
        """
        Gets sample-rate.

        ::

            >>> server = supriya.realtime.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer()
            >>> buffer_.sample_rate
            0

        ::

            >>> buffer_ = buffer_.allocate(frame_count=8)
            >>> buffer_.sample_rate
            44100.0

        ::

            >>> buffer_ = buffer_.free()
            >>> buffer_.sample_rate
            0

        Returns float.
        """
        if self.is_allocated:
            proxy = self.server._buffer_proxies[self.buffer_id]
            return proxy.sample_rate
        return 0

    @property
    def is_allocated(self):
        """
        Is true if buffer is allocated. Otherwise false.

        ::

            >>> server = supriya.realtime.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer()
            >>> buffer_.is_allocated
            False

        ::

            >>> buffer_ = buffer_.allocate(frame_count=8)
            >>> buffer_.is_allocated
            True

        ::

            >>> buffer_ = buffer_.free()
            >>> buffer_.is_allocated
            False

        Returns boolean
        """
        if self.buffer_group is not None:
            return self.buffer_group.is_allocated
        return self.server is not None

    @property
    def server(self):
        """
        Gets associated server.

        ::

            >>> server = supriya.realtime.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer()
            >>> buffer_.server is None
            True

        ::

            >>> buffer_ = buffer_.allocate(frame_count=8)
            >>> buffer_.server is server
            True

        ::

            >>> buffer_ = buffer_.free()
            >>> buffer_.server is None
            True

        Returns server or none.
        """
        if self.buffer_group is not None:
            return self.buffer_group.server
        return self._server
