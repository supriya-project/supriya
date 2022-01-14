import os
import pathlib
import tempfile
from collections.abc import Sequence
from os import PathLike

import supriya.exceptions
from supriya.system import SupriyaValueObject

from ..io import PlayMemo
from .bases import ServerObject


class Buffer(ServerObject):
    """
    A buffer.

    ::

        >>> server = supriya.Server().boot()

    ::

        >>> buffer_ = supriya.realtime.Buffer()
        >>> buffer_
        <- Buffer: ???>

    ::

        >>> buffer_ = buffer_.allocate(server, frame_count=8192)
        >>> server.sync()
        <Server: udp://127.0.0.1:57110, 8i8o>

    ::

        >>> buffer_
        <+ Buffer: 0, 1ch, 8192>

    ::

        >>> buffer_ = buffer_.free()
        >>> buffer_
        <- Buffer: ???>

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_buffer_group", "_buffer_id", "_buffer_id_was_set_manually")

    ### INITIALIZER ###

    def __init__(self, buffer_group_or_index=None):
        ServerObject.__init__(self)
        buffer_group = None
        buffer_id = None
        self._buffer_id_was_set_manually = False
        if buffer_group_or_index is not None:
            self._buffer_id_was_set_manually = True
            if isinstance(buffer_group_or_index, BufferGroup):
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

            >>> server = supriya.Server().boot()
            >>> buffer_one = supriya.realtime.Buffer().allocate(server, frame_count=8)
            >>> buffer_two = supriya.realtime.Buffer().allocate(server, frame_count=8)

        ::

            >>> buffer_one
            <+ Buffer: 0, 1ch, 8>

        ::

            >>> float(buffer_one)
            0.0

        ::

            >>> buffer_two
            <+ Buffer: 1, 1ch, 8>

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

            >>> server = supriya.Server().boot()
            >>> buffer_one = supriya.realtime.Buffer().allocate(server, frame_count=8)
            >>> buffer_two = supriya.realtime.Buffer().allocate(server, frame_count=8)

        ::

            >>> buffer_one
            <+ Buffer: 0, 1ch, 8>

        ::

            >>> int(buffer_one)
            0

        ::

            >>> buffer_two
            <+ Buffer: 1, 1ch, 8>

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

    def __plot__(self):
        import librosa

        with tempfile.TemporaryDirectory() as temp_directory:
            file_path = pathlib.Path(temp_directory) / "tmp.wav"
            self.write(file_path=file_path, header_format="wav", sample_format="int32")
            return librosa.load(file_path, mono=False, sr=None)

    def __render__(self, **kwargs) -> PlayMemo:
        with tempfile.TemporaryDirectory() as temp_directory:
            file_path = pathlib.Path(temp_directory) / "tmp.wav"
            self.write(file_path=file_path, header_format="wav", sample_format="int32")
            return PlayMemo.from_path(file_path)

    def __repr__(self):
        """
        Gets interpreter representation of buffer.

        ::

            >>> server = supriya.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer()
            >>> repr(buffer_)
            '<- Buffer: ???>'

        ::

            >>> buffer_ = buffer_.allocate(server, frame_count=8)
            >>> repr(buffer_)
            '<+ Buffer: 0, 1ch, 8>'

        ::

            >>> buffer_ = buffer_.free()
            >>> repr(buffer_)
            '<- Buffer: ???>'

        Returns string.
        """
        if not self.is_allocated:
            return f"<- {type(self).__name__}: ???>"
        return f"<+ {type(self).__name__}: {self.buffer_id}, {self.channel_count}ch, {self.frame_count}>"

    ### PRIVATE METHODS ###

    def _allocate_buffer_id(self):
        if self.buffer_id is None:
            buffer_id = self.server.buffer_allocator.allocate(1)
            if buffer_id is None:
                ServerObject.free(self)
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
            if not isinstance(channel_indices, Sequence):
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
            del self.server._buffers[buffer_id]
        return buffer_id

    def _unregister_with_remote_server(self, buffer_id):
        import supriya.commands

        on_done = supriya.commands.BufferQueryRequest(buffer_ids=(buffer_id,))
        request = supriya.commands.BufferFreeRequest(
            buffer_id=buffer_id, callback=on_done
        )
        return request

    ### PUBLIC METHODS ###

    def allocate(self, server, channel_count=1, frame_count=1, *, sync=True):
        """
        Allocates buffer on `server`.

        ::

            >>> server = supriya.Server().boot()
            >>> buffer_one = supriya.realtime.Buffer().allocate(server)
            >>> buffer_one.query()
            BufferInfoResponse(
                items=(
                    Item(buffer_id=0, frame_count=1, channel_count=1, sample_rate=4...00.0),
                ),
            )

        ::

            >>> buffer_two = supriya.realtime.Buffer().allocate(
            ...     server,
            ...     frame_count=16,
            ... )
            >>> buffer_two.query()
            BufferInfoResponse(
                items=(
                    Item(buffer_id=1, frame_count=16, channel_count=1, sample_rate=4...00.0),
                ),
            )

        ::

            >>> buffer_three = supriya.realtime.Buffer().allocate(
            ...     server,
            ...     channel_count=2,
            ...     frame_count=32,
            ... )
            >>> buffer_three.query()
            BufferInfoResponse(
                items=(
                    Item(buffer_id=2, frame_count=32, channel_count=2, sample_rate=4...00.0),
                ),
            )

        ::

            >>> buffer_three.allocate(server)
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
        channel_count = int(channel_count)
        frame_count = int(frame_count)
        if channel_count < 1:
            raise ValueError(channel_count)
        if frame_count < 1:
            raise ValueError(frame_count)
        try:
            ServerObject.allocate(self, server=server)
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
        server,
        file_path: PathLike,
        *,
        channel_indices=None,
        callback=None,
        frame_count=None,
        starting_frame=None,
        sync=True,
    ):
        """
        Allocates buffer on `server` with contents read from `file_path`.

        ::

            >>> server = supriya.Server().boot()
            >>> buffer_one = supriya.realtime.Buffer().allocate_from_file(
            ...     server,
            ...     supriya.system.Assets["audio/pulse_44100sr_16bit_octo.wav"],
            ... )
            >>> buffer_one.query()
            BufferInfoResponse(
                items=(
                    Item(buffer_id=0, frame_count=8, channel_count=8, sample_rate=4...00.0),
                ),
            )

        ::

            >>> buffer_two = supriya.realtime.Buffer().allocate_from_file(
            ...     server,
            ...     supriya.system.Assets["audio/pulse_44100sr_16bit_octo.wav"],
            ...     channel_indices=(3, 4),
            ...     frame_count=4,
            ...     starting_frame=1,
            ...     sync=True,
            ... )
            >>> buffer_two.query()
            BufferInfoResponse(
                items=(
                    Item(buffer_id=1, frame_count=4, channel_count=2, sample_rate=4...00.0),
                ),
            )

        ::

            >>> for frame_id in range(buffer_two.frame_count):
            ...     buffer_two.get_frames(frame_id).as_dict()
            ...
            OrderedDict([(0, (0.0, 0.0))])
            OrderedDict([(2, (0.0, 0.0))])
            OrderedDict([(4, (0.999969482421875, 0.0))])
            OrderedDict([(6, (0.0, 0.999969482421875))])

        ::

            >>> buffer_two.allocate(server)
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
            ServerObject.allocate(self, server=server)
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
            ServerObject.allocate(self, server=server)
        return self

    def close(self, *, sync=True):
        """
        Closes buffer, if it was open during a read or write process by
        the DiskIn or DiskOut UGens.

        ::

            >>> server = supriya.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer().allocate(
            ...     server, channel_count=8, frame_count=8
            ... )
            >>> buffer_.read(
            ...     supriya.system.Assets["audio/pulse_44100sr_16bit_octo.wav"],
            ...     leave_open=True,
            ... )
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

    def copy(
        self,
        target_buffer_id,
        *,
        frame_count=None,
        source_starting_frame=None,
        target_starting_frame=None,
        sync=True,
    ):
        """
        Copies data in this buffer into another buffer.

        ::

            >>> server = supriya.Server().boot()
            >>> buffer_one = supriya.realtime.Buffer().allocate(server, frame_count=4)
            >>> buffer_two = supriya.realtime.Buffer().allocate(server, frame_count=4)
            >>> buffer_one.fill((0, 4, 0.5))
            >>> buffer_one.copy(target_buffer_id=buffer_two)
            >>> buffer_two.get_contiguous((0, 4)).as_dict()
            OrderedDict([(0, (0.5, 0.5, 0.5, 0.5))])

        ::

            >>> buffer_one = buffer_one.free()
            >>> buffer_two = buffer_two.free()

        ::

            >>> buffer_one.copy(target_buffer_id=666)
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

    def fill(self, *index_count_value_triples, sync=True):
        """
        Fills contiguous blocks of samples with values.

        ::

            >>> server = supriya.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer().allocate(
            ...     server,
            ...     frame_count=8,
            ...     sync=True,
            ... )
            >>> buffer_.fill((0, 2, 0.5), (3, 3, 1.0))
            >>> buffer_.get_contiguous((0, 8)).as_dict()
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
        request.communicate(server=self.server, sync=sync)

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
        ServerObject.free(self)
        return self

    def fill_via_chebyshev(
        self,
        amplitudes,
        *,
        as_wavetable=False,
        should_normalize=True,
        should_clear_first=True,
        sync=True,
    ):
        """
        Fills buffer with Chebyshev polynomial.

        ::

            >>> server = supriya.Server().boot()
            >>> buffer_ = server.add_buffer(1, 512)
            >>> buffer_.fill_via_chebyshev(
            ...     [1, 0.5, 0.25],
            ...     as_wavetable=False,
            ... )
            >>> supriya.plot(buffer_)  # doctest: +SKIP

        ::

            >>> buffer_ = buffer_.free()

        ::

            >>> buffer_.fill_via_chebyshev([1, 0.5, 0.25])
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
        amplitudes,
        *,
        as_wavetable=False,
        should_clear_first=True,
        should_normalize=True,
        sync=True,
    ):
        """
        Fills buffer with sum of sinusoids via `/b_gen sine1`.

        ::

            >>> server = supriya.Server().boot()
            >>> buffer_ = server.add_buffer(1, 512)
            >>> buffer_.fill_via_sine_1(
            ...     [1, 1, 1],
            ...     as_wavetable=False,
            ... )
            >>> supriya.plot(buffer_)  # doctest: +SKIP

        ::

            >>> buffer_ = buffer_.free()

        ::

            >>> buffer_.fill_via_sine_1([1, 1, 1])
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
        *,
        as_wavetable=False,
        should_clear_first=True,
        should_normalize=True,
        sync=True,
    ):
        """
        Fills buffer with sum of sinusoids via `/b_gen sine2`.

        ::

            >>> server = supriya.Server().boot()
            >>> buffer_ = server.add_buffer(1, 512)
            >>> buffer_.fill_via_sine_2(
            ...     frequencies=[1, 2, 4],
            ...     amplitudes=[1, 0.5, 0.25],
            ...     as_wavetable=False,
            ... )
            >>> supriya.plot(buffer_)  # doctest: +SKIP

        ::

            >>> buffer_ = buffer_.free()

        ::

            >>> buffer_.fill_via_sine_2(
            ...     frequencies=[1, 2, 4],
            ...     amplitudes=[1, 0.5, 0.25],
            ... )
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
        *,
        as_wavetable=False,
        should_clear_first=True,
        should_normalize=True,
        sync=True,
    ):
        """
        Fills buffer with sum of sinusoids via `/b_gen sine3`.

        ::

            >>> server = supriya.Server().boot()
            >>> buffer_ = server.add_buffer(1, 512)
            >>> buffer_.fill_via_sine_3(
            ...     frequencies=[1, 2, 3],
            ...     amplitudes=[1, 0.5, 0.25],
            ...     phases=[0, 0.5, 0],
            ...     as_wavetable=False,
            ... )
            >>> supriya.plot(buffer_)  # doctest: +SKIP

        ::

            >>> buffer_ = buffer_.free()

        ::

            >>> buffer_.fill_via_sine_3(
            ...     frequencies=[1, 2, 3],
            ...     amplitudes=[1, 0.5, 0.25],
            ...     phases=[0, 0.5, 0],
            ... )
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

    def get(self, *indices):
        """
        Gets sample values at `indices`.

        ::

            >>> server = supriya.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer().allocate(
            ...     server,
            ...     frame_count=4,
            ...     sync=True,
            ... )
            >>> response = buffer_.get(1, 2)
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
        request = supriya.commands.BufferGetRequest(buffer_id=self, indices=indices)
        response = request.communicate(server=self.server)
        if isinstance(response, supriya.commands.FailResponse):
            raise IndexError("Index out of range.")
        return response

    def get_contiguous(self, *index_count_pairs):
        """
        Gets contiguous sample values.

        ::

            >>> server = supriya.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer().allocate(
            ...     server,
            ...     frame_count=4,
            ...     sync=True,
            ... )
            >>> response = buffer_.get_contiguous((0, 2), (1, 3))
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

    def get_frames(self, *frame_ids, completion_callback=None):
        """
        Gets frames at `frame_ids`.

        ::

            >>> server = supriya.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer().allocate_from_file(
            ...     server,
            ...     supriya.system.Assets["audio/pulse_44100sr_16bit_octo.wav"],
            ... )
            >>> for frame_id in range(buffer_.frame_count):
            ...     buffer_.get_frames(frame_id).as_dict()
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

            >>> buffer_.get_frames()
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
        response = self.get_contiguous(*index_count_pairs)
        return response

    def normalize(self, *, as_wavetable=None, new_maximum=1.0, sync=True):
        request = supriya.commands.BufferNormalizeRequest(
            as_wavetable=as_wavetable, buffer_id=self, new_maximum=new_maximum
        )
        request.communicate(server=self.server, sync=sync)

    def query(self):
        """
        Queries buffer.

        ::

            >>> server = supriya.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer().allocate(
            ...     server, channel_count=2, frame_count=16
            ... )
            >>> buffer_.query()
            BufferInfoResponse(
                items=(
                    Item(buffer_id=0, frame_count=16, channel_count=2, sample_rate=4...00.0),
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
        *,
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

            >>> server = supriya.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer().allocate(
            ...     server, channel_count=2, frame_count=8
            ... )
            >>> for frame_id in range(buffer_.frame_count):
            ...     buffer_.get_frames(frame_id).as_dict()
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

            >>> file_path = supriya.system.Assets["audio/pulse_44100sr_16bit_octo.wav"]
            >>> buffer_.read(file_path, channel_indices=(0, 1))

        ::

            >>> for frame_id in range(buffer_.frame_count):
            ...     buffer_.get_frames(frame_id).as_dict()
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

    def set(self, *index_value_pairs, sync=False):
        """
        Sets samples.

        ::

            >>> server = supriya.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer().allocate(server, frame_count=8)

        ::

            >>> buffer_.set((0, 0.25), (1, 0.5), (4, 0.75), (5, 1.0))
            >>> buffer_.get_contiguous((0, 8)).as_dict()[0]
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

    def set_contiguous(self, *index_values_pairs, sync=False):
        """
        Sets contiguous blocks of samples.

        ::

            >>> server = supriya.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer().allocate(server, frame_count=8)

        ::

            >>> buffer_.set_contiguous((1, [1, 2, 3]), (4, [-3, 2, -1]))
            >>> buffer_.get_contiguous((0, 8)).as_dict()[0]
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
        *,
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

            >>> server = supriya.Server().boot()
            >>> buffer_one = supriya.realtime.Buffer().allocate_from_file(
            ...     server,
            ...     supriya.system.Assets["audio/pulse_44100sr_16bit_octo.wav"],
            ...     channel_indices=(0,),
            ... )
            >>> buffer_one.get_contiguous((0, 8)).as_dict()[0]
            (0.999969482421875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

        ::

            >>> import os
            >>> file_path = os.path.expanduser("~")
            >>> file_path = os.path.join(file_path, "temp.wav")
            >>> if os.path.exists(file_path):
            ...     os.remove(file_path)

        ::

            >>> buffer_one.write(
            ...     file_path,
            ...     header_format="wav",
            ... )

        ::

            >>> buffer_two = supriya.realtime.Buffer().allocate_from_file(server, file_path)
            >>> buffer_two.get_contiguous((0, 8)).as_dict()[0]
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

    def zero(self, *, callback=None, sync=True):
        """
        Zero all samples in buffer.

        ::

            >>> server = supriya.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer().allocate(server, frame_count=8)

        ::

            >>> buffer_.set_contiguous(
            ...     (0, (1, 2, 3, 4, 5, 6, 7, 8)),
            ...     sync=True,
            ... )

        ::

            >>> buffer_.get_contiguous((0, 8)).as_dict()
            OrderedDict([(0, (1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0))])

        ::

            >>> buffer_.zero()

        ::

            >>> buffer_.get_contiguous((0, 8)).as_dict()
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

            >>> server = supriya.Server().boot()
            >>> buffer_one = supriya.realtime.Buffer().allocate(server, frame_count=8)
            >>> buffer_one.buffer_group is None
            True

        ::

            >>> buffer_group = supriya.realtime.BufferGroup(buffer_count=1)
            >>> buffer_group.allocate(server, frame_count=8)
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

            >>> server = supriya.Server().boot()
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

            >>> buffer_one = buffer_one.allocate(server, frame_count=8)
            >>> buffer_one.buffer_id
            0

        ::

            >>> buffer_group.allocate(server, frame_count=8)
            <+ BufferGroup{4}: 1>

        ::

            >>> for buffer_ in buffer_group:
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

            >>> server = supriya.Server().boot()
            >>> buffer_one = supriya.realtime.Buffer().allocate(server, frame_count=8)

        ::

            >>> buffer_two = supriya.realtime.Buffer().allocate(
            ...     server, channel_count=4, frame_count=8
            ... )

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

            >>> server = supriya.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer()
            >>> buffer_.duration_in_seconds
            0.0

        ::

            >>> buffer_ = buffer_.allocate(server, frame_count=44100)
            >>> buffer_.duration_in_seconds == buffer_.frame_count / buffer_.sample_rate
            True

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

            >>> server = supriya.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer()
            >>> buffer_.frame_count
            0

        ::

            >>> buffer_ = buffer_.allocate(server, frame_count=512)
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

            >>> server = supriya.Server().boot()
            >>> buffer_one = supriya.realtime.Buffer().allocate(server, frame_count=16)
            >>> buffer_two = supriya.realtime.Buffer().allocate(
            ...     server,
            ...     channel_count=2,
            ...     frame_count=16,
            ... )
            >>> buffer_three = supriya.realtime.Buffer().allocate(
            ...     server,
            ...     channel_count=8,
            ...     frame_count=16,
            ... )

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

            >>> server = supriya.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer()
            >>> buffer_.sample_rate
            0

        ::

            >>> buffer_ = buffer_.allocate(server, frame_count=8)
            >>> buffer_.sample_rate
            4...00.0

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

            >>> server = supriya.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer()
            >>> buffer_.is_allocated
            False

        ::

            >>> buffer_ = buffer_.allocate(server, frame_count=8)
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

            >>> server = supriya.Server().boot()
            >>> buffer_ = supriya.realtime.Buffer()
            >>> buffer_.server is None
            True

        ::

            >>> buffer_ = buffer_.allocate(server, frame_count=8)
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


class BufferGroup(ServerObject):
    """
    A buffer group.

    ::

        >>> server = supriya.Server().boot()

    ::

        >>> buffer_group = supriya.realtime.BufferGroup(buffer_count=4)
        >>> buffer_group
        <- BufferGroup{4}: ???>

    ::

        >>> buffer_group.allocate(
        ...     server,
        ...     frame_count=8192,
        ...     sync=True,
        ... )
        <+ BufferGroup{4}: 0>

    ::

        >>> buffer_group.free()
        <- BufferGroup{4}: ???>

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_buffer_id", "_buffers")

    ### INITIALIZER ###

    def __init__(self, buffer_count=1):
        ServerObject.__init__(self)
        self._buffer_id = None
        buffer_count = int(buffer_count)
        assert 0 < buffer_count
        self._buffers = tuple(
            Buffer(buffer_group_or_index=self) for _ in range(buffer_count)
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
        buffer_id = self.buffer_id
        if buffer_id is None:
            buffer_id = "???"
        string = "<{} {}{{{}}}: {}>".format(
            "+" if self.is_allocated else "-", type(self).__name__, len(self), buffer_id
        )
        return string

    ### PRIVATE METHODS ###

    def _register_with_local_server(self, server):
        ServerObject.allocate(self, server=server)
        allocator = self.server.buffer_allocator
        buffer_id = allocator.allocate(len(self))
        if buffer_id is None:
            ServerObject.free(self)
            raise ValueError
        self._buffer_id = buffer_id
        for buffer_ in self:
            buffer_._register_with_local_server()
        return buffer_id

    ### PUBLIC METHODS ###

    def allocate(self, server, channel_count=1, frame_count=None, sync=True):
        """
        Allocates buffer group.

        Returns buffer group.
        """
        if self.is_allocated:
            return supriya.exceptions.BufferAlreadyAllocated
        channel_count = int(channel_count)
        frame_count = int(frame_count)
        assert 0 < channel_count
        assert 0 < frame_count
        self._register_with_local_server(server)
        requests = []
        for buffer_ in self:
            requests.append(
                buffer_._register_with_remote_server(
                    channel_count=channel_count, frame_count=frame_count
                )
            )
        supriya.commands.RequestBundle(contents=requests).communicate(
            server=server, sync=sync
        )
        return self

    def free(self) -> "BufferGroup":
        """
        Frees all buffers in buffer group.
        """
        if not self.is_allocated:
            raise supriya.exceptions.BufferNotAllocated
        for buffer_ in self:
            buffer_.free()
        buffer_id = self.buffer_id
        self._buffer_id = None
        self.server.buffer_allocator.free(buffer_id)
        ServerObject.free(self)
        return self

    def index(self, item):
        return self.buffers.index(item)

    @staticmethod
    def from_file_paths(server, file_paths, sync=True):
        """
        Create a buffer group from `file_paths`.

        ::

            >>> file_paths = supriya.Assets["audio/*mono_1s*"]
            >>> len(file_paths)
            4

        ::

            >>> server = supriya.Server().boot()
            >>> buffer_group = supriya.realtime.BufferGroup.from_file_paths(server, file_paths)

        ::

            >>> for buffer_ in buffer_group:
            ...     buffer_
            ...
            <+ Buffer: 0, 1ch, 44100>
            <+ Buffer: 1, 1ch, 44100>
            <+ Buffer: 2, 1ch, 44100>
            <+ Buffer: 3, 1ch, 44100>

        Returns buffer group.
        """
        for file_path in file_paths:
            assert os.path.exists(file_path)
        buffer_group = BufferGroup(buffer_count=len(file_paths))
        buffer_group._register_with_local_server(server)
        requests = []
        for buffer_, file_path in zip(buffer_group.buffers, file_paths):
            request = buffer_._register_with_remote_server(file_path=file_path)
            requests.append(request)
        supriya.commands.RequestBundle(contents=requests).communicate(server, sync=sync)
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


class BufferProxy(SupriyaValueObject):
    """
    A buffer proxy.

    Acts as a singleton reference to a buffer on the server, tracking the state
    of a single buffer id and responding to `/b_info` messages. Multiple Buffer
    instances reference a single BufferProxy.

    BufferProxy instances are created internally by the server, and should be
    treated as an implementation detail.

    ::

        >>> server = supriya.Server()
        >>> buffer_proxy = supriya.realtime.BufferProxy(
        ...     buffer_id=0,
        ...     server=server,
        ...     channel_count=2,
        ...     frame_count=441,
        ...     sample_rate=44100,
        ... )
        >>> buffer_proxy
        BufferProxy(
            buffer_id=0,
            channel_count=2,
            frame_count=441,
            sample_rate=44100,
            server=<Server: offline>,
        )

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_buffer_id",
        "_channel_count",
        "_frame_count",
        "_sample_rate",
        "_server",
    )

    ### INITIALIZER ###

    def __init__(
        self, buffer_id=None, channel_count=0, frame_count=0, sample_rate=0, server=None
    ):
        import supriya.realtime

        buffer_id = int(buffer_id)
        assert 0 <= buffer_id
        assert isinstance(server, supriya.realtime.Server)
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

            >>> server = supriya.Server()
            >>> buffer_proxy = supriya.realtime.BufferProxy(
            ...     buffer_id=0,
            ...     server=server,
            ...     channel_count=2,
            ...     frame_count=441,
            ...     sample_rate=44100,
            ... )
            >>> float(buffer_proxy)
            0.0

        Returns float.
        """
        return float(self.buffer_id)

    def __int__(self):
        """
        Gets integer representation of buffer proxy.

        ::

            >>> server = supriya.Server()
            >>> buffer_proxy = supriya.realtime.BufferProxy(
            ...     buffer_id=0,
            ...     server=server,
            ...     channel_count=2,
            ...     frame_count=441,
            ...     sample_rate=44100,
            ... )
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

            >>> server = supriya.Server()
            >>> a_buffer = supriya.realtime.BufferProxy(
            ...     buffer_id=23,
            ...     channel_count=1,
            ...     frame_count=256,
            ...     sample_rate=44100,
            ...     server=server,
            ... )
            >>> a_buffer
            BufferProxy(
                buffer_id=23,
                channel_count=1,
                frame_count=256,
                sample_rate=44100,
                server=<Server: offline>,
            )

        ::

            >>> response_item = supriya.commands.BufferInfoResponse.Item(
            ...     buffer_id=23,
            ...     channel_count=2,
            ...     frame_count=512,
            ...     sample_rate=44100,
            ... )

        ::

            >>> a_buffer._handle_response(response_item)
            >>> a_buffer
            BufferProxy(
                buffer_id=23,
                channel_count=2,
                frame_count=512,
                sample_rate=44100,
                server=<Server: offline>,
            )

        Returns none.
        """
        import supriya.commands

        if isinstance(response, supriya.commands.BufferInfoResponse.Item):
            assert response.buffer_id == self.buffer_id
            self._channel_count = response.channel_count
            self._frame_count = response.frame_count
            self._sample_rate = response.sample_rate

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        """
        Gets buffer id of buffer proxy.

        ::

            >>> server = supriya.Server()
            >>> buffer_proxy = supriya.realtime.BufferProxy(
            ...     buffer_id=0,
            ...     server=server,
            ...     channel_count=2,
            ...     frame_count=441,
            ...     sample_rate=44100,
            ... )
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

            >>> server = supriya.Server()
            >>> buffer_proxy = supriya.realtime.BufferProxy(
            ...     buffer_id=0,
            ...     server=server,
            ...     channel_count=2,
            ...     frame_count=441,
            ...     sample_rate=44100,
            ... )
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

            >>> server = supriya.Server()
            >>> buffer_proxy = supriya.realtime.BufferProxy(
            ...     buffer_id=0,
            ...     server=server,
            ...     channel_count=2,
            ...     frame_count=441,
            ...     sample_rate=44100,
            ... )
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

            >>> server = supriya.Server()
            >>> buffer_proxy = supriya.realtime.BufferProxy(
            ...     buffer_id=0,
            ...     server=server,
            ...     channel_count=2,
            ...     frame_count=441,
            ...     sample_rate=44100,
            ... )
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

            >>> server = supriya.Server()
            >>> buffer_proxy = supriya.realtime.BufferProxy(
            ...     buffer_id=0,
            ...     server=server,
            ...     channel_count=2,
            ...     frame_count=441,
            ...     sample_rate=44100,
            ... )
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

            >>> server = supriya.Server()
            >>> buffer_proxy = supriya.realtime.BufferProxy(
            ...     buffer_id=0,
            ...     server=server,
            ...     channel_count=2,
            ...     frame_count=441,
            ...     sample_rate=44100,
            ... )
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

            >>> server = supriya.Server()
            >>> buffer_proxy = supriya.realtime.BufferProxy(
            ...     buffer_id=0,
            ...     server=server,
            ...     channel_count=2,
            ...     frame_count=441,
            ...     sample_rate=44100,
            ... )
            >>> buffer_proxy.server
            <Server: offline>

        Returns server.
        """
        return self._server
