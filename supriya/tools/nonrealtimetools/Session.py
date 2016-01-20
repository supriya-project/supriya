# -*- encoding: utf-8 -*-
import bisect
import collections
import hashlib
import os
import shutil
import struct
import subprocess
import tempfile
from abjad.tools import mathtools
from supriya.tools import osctools
from supriya.tools import requesttools
from supriya.tools import servertools
from supriya.tools import soundfiletools
from supriya.tools import synthdeftools
from supriya.tools.osctools.OscMixin import OscMixin


class Session(OscMixin):
    r'''A non-realtime session.

    ::

        >>> from supriya.tools import nonrealtimetools
        >>> session = nonrealtimetools.Session()

    ::

        >>> from supriya.tools import synthdeftools
        >>> from supriya.tools import ugentools
        >>> builder = synthdeftools.SynthDefBuilder(frequency=440)
        >>> with builder:
        ...     out = ugentools.Out.ar(
        ...         source=ugentools.SinOsc.ar(
        ...             frequency=builder['frequency'],
        ...             )
        ...         )
        ...
        >>> synthdef = builder.build()

    ::

        >>> with session.at(0):
        ...     synth_a = session.add_synth(duration=10, synthdef=synthdef)
        ...     synth_b = session.add_synth(duration=15, synthdef=synthdef)
        ...
        >>> with session.at(5):
        ...     synth_c = session.add_synth(duration=10, synthdef=synthdef)
        ...

    ::

        >>> session.to_osc_bundles()
        []

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_active_moments',
        '_audio_input_bus_group',
        '_audio_output_bus_group',
        '_buses',
        '_input_count',
        '_moments',
        '_nodes',
        '_offsets',
        '_output_count',
        '_root_node',
        )

    _prioritized_request_types = [
        requesttools.SynthDefReceiveRequest,
        requesttools.ControlBusSetRequest,
        requesttools.GroupNewRequest,
        requesttools.NodeOrderRequest,
        requesttools.SynthNewRequest,
        requesttools.NodeMapToAudioBusRequest,
        requesttools.NodeMapToControlBusRequest,
        requesttools.NodeSetRequest,
        ]

    ### INITIALIZER ###

    def __init__(self, input_count=0, output_count=2):
        from supriya.tools import nonrealtimetools
        self._active_moments = []
        self._moments = {}
        self._nodes = set()
        self._offsets = []
        self._root_node = nonrealtimetools.RootNode(self)
        self._setup_initial_moments()
        self._setup_buses(input_count, output_count)

    ### PRIVATE METHODS ###

    def _build_bus_id_mapping(self):
        input_count = self._input_count or 0
        output_count = self._output_count or 0
        first_private_bus_id = input_count + output_count
        audio_bus_allocator = servertools.BlockAllocator(
            heap_minimum=first_private_bus_id,
            )
        control_bus_allocator = servertools.BlockAllocator()
        mapping = {}
        if output_count:
            bus_group = self.audio_output_bus_group
            for bus_id, bus in enumerate(bus_group):
                mapping[bus] = bus_id
        if input_count:
            bus_group = self.audio_input_bus_group
            for bus_id, bus in enumerate(bus_group, output_count):
                mapping[bus] = bus_id
        for bus in self._buses:
            if bus in mapping:
                continue
            if bus.calculation_rate == synthdeftools.CalculationRate.AUDIO:
                allocator = audio_bus_allocator
            else:
                allocator = control_bus_allocator
            if bus.bus_group is None:
                mapping[bus] = allocator.allocate(1)
            else:
                block_id = allocator.allocate(len(bus.bus_group))
                mapping[bus.bus_group] = block_id
                for bus_id in range(block_id, block_id + len(bus.bus_group)):
                    mapping[bus] = bus_id
        return mapping

    def _build_command(
        self,
        output_filename,
        input_filename=None,
        sample_rate=44100,
        header_format=soundfiletools.HeaderFormat.AIFF,
        sample_format=soundfiletools.SampleFormat.INT24,
        **kwargs
        ):
        r'''Builds non-realtime rendering command.

        ::

            >>> session._build_command('output.aiff')
            'scsynth -N {} _ output.aiff 44100 aiff int24'

        '''
        parts = ['scsynth', '-N', '{}']
        if input_filename:
            parts.append(os.path.expanduser(input_filename))
        else:
            parts.append('_')
        parts.append(os.path.expanduser(output_filename))
        parts.append(str(int(sample_rate)))
        header_format = soundfiletools.HeaderFormat.from_expr(header_format)
        parts.append(header_format.name.lower())  # Must be lowercase.
        sample_format = soundfiletools.SampleFormat.from_expr(sample_format)
        parts.append(sample_format.name.lower())  # Must be lowercase.
        server_options = servertools.ServerOptions(**kwargs)
        server_options = server_options.as_options_string(realtime=False)
        if server_options:
            parts.append(server_options)
        command = ' '.join(parts)
        return command

    def _build_id_mapping(self):
        id_mapping = {}
        id_mapping.update(self._build_bus_id_mapping())
        id_mapping.update(self._build_synth_id_mapping())
        return id_mapping

    def _build_synth_id_mapping(self):
        allocator = servertools.NodeIdAllocator()
        mapping = {}
        for offset in self.offsets[1:]:
            moment = self.moments[offset]
            for start_node in moment.start_nodes:
                mapping[start_node] = allocator.allocate_node_id()
        return mapping

    def _find_moment_after(self, offset):
        index = bisect.bisect(self.offsets, offset)
        if index < len(self.offsets):
            old_offset = self.offsets[index]
            if offset < old_offset:
                return self.moments[old_offset]
        return None

    def _find_moment_at(self, offset):
        return self.moments.get(offset, None)

    def _find_moment_before(self, offset):
        index = bisect.bisect_left(self.offsets, offset)
        if index == len(self.offsets):
            index -= 1
        old_offset = self.offsets[index]
        if offset <= old_offset:
            index -= 1
        if index < 0:
            return None
        old_offset = self.offsets[index]
        return self.moments[old_offset]

    def _process_terminal_event(self, final_offset, timespan):
        osc_bundles = []
        if timespan is not None:
            prototype = (mathtools.Infinity(), mathtools.NegativeInfinity)
            if timespan.stop_offset not in prototype and \
                final_offset < timespan.stop_offset:
                osc_bundle = osctools.OscBundle(
                    timestamp=float(timespan.stop_offset),
                    contents=[osctools.OscMessage(0)],
                    )
                osc_bundles.append(osc_bundle)
        return osc_bundles

    def _setup_buses(self, input_count, output_count):
        from supriya.tools import nonrealtimetools
        self._buses = collections.OrderedDict()
        input_count = int(input_count or 0)
        assert 0 <= input_count
        self._input_count = input_count
        output_count = int(output_count or 0)
        assert 0 <= output_count
        self._output_count = output_count
        audio_input_bus_group = None
        if self._input_count:
            audio_input_bus_group = nonrealtimetools.AudioInputBusGroup(self)
        self._audio_input_bus_group = audio_input_bus_group
        audio_output_bus_group = None
        if self._output_count:
            audio_output_bus_group = nonrealtimetools.AudioOutputBusGroup(self)
        self._audio_output_bus_group = audio_output_bus_group

    def _setup_initial_moments(self):
        from supriya.tools import nonrealtimetools
        offset = float('-inf')
        moment = nonrealtimetools.Moment(self, offset)
        moment.nodes_to_children[self.root_node] = None
        moment.nodes_to_parents[self.root_node] = None
        self.moments[offset] = moment
        self.offsets.append(offset)
        offset = 0
        moment = moment._clone(offset)
        self.moments[offset] = moment
        self.offsets.append(offset)

    ### PUBLIC METHODS ###

    def at(self, offset):
        assert 0 <= offset
        moment = self._find_moment_at(offset)
        if moment:
            return moment
        old_moment = self._find_moment_before(offset)
        new_moment = old_moment._clone(offset)
        self.moments[offset] = new_moment
        self.offsets.insert(
            self.offsets.index(old_moment.offset) + 1,
            offset,
            )
        return new_moment

    def add_group(
        self,
        add_action=None,
        ):
        return self.root_node.add_group(add_action=add_action)

    def add_synth(
        self,
        add_action=None,
        duration=None,
        synthdef=None,
        **synth_kwargs
        ):
        return self.root_node.add_synth(
            add_action=add_action,
            duration=duration,
            synthdef=synthdef,
            **synth_kwargs
            )

    def move_node(
        self,
        node,
        add_action=None,
        ):
        self.root_node.move_node(node, add_action=add_action)

    def render(
        self,
        output_filename,
        input_filename=None,
        timespan=None,
        sample_rate=44100,
        header_format=soundfiletools.HeaderFormat.AIFF,
        sample_format=soundfiletools.SampleFormat.INT24,
        debug=False,
        **kwargs
        ):
        datagram = self.to_datagram(timespan=timespan)
        md5 = hashlib.md5()
        md5.update(datagram)
        md5 = md5.hexdigest()
        temp_directory_path = tempfile.mkdtemp()
        file_path = os.path.join(temp_directory_path, '{}.osc'.format(md5))
        with open(file_path, 'wb') as file_pointer:
            file_pointer.write(datagram)
        command = self._build_command(
            output_filename,
            input_filename=None,
            sample_rate=sample_rate,
            header_format=header_format,
            sample_format=sample_format,
            **kwargs
            )
        command = command.format(file_path)
        exit_code = subprocess.call(command, shell=True)
        if debug:
            return exit_code, file_path
        else:
            shutil.rmtree(temp_directory_path)
            return exit_code, None

    def report(self):
        states = []
        for offset in self.offsets[1:]:
            moment = self.moments[offset]
            state = moment.report()
            states.append(state)
        return states

    def to_datagram(self, timespan=None):
        osc_bundles = self.to_osc_bundles(timespan=timespan)
        datagrams = []
        for osc_bundle in osc_bundles:
            datagram = osc_bundle.to_datagram(realtime=False)
            size = len(datagram)
            size = struct.pack('>i', size)
            datagrams.append(size)
            datagrams.append(datagram)
        datagram = b''.join(datagrams)
        return datagram

    def to_osc_bundles(self, timespan=None):
        osc_bundles = []
        id_mapping = self._build_id_mapping()
        visited_synthdefs = set()
        offsets = self.offsets[1:]
        for i, offset in enumerate(offsets, 1):
            moment = self.moments[offset]
            requests = moment.to_requests(id_mapping, visited_synthdefs)
            osc_messages = [request.to_osc_message(True)
                for request in requests]
            if i == len(offsets):
                osc_message = osctools.OscMessage(0)
                osc_messages.append(osc_message)
            if osc_messages:
                osc_bundle = osctools.OscBundle(
                    timestamp=offset,
                    contents=osc_messages,
                    )
                osc_bundles.append(osc_bundle)
        return osc_bundles

    ### PUBLIC PROPERTIES ###

    @property
    def active_moments(self):
        return self._active_moments

    @property
    def audio_input_bus_group(self):
        return self._audio_input_bus_group

    @property
    def audio_output_bus_group(self):
        return self._audio_output_bus_group

    @property
    def buses(self):
        return self._buses

    @property
    def input_count(self):
        return self._input_count

    @property
    def moments(self):
        return self._moments

    @property
    def nodes(self):
        return self._nodes

    @property
    def offsets(self):
        return self._offsets

    @property
    def output_count(self):
        return self._output_count

    @property
    def root_node(self):
        return self._root_node
