# -*- encoding: utf-8 -*-
import bisect
import collections
import hashlib
import os
import shutil
import struct
import subprocess
import tempfile
from abjad.tools import documentationtools
from supriya.tools import osctools
from supriya.tools import requesttools
from supriya.tools import servertools
from supriya.tools import soundfiletools
from supriya.tools import synthdeftools
from supriya.tools import timetools
from supriya.tools.osctools.OscMixin import OscMixin
try:
    from queue import PriorityQueue
except ImportError:
    from Queue import PriorityQueue


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

        >>> import pprint
        >>> result = session.to_lists(duration=20)
        >>> pprint.pprint(result)
        [[0.0,
          [['/d_recv',
            bytearray(b'SCgf\x00\x00\x00\x02\x00\x01 9c4eb4778dc0faf39459fa8a5cd45'
                      b'c19\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01C'
                      b'\xdc\x00\x00\x00\x00\x00\x01\tfrequency\x00\x00\x00'
                      b'\x00\x00\x00\x00\x03\x07Control\x01\x00\x00\x00\x00\x00\x00'
                      b'\x00\x01\x00\x00\x01\x06SinOsc\x02\x00\x00\x00\x02\x00\x00\x00'
                      b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff'
                      b'\xff\xff\xff\x00\x00\x00\x00\x02\x03Out\x02\x00\x00\x00'
                      b'\x02\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00'
                      b'\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00')],
           ['/s_new', '9c4eb4778dc0faf39459fa8a5cd45c19', 1000, 0, 0],
           ['/s_new', '9c4eb4778dc0faf39459fa8a5cd45c19', 1001, 0, 0]]],
         [5.0, [['/s_new', '9c4eb4778dc0faf39459fa8a5cd45c19', 1002, 0, 0]]],
         [10.0, [['/n_free', 1000]]],
         [15.0, [['/n_free', 1001, 1002]]],
         [20.0, [[0]]]]

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_active_moments',
        '_audio_input_bus_group',
        '_audio_output_bus_group',
        '_buffers',
        '_buses',
        '_input_count',
        '_nodes',
        '_offsets',
        '_output_count',
        '_root_node',
        '_session_ids',
        '_states',
        )

    _ordered_buffer_post_alloc_request_types = (
        requesttools.BufferReadRequest,
        requesttools.BufferReadChannelRequest,
        requesttools.BufferZeroRequest,
        requesttools.BufferFillRequest,
        requesttools.BufferGenerateRequest,
        requesttools.BufferSetRequest,
        requesttools.BufferSetContiguousRequest,
        requesttools.BufferNormalizeRequest,
        requesttools.BufferCopyRequest,
        )

    _ordered_buffer_pre_free_request_types = (
        requesttools.BufferWriteRequest,
        #requesttools.BufferCloseRequest,  # should be automatic
        )

    ### INITIALIZER ###

    def __init__(self, input_count=0, output_count=2):
        from supriya.tools import nonrealtimetools
        self._active_moments = []
        self._session_ids = {}
        self._states = {}
        self._buffers = timetools.TimespanCollection()
        self._nodes = timetools.TimespanCollection()
        self._offsets = []
        self._root_node = nonrealtimetools.RootNode(self)
        self._setup_initial_states()
        self._setup_buses(input_count, output_count)

    ### SPECIAL METHODS ###

    def __graph__(self, include_controls=False):
        from supriya.tools import nonrealtimetools
        graph = documentationtools.GraphvizGraph()
        for offset, state in sorted(self.states.items()):
            if float('-inf') < offset:
                self._apply_transitions(state.offset)
            state_graph = state.__graph__(include_controls=include_controls)
            subgraph = documentationtools.GraphvizSubgraph()
            subgraph.extend(state_graph.children)
            subgraph.attributes['label'] = str(offset)
            graph.append(subgraph)
        nonrealtimetools.StateGrapher._style_graph(graph)
        return graph

    ### PRIVATE METHODS ###

    def _apply_transitions(self, offsets, chain=True):
        from supriya.tools import nonrealtimetools
        if nonrealtimetools.DoNotPropagate._stack:
            return
        queue = PriorityQueue()
        try:
            for offset in offsets:
                queue.put(offset)
        except TypeError:
            queue.put(offsets)
        previous_offset = None
        while not queue.empty():
            offset = queue.get()
            if offset == previous_offset:
                continue
            previous_offset = offset
            state = self._find_state_at(offset, clone_if_missing=False)
            if state is None:
                continue
            # TODO: automatically handle sparsifying here.
            #elif state.is_sparse and 0 < offset:
            #    print('SPARSE', state.offset, state.start_nodes, state.stop_nodes,
            #        state.nodes_to_children)
            #    state._sparsify()
            #    changed = True
            previous_state = self._find_state_before(
                offset, with_node_tree=True)
            assert previous_state is not None
            result = nonrealtimetools.State._apply_transitions(
                state.transitions,
                previous_state.nodes_to_children,
                previous_state.nodes_to_parents,
                state.stop_nodes,
                )
            nodes_to_children, nodes_to_parents = result
            changed = False
            if nodes_to_children != state.nodes_to_children:
                state._nodes_to_children = nodes_to_children
                state._nodes_to_parents = nodes_to_parents
                changed = True
            if changed and chain:
                next_state = self._find_state_after(
                    offset,
                    with_node_tree=True,
                    )
                if next_state is not None:
                    queue.put(next_state.offset)

    def _build_id_mapping(self):
        id_mapping = {}
        id_mapping.update(self._build_id_mapping_for_buffers())
        id_mapping.update(self._build_id_mapping_for_buses())
        id_mapping.update(self._build_id_mapping_for_nodes())
        return id_mapping

    def _build_id_mapping_for_buffers(self):
        mapping = {}
        for buffer_ in self._buffers:
            if buffer_ in mapping:
                continue
            if buffer_.buffer_group is None:
                mapping[buffer_] = buffer_.session_id
            else:
                initial_id = buffer_.buffer_group[0].session_id
                mapping[buffer_.buffer_group] = initial_id
                for child in buffer_.buffer_group:
                    mapping[child] = child.session_id
        return mapping

    def _build_id_mapping_for_buses(self):
        input_count = self._input_count or 0
        output_count = self._output_count or 0
        first_private_bus_id = input_count + output_count
        allocators = {
            synthdeftools.CalculationRate.AUDIO: servertools.BlockAllocator(
                heap_minimum=first_private_bus_id,
                ),
            synthdeftools.CalculationRate.CONTROL: servertools.BlockAllocator(),
            }
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
            allocator = allocators[bus.calculation_rate]
            if bus.bus_group is None:
                mapping[bus] = allocator.allocate(1)
            else:
                block_id = allocator.allocate(len(bus.bus_group))
                mapping[bus.bus_group] = block_id
                for bus_id in range(block_id, block_id + len(bus.bus_group)):
                    mapping[bus] = bus_id
        return mapping

    def _build_id_mapping_for_nodes(self):
        allocator = servertools.NodeIdAllocator()
        mapping = {self.root_node: 0}
        for offset in self.offsets[1:]:
            state = self.states[offset]
            nodes = sorted(state.start_nodes, key=lambda x: x.session_id)
            for node in nodes:
                mapping[node] = allocator.allocate_node_id()
                mapping[node] = node.session_id
        return mapping

    def _build_render_command(
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

            >>> session._build_render_command('output.aiff')
            'scsynth -N {} _ output.aiff 44100 aiff int24'

        '''
        from abjad.tools import systemtools
        scsynth_path = 'scsynth'
        if not systemtools.IOManager.find_executable('scsynth'):
            found_scsynth = False
            for path in (
                '/Applications/SuperCollider/SuperCollider.app/Contents/MacOS/scsynth',  # pre-7
                '/Applications/SuperCollider/SuperCollider.app/Contents/Resources/scsynth',  # post-7
                ):
                if os.path.exists(path):
                    scsynth_path = path
                    found_scsynth = True
            if not found_scsynth:
                raise Exception('Cannot find scsynth. Is it on your $PATH?')
        parts = [scsynth_path, '-N', '{}']
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

    def _collect_bus_set_requests(self, bus_settings, offset):
        requests = []
        if offset in bus_settings:
            index_value_pairs = sorted(bus_settings[offset].items())
            request = requesttools.ControlBusSetRequest(
                index_value_pairs=index_value_pairs,
                )
            requests.append(request)
        return requests

    def _collect_buffer_allocate_requests(
        self,
        buffer_open_states,
        id_mapping,
        start_buffers,
        ):
        requests = []
        if start_buffers:
            for buffer_ in sorted(start_buffers, key=lambda x: x.session_id):
                arguments = dict(
                    buffer_id=id_mapping[buffer_],
                    frame_count=buffer_.frame_count,
                    )
                request_class = requesttools.BufferAllocateRequest
                if buffer_.file_path is not None:
                    request_class = requesttools.BufferAllocateReadRequest
                    arguments['file_path'] = buffer_.file_path
                    arguments['starting_frame'] = buffer_.starting_frame
                    channel_indices = buffer_.channel_count
                    if isinstance(channel_indices, int):
                        channel_indices = tuple(range(buffer_.channel_count))
                        arguments['channel_indices'] = channel_indices
                        request_class = requesttools.BufferAllocateReadChannelRequest
                    elif isinstance(buffer_.channel_count, tuple):
                        arguments['channel_indices'] = channel_indices
                        request_class = requesttools.BufferAllocateReadChannelRequest
                else:
                    arguments['channel_count'] = buffer_.channel_count or 1
                    arguments['frame_count'] = arguments['frame_count'] or 1
                try:
                    request = request_class(**arguments)
                except TypeError:
                    print(request_class, arguments)
                    raise
                requests.append(request)
                buffer_open_states[id_mapping[buffer_]] = False
        return requests

    def _collect_buffer_free_requests(
        self,
        buffer_open_states,
        id_mapping,
        stop_buffers,
        ):
        requests = []
        if stop_buffers:
            for buffer_ in sorted(stop_buffers, key=lambda x: x.session_id):
                if buffer_open_states[id_mapping[buffer_]]:
                    close_request = requesttools.BufferCloseRequest(
                        buffer_id=id_mapping[buffer_],
                        )
                    requests.append(close_request)
                request = requesttools.BufferFreeRequest(
                    buffer_id=id_mapping[buffer_],
                    )
                requests.append(request)
                del(buffer_open_states[id_mapping[buffer_]])
        return requests

    def _collect_buffer_nonlifecycle_requests(
        self,
        all_buffers,
        buffer_open_states,
        buffer_settings,
        id_mapping,
        offset,
        request_types,
        ):
        requests = []
        buffer_settings = buffer_settings.get(offset)
        if not buffer_settings:
            return requests
        for request_type in request_types:
            buffer_requests = buffer_settings.get(request_type)
            if not buffer_requests:
                continue
            if request_type in (
                requesttools.BufferReadRequest,
                requesttools.BufferReadChannelRequest,
                requesttools.BufferWriteRequest,
                ):
                for request in buffer_requests:
                    buffer_id = request.buffer_id
                    open_state = buffer_open_states[buffer_id]
                    if open_state:
                        close_request = requesttools.BufferCloseRequest(
                            buffer_id=buffer_id,
                            )
                        requests.append(close_request)
                    requests.append(request)
                    open_state = bool(request.leave_open)
                    buffer_open_states[buffer_id] = open_state
            else:
                requests.extend(buffer_requests)
        return requests

    def _collect_buffer_settings(self, id_mapping):
        buffer_settings = {}
        for buffer_ in sorted(self._buffers, key=lambda x: id_mapping[x]):
            for event_type, events in buffer_._events.items():
                for offset, payload in events:
                    payload = payload.copy()
                    for key, value in payload.items():
                        try:
                            if value in id_mapping:
                                payload[key] = id_mapping[value]
                        except TypeError:  # unhashable
                            continue
                    if event_type is requesttools.BufferReadRequest:
                        if 'channel_indices' in payload:
                            if payload['channel_indices'] is not None:
                                event = requesttools.BufferReadChannelRequest(**payload)
                            else:
                                payload.pop('channel_indices')
                                event = requesttools.BufferReadRequest(**payload)
                        else:
                            event = requesttools.BufferReadRequest(**payload)
                    else:
                        event = event_type(**payload)
                    offset_settings = buffer_settings.setdefault(offset, {})
                    event_type_settings = offset_settings.setdefault(event_type, [])
                    event_type_settings.append(event)
        return buffer_settings

    def _collect_bus_settings(self, id_mapping):
        bus_settings = {}
        for bus in self._buses:
            if bus.calculation_rate != synthdeftools.CalculationRate.CONTROL:
                continue
            bus_id = id_mapping[bus]
            for offset, value in bus._events:
                bus_settings.setdefault(offset, {})[bus_id] = value
        return bus_settings

    def _collect_durated_objects(self, offset, is_last_offset):
        state = self._find_state_at(offset, clone_if_missing=True)
        start_buffers, start_nodes = state.start_buffers, state.start_nodes
        stop_buffers = state.stop_buffers.copy()
        stop_nodes = state.stop_nodes.copy()
        if is_last_offset:
            stop_buffers.update(state.overlap_buffers)
            stop_nodes.update(state.overlap_nodes)
        all_buffers = set(self.buffers.find_timespans_overlapping_offset(offset))
        all_nodes = set(self.nodes.find_timespans_overlapping_offset(offset))
        all_buffers.update(stop_buffers)
        all_nodes.update(stop_nodes)
        return (
            all_buffers,
            all_nodes,
            start_buffers,
            start_nodes,
            stop_buffers,
            stop_nodes,
            )

    def _collect_node_action_requests(
        self,
        duration,
        id_mapping,
        node_actions,
        node_settings,
        start_nodes,
        ):
        from supriya.tools import nonrealtimetools
        requests = []
        for source, action in node_actions.items():
            if source in start_nodes:
                if isinstance(source, nonrealtimetools.Synth):
                    synth_kwargs = source.synth_kwargs
                    if source in node_settings:
                        synth_kwargs.update(node_settings.pop(source))
                    if 'duration' in source.synthdef.parameter_names:
                        # need to propagate in session rendering timespan
                        # as many nodes have "infinite" duration
                        node_duration = source.duration
                        if duration < source.stop_offset:  # duration is session duration
                            node_duration = duration - source.start_offset
                        synth_kwargs['duration'] = float(node_duration)
                    request = source.to_request(action, id_mapping, **synth_kwargs)
                else:
                    request = source.to_request(action, id_mapping)
            else:
                request = action.to_request(id_mapping)
            requests.append(request)
        return requests

    def _collect_node_free_requests(self, id_mapping, stop_nodes):
        requests = []
        if stop_nodes:
            free_ids, gate_ids = [], []
            for node in stop_nodes:
                node_id = id_mapping[node]
                if hasattr(node, 'synthdef') and \
                    'gate' in node.synthdef.parameter_names:
                    gate_ids.append(node_id)
                elif node.duration:
                    free_ids.append(node_id)
            free_ids.sort()
            gate_ids.sort()
            if free_ids:
                request = requesttools.NodeFreeRequest(node_ids=free_ids)
                requests.append(request)
            if gate_ids:
                for node_id in gate_ids:
                    request = requesttools.NodeSetRequest(
                        node_id=node_id,
                        gate=0,
                        )
                    requests.append(request)
        return requests

    def _collect_node_settings(self, offset, state, id_mapping):
        result = collections.OrderedDict()
        if state.nodes_to_children is None:
            # Current state is sparse;
            # Use previous non-sparse state's nodes to order settings.
            state = self._find_state_before(
                offset,
                with_node_tree=True,
                )
            iterator = state._iterate_nodes(
                self.root_node,
                state.nodes_to_children,
                )
        else:
            iterator = state._iterate_nodes(
                self.root_node,
                state.nodes_to_children,
                )
        for node in iterator:
            settings = node._collect_settings(
                offset,
                id_mapping=id_mapping,
                persistent=False,
                )
            if settings:
                result[node] = settings
        return result

    def _collect_node_set_requests(self, id_mapping, node_settings):
        from supriya.tools import nonrealtimetools
        requests = []
        bus_prototype = (
            nonrealtimetools.Bus,
            nonrealtimetools.BusGroup,
            type(None),
            )
        buffer_prototype = (
            nonrealtimetools.Buffer,
            nonrealtimetools.BufferGroup,
            )
        for node, settings in node_settings.items():
            node_id = id_mapping[node]
            a_settings = {}
            c_settings = {}
            n_settings = {}
            for key, value in settings.items():
                if isinstance(value, bus_prototype):
                    if value is None:
                        c_settings[key] = -1
                    elif value.calculation_rate == servertools.CalculationRate.CONTROL:
                        c_settings[key] = id_mapping[value]
                    else:
                        a_settings[key] = id_mapping[value]
                else:
                    if isinstance(value, buffer_prototype):
                        value = id_mapping[value]
                    n_settings[key] = value
            if n_settings:
                request = requesttools.NodeSetRequest(
                    node_id=node_id,
                    **n_settings
                    )
                requests.append(request)
            if a_settings:
                request = requesttools.NodeMapToAudioBusRequest(
                    node_id=node_id,
                    **a_settings
                    )
                requests.append(request)
            if c_settings:
                request = requesttools.NodeMapToControlBusRequest(
                    node_id=node_id,
                    **c_settings
                    )
                requests.append(request)
            # separate out floats, control buses and audio buses
        return requests

    def _collect_requests_at_offset(
        self,
        buffer_open_states,
        buffer_settings,
        bus_settings,
        duration,
        id_mapping,
        is_last_offset,
        offset,
        visited_synthdefs,
        ):
        requests = []
        (
            all_buffers, all_nodes,
            start_buffers, start_nodes,
            stop_buffers, stop_nodes
            ) = self._collect_durated_objects(offset, is_last_offset)
        state = self._find_state_at(offset, clone_if_missing=True)
        node_actions = state.transitions
        node_settings = self._collect_node_settings(offset, state, id_mapping)
        requests += self._collect_synthdef_requests(
            start_nodes,
            visited_synthdefs,
            )
        requests += self._collect_buffer_allocate_requests(
            buffer_open_states,
            id_mapping,
            start_buffers,
            )
        requests += self._collect_buffer_nonlifecycle_requests(
            all_buffers,
            buffer_open_states,
            buffer_settings,
            id_mapping,
            offset,
            self._ordered_buffer_post_alloc_request_types,
            )
        requests += self._collect_node_action_requests(
            duration,
            id_mapping,
            node_actions,
            node_settings,
            start_nodes,
            )
        requests += self._collect_bus_set_requests(bus_settings, offset)
        requests += self._collect_node_set_requests(id_mapping, node_settings)
        requests += self._collect_node_free_requests(id_mapping, stop_nodes)
        requests += self._collect_buffer_nonlifecycle_requests(
            all_buffers,
            buffer_open_states,
            buffer_settings,
            id_mapping,
            offset,
            self._ordered_buffer_pre_free_request_types,
            )
        requests += self._collect_buffer_free_requests(
            buffer_open_states,
            id_mapping,
            stop_buffers,
            )
        return requests

    def _collect_synthdef_requests(self, start_nodes, visited_synthdefs):
        from supriya.tools import nonrealtimetools
        requests = []
        synthdefs = set()
        for node in start_nodes:
            if not isinstance(node, nonrealtimetools.Synth):
                continue
            elif node.synthdef in visited_synthdefs:
                continue
            synthdefs.add(node.synthdef)
            visited_synthdefs.add(node.synthdef)
        synthdefs = sorted(synthdefs, key=lambda x: x.anonymous_name)
        if synthdefs:
            request = requesttools.SynthDefReceiveRequest(synthdefs=synthdefs)
            requests.append(request)
        return requests

    def _find_state_after(self, offset, with_node_tree=None):
        index = bisect.bisect(self.offsets, offset)
        if with_node_tree:
            while index < len(self.offsets):
                state = self.states[self.offsets[index]]
                if state.nodes_to_children is not None:
                    return state
                index += 1
            return None
        if index < len(self.offsets):
            old_offset = self.offsets[index]
            if offset < old_offset:
                return self.states[old_offset]
        return None

    def _find_state_at(self, offset, clone_if_missing=False):
        state = self.states.get(offset, None)
        if state is None and clone_if_missing:
            old_state = self._find_state_before(offset, with_node_tree=True)
            state = old_state._clone(offset)
            self.states[offset] = state
            self.offsets.insert(
                self.offsets.index(old_state.offset) + 1,
                offset,
            )
        return state

    def _find_state_before(self, offset, with_node_tree=None):
        index = bisect.bisect_left(self.offsets, offset)
        if index == len(self.offsets):
            index -= 1
        old_offset = self.offsets[index]
        if offset <= old_offset:
            index -= 1
        if index < 0:
            return None
        if with_node_tree:
            while 0 <= index:
                state = self.states[self.offsets[index]]
                if state.nodes_to_children is not None:
                    return state
                index -= 1
            return None
        return self.states[self.offsets[index]]

    def _get_next_session_id(self, kind='node'):
        default = 0
        if kind == 'node':
            default = 1000
        session_id = self._session_ids.setdefault(kind, default)
        self._session_ids[kind] += 1
        return session_id

    def _iterate_state_pairs(
        self,
        offset,
        reverse=False,
        with_node_tree=None,
        ):
        if reverse:
            state_two = self._find_state_at(
                offset,
                clone_if_missing=True,
                )
            state_one = self._find_state_before(
                state_two.offset,
                with_node_tree=with_node_tree,
                )
            while state_one is not None:
                yield state_one, state_two
                state_two = state_one
                state_one = self._find_state_before(
                    state_two.offset,
                    with_node_tree=with_node_tree,
                    )
        else:
            state_one = self._find_state_at(
                offset,
                clone_if_missing=True,
                )
            state_two = self._find_state_after(
                state_one.offset,
                with_node_tree=with_node_tree,
                )
            while state_two is not None:
                yield state_one, state_two
                state_one = state_two
                state_two = self._find_state_after(
                    state_one.offset,
                    with_node_tree=with_node_tree,
                    )

    def _process_duration(self, duration=None):
        if self.duration == float('inf'):
            assert duration is not None and 0 < duration < float('inf')
        offsets = self.offsets[1:]
        states = [self.states[offset] for offset in offsets]
        if duration:
            offsets = [offset for offset in offsets if
                offset <= duration]
            states = [self.states[offset] for offset in offsets]
            if states[-1].offset != duration:
                terminal_state = states[-1]._clone(duration)
                states.append(terminal_state)
        return states

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

    def _setup_initial_states(self):
        from supriya.tools import nonrealtimetools
        offset = float('-inf')
        state = nonrealtimetools.State(self, offset)
        state._nodes_to_children = {self.root_node: ()}
        state._nodes_to_parents = {self.root_node: None}
        self.states[offset] = state
        self.offsets.append(offset)
        offset = 0
        state = state._clone(offset)
        self.states[offset] = state
        self.offsets.append(offset)

    def _add_state_at(self, offset):
        old_state = self._find_state_before(offset)
        state = old_state._clone(offset)
        self.states[offset] = state
        self.offsets.insert(
            self.offsets.index(old_state.offset) + 1,
            offset,
            )
        return state

    def _remove_state_at(self, offset):
        state = self._find_state_at(offset, clone_if_missing=False)
        if state is None:
            return
        assert state.is_sparse
        self.offsets.remove(offset)
        del(self.states[offset])
        return state

    ### PUBLIC METHODS ###

    def at(self, offset, propagate=True):
        from supriya.tools import nonrealtimetools
        assert 0 <= offset
        state = self._find_state_at(offset)
        if state:
            assert state.offset in self.states
        if not state:
            state = self._add_state_at(offset)
        return nonrealtimetools.Moment(self, offset, state, propagate)

    def add_buffer(
        self,
        channel_count=None,
        duration=None,
        frame_count=None,
        starting_frame=None,
        file_path=None,
        ):
        from supriya.tools import nonrealtimetools
        assert self.active_moments
        start_moment = self.active_moments[-1]
        session_id = self._get_next_session_id('buffer')
        buffer_ = nonrealtimetools.Buffer(
            self,
            channel_count=channel_count,
            duration=duration,
            file_path=file_path,
            frame_count=frame_count,
            session_id=session_id,
            start_offset=start_moment.offset,
            starting_frame=starting_frame,
            )
        start_moment.state.start_buffers.add(buffer_)
        with self.at(buffer_.stop_offset) as stop_moment:
            stop_moment.state.stop_buffers.add(buffer_)
        self._buffers.insert(buffer_)
        return buffer_

    def add_buffer_group(
        self,
        buffer_count=1,
        channel_count=None,
        duration=None,
        frame_count=None,
        ):
        from supriya.tools import nonrealtimetools
        assert self.active_moments
        start_moment = self.active_moments[-1]
        buffer_group = nonrealtimetools.BufferGroup(
            self,
            buffer_count=buffer_count,
            channel_count=channel_count,
            duration=duration,
            frame_count=frame_count,
            start_offset=start_moment.offset,
            )
        for buffer_ in buffer_group:
            self._buffers.insert(buffer_)
            start_moment.state.start_buffers.add(buffer_)
        with self.at(buffer_group.stop_offset) as stop_moment:
            for buffer_ in buffer_group:
                stop_moment.state.stop_buffers.add(buffer_)
        return buffer_group

    def add_bus(self, calculation_rate='control'):
        from supriya.tools import nonrealtimetools
        bus = nonrealtimetools.Bus(self, calculation_rate=calculation_rate)
        self._buses[bus] = None  # ordered dictionary
        return bus

    def add_bus_group(self, bus_count=1, calculation_rate='control'):
        from supriya.tools import nonrealtimetools
        bus_group = nonrealtimetools.BusGroup(
            self,
            bus_count=bus_count,
            calculation_rate=calculation_rate,
            )
        for bus in bus_group:
            self._buses[bus] = None  # ordered dictionary
        return bus_group

    def add_group(
        self,
        add_action=None,
        duration=None
        ):
        return self.root_node.add_group(
            add_action=add_action,
            duration=duration,
            )

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

    def cue_soundfile(
        self,
        file_path,
        channel_count=2,
        duration=None,
        frame_count=1024 * 32,
        start_frame=0,
        ):
        buffer_ = self.add_buffer(
            channel_count=channel_count,
            duration=duration,
            frame_count=frame_count,
            )
        buffer_.read(
            file_path,
            leave_open=True,
            start_frame=start_frame,
            )
        return buffer_

    def move_node(
        self,
        node,
        add_action=None,
        ):
        self.root_node.move_node(node, add_action=add_action)

    def rebuild_transitions(self):
        for state_one, state_two in self._iterate_state_pairs(
            float('-inf'), with_node_tree=True):
            transitions = state_two._rebuild_transitions(state_one, state_two)
            state_two._transitions = transitions

    def render(
        self,
        output_filename,
        input_filename=None,
        duration=None,
        sample_rate=44100,
        header_format=soundfiletools.HeaderFormat.AIFF,
        sample_format=soundfiletools.SampleFormat.INT24,
        debug=False,
        **kwargs
        ):
        datagram = self.to_datagram(duration=duration)
        md5 = hashlib.md5()
        md5.update(datagram)
        md5 = md5.hexdigest()
        temp_directory_path = tempfile.mkdtemp()
        file_path = os.path.join(temp_directory_path, '{}.osc'.format(md5))
        with open(file_path, 'wb') as file_pointer:
            file_pointer.write(datagram)
        command = self._build_render_command(
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
            state = self.states[offset]
            states.append(state.report())
        return states

    def to_datagram(self, duration=None):
        osc_bundles = self.to_osc_bundles(duration=duration)
        datagrams = []
        for osc_bundle in osc_bundles:
            datagram = osc_bundle.to_datagram(realtime=False)
            size = len(datagram)
            size = struct.pack('>i', size)
            datagrams.append(size)
            datagrams.append(datagram)
        datagram = b''.join(datagrams)
        return datagram

    def to_lists(self, duration=None):
        osc_bundles = self.to_osc_bundles(duration=duration)
        return [osc_bundle.to_list() for osc_bundle in osc_bundles]

    def to_osc_bundles(self, duration=None):
        id_mapping = self._build_id_mapping()
        if self.duration == float('inf'):
            assert duration is not None and 0 < duration < float('inf')
        duration = duration or self.duration
        offsets = self.offsets[1:]
        if duration not in offsets:
            offsets.append(duration)
            offsets.sort()
        buffer_settings = self._collect_buffer_settings(id_mapping)
        bus_settings = self._collect_bus_settings(id_mapping)
        is_last_offset = False
        osc_bundles = []
        buffer_open_states = {}
        visited_synthdefs = set()
        for offset in offsets:
            osc_messages = []
            if offset == duration:
                is_last_offset = True
            requests = self._collect_requests_at_offset(
                buffer_open_states,
                buffer_settings,
                bus_settings,
                duration,
                id_mapping,
                is_last_offset,
                offset,
                visited_synthdefs,
                )
            osc_messages.extend(_.to_osc_message(True) for _ in requests)
            if is_last_offset:
                osc_messages.append(osctools.OscMessage(0))
            if osc_messages:
                osc_bundle = osctools.OscBundle(
                    timestamp=float(offset),
                    contents=osc_messages,
                    )
                osc_bundles.append(osc_bundle)
            if is_last_offset:
                break
        return osc_bundles

    def to_strings(self, include_controls=False):
        from supriya.tools import responsetools
        result = []
        previous_string = None
        for offset, state in sorted(self.states.items()):
            if offset < 0:
                continue
            self._apply_transitions(state.offset)
            query_tree_group = responsetools.QueryTreeGroup.from_state(
                state, include_controls=include_controls)
            string = str(query_tree_group)
            if string == previous_string:
                continue
            previous_string = string
            result.append('{}:'.format(float(round(offset, 6))))
            result.extend(('    ' + line for line in string.split('\n')))
        return '\n'.join(result)

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
    def buffers(self):
        return self._buffers

    @property
    def buses(self):
        return self._buses

    @property
    def duration(self):
        if 1 < len(self.offsets):
            return self.offsets[-1]
        return 0

    @property
    def input_count(self):
        return self._input_count

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

    @property
    def states(self):
        return self._states
