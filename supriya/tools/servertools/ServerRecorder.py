# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class ServerRecorder(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_channel_count',
        '_current_channel_count',
        '_current_header_format',
        '_current_file_path',
        '_current_sample_format',
        '_header_format',
        '_is_recording',
        '_record_buffer',
        '_record_node',
        '_record_synthdef',
        '_sample_format',
        '_server',
        )

    ### INITIALIZER ###

    def __init__(self, server):
        from supriya.tools import soundfiletools
        self._server = server
        server_options = server.server_options
        self._channel_count = server_options.output_bus_channel_count
        self._header_format = soundfiletools.HeaderFormat.AIFF
        self._sample_format = soundfiletools.SampleFormat.INT24
        self._current_channel_count = self._channel_count
        self._current_file_path = None
        self._current_header_format = self._header_format
        self._current_sample_format = self._sample_format
        self._record_node = None
        self._is_recording = False

    ### PRIVATE METHODS ###

    def _cache_properties(self):
        self._current_header_format = self.header_format
        self._current_sample_format = self.sample_format
        self._current_channel_count = self._channel_count

    def _get_file_path(self, file_path=None):
        pass

    def _get_record_buffer_id(self):
        return 0

    def _setup_buffer(self, file_path):
        from supriya.tools import requesttools
        from supriya.tools import servertools
        buffer_id = self._get_record_buffer_id()
        buffer_ = servertools.Buffer(buffer_id)
        frame_count = 65536 * 16
        completion_message = requesttools.BufferWriteRequest(
            buffer_id=buffer_id,
            file_path=file_path,
            header_format=self.current_header_format,
            sample_format=self.current_sample_format,
            leave_open=True,
            )
        buffer_.allocate(
            frame_count=frame_count,
            channel_count=self.channel_count,
            completion_message=completion_message,
            )
        self._buffer = buffer_

    def _setup_synthdef(self):
        from supriya.tools import synthdeftools
        from supriya.tools import ugentools
        with synthdeftools.SynthDefBuilder() as builder:
            source = ugentools.In.ar(
                bus=0,
                channel_count=self.channel_count,
                )
            ugentools.DiskOut.ar(
                buffer_id=self.record_buffer,
                source=source,
                )
        synthdef = builder.build_synthdef()
        synthdef.allocate(server=self.server)
        self._record_synthdef = synthdef

    def _setup_node(self):
        pass

    ### PUBLIC METHODS ###

    def pause(self):
        if self.record_node is not None:
            self.record_node.pause()
        else:
            raise Exception

    def prepare(self, file_path=None):
        if self.is_recording:
            raise Exception
        self._current_file_path = self._get_file_path(file_path)
        self._cache_properties()
        self._setup_buffer(file_path=self.current_file_path)
        self._setup_synthdef()
        self._setup_node()

    def start(self, file_path=None):
        if self.record_node is not None:
            raise Exception('Already recording.')
        self.prepare(file_path=file_path)

    def stop(self):
        pass

    def unpause(self):
        if self.record_node is not None:
            self.record_node.unpause()
        else:
            raise Exception

    ### PUBLIC PROPERTIES ###

    @property
    def is_recording(self):
        return self._is_recording

    @property
    def record_buffer(self):
        return self._record_buffer

    @property
    def record_node(self):
        return self._record_node

    @property
    def channel_count(self):
        return self._channel_count

    @channel_count.setter
    def channel_count(self, expr):
        channel_count = int(expr)
        assert 0 < channel_count
        self._channel_count = channel_count

    @property
    def sample_format(self):
        return self._sample_format

    @sample_format.setter
    def sample_format(self, expr):
        from supriya.tools import soundfiletools
        sample_format = soundfiletools.SampleFormat.from_expr(expr)
        self._sample_format = sample_format

    @property
    def header_format(self):
        return self._header_format

    @header_format.setter
    def header_format(self, expr):
        from supriya.tools import soundfiletools
        header_format = soundfiletools.HeaderFormat.from_expr(expr)
        self._header_format = header_format

    @property
    def current_channel_count(self):
        return self._current_channel_count

    @property
    def current_file_path(self):
        return self._current_file_path

    @property
    def current_sample_format(self):
        return self._current_sample_format

    @property
    def current_header_format(self):
        return self._current_header_format