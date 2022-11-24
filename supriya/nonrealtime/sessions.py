import asyncio
import bisect
import collections
import hashlib
import logging
import pathlib
import platform
import shutil
import struct
from os import PathLike
from queue import PriorityQueue
from types import MappingProxyType
from typing import Dict, List, Optional, Set, Tuple, Type

import uqbar.io
from uqbar.containers import DependencyGraph
from uqbar.objects import new

import supriya.commands
import supriya.intervals
import supriya.osc
import supriya.realtime
import supriya.soundfiles
import supriya.synthdefs
from supriya import CalculationRate, HeaderFormat, ParameterRate, SampleFormat, scsynth
from supriya.commands import (
    BufferCopyRequest,
    BufferFillRequest,
    BufferGenerateRequest,
    BufferNormalizeRequest,
    BufferReadChannelRequest,
    BufferReadRequest,
    BufferSetContiguousRequest,
    BufferSetRequest,
    BufferWriteRequest,
    BufferZeroRequest,
    NothingRequest,
    Request,
    RequestBundle,
)
from supriya.exceptions import NonrealtimeOutputMissing, NonrealtimeRenderError
from supriya.nonrealtime.bases import SessionObject
from supriya.nonrealtime.nodes import Synth
from supriya.osc import OscBundle
from supriya.querytree import QueryTreeGroup
from supriya.synthdefs import SynthDef
from supriya.typing import (
    AddActionLike,
    CalculationRateLike,
    HeaderFormatLike,
    SampleFormatLike,
)
from supriya.utils import iterate_nwise

logger = logging.getLogger(__name__)


class Session:
    """
    A non-realtime session.

    ::

        >>> import supriya.nonrealtime
        >>> session = supriya.nonrealtime.Session()

    ::

        >>> import supriya.synthdefs
        >>> import supriya.ugens
        >>> builder = supriya.synthdefs.SynthDefBuilder(frequency=440)
        >>> with builder:
        ...     out = supriya.ugens.Out.ar(
        ...         source=supriya.ugens.SinOsc.ar(
        ...             frequency=builder["frequency"],
        ...         )
        ...     )
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

        >>> result = session.to_lists(duration=20)
        >>> result == [
        ...     [
        ...         0.0,
        ...         [
        ...             ["/d_recv", bytearray(synthdef.compile(use_anonymous_name=True))],
        ...             ["/s_new", "9c4eb4778dc0faf39459fa8a5cd45c19", 1000, 0, 0],
        ...             ["/s_new", "9c4eb4778dc0faf39459fa8a5cd45c19", 1001, 0, 0],
        ...         ],
        ...     ],
        ...     [5.0, [["/s_new", "9c4eb4778dc0faf39459fa8a5cd45c19", 1002, 0, 0]]],
        ...     [10.0, [["/n_free", 1000]]],
        ...     [15.0, [["/n_free", 1001, 1002]]],
        ...     [20.0, [[0]]],
        ... ]
        True

    """

    ### CLASS VARIABLES ###

    _ordered_buffer_post_alloc_request_types: Tuple[Type[Request], ...] = (
        BufferReadRequest,
        BufferReadChannelRequest,
        BufferZeroRequest,
        BufferFillRequest,
        BufferGenerateRequest,
        BufferSetRequest,
        BufferSetContiguousRequest,
        BufferNormalizeRequest,
        BufferCopyRequest,
    )

    _ordered_buffer_pre_free_request_types: Tuple[Type[Request], ...] = (
        BufferWriteRequest,
        # supriya.commands.BufferCloseRequest,  # should be automatic
    )

    ### INITIALIZER ###

    def __init__(
        self,
        input_bus_channel_count=None,
        output_bus_channel_count=None,
        input_=None,
        name: Optional[str] = None,
        padding: Optional[float] = None,
    ):
        import supriya.nonrealtime

        self._options = scsynth.Options(
            input_bus_channel_count=input_bus_channel_count,
            output_bus_channel_count=output_bus_channel_count,
            realtime=False,
        )

        self._active_moments: List[supriya.nonrealtime.Moment] = []
        self._buffers = supriya.intervals.IntervalTree(accelerated=True)
        self._buffers_by_seesion_id: Dict = {}
        self._buses: Dict = collections.OrderedDict()
        self._buses_by_session_id: Dict = {}
        self._name = name
        self._nodes = supriya.intervals.IntervalTree(accelerated=True)
        self._nodes_by_session_id: Dict = {}
        self._offsets: List[float] = []
        self._root_node = supriya.nonrealtime.RootNode(self)
        self._session_ids: Dict = {}
        self._states: Dict = {}
        self._transcript = None

        if input_ and not self.is_session_like(input_):
            input_ = str(input_)
        self._input = input_
        if padding is not None:
            padding = float(padding)
        self._padding = padding

        self._setup_initial_states()
        self._setup_buses()

    ### SPECIAL METHODS ###

    def __graph__(self):
        """
        Graphs session.

        TODO: Get graphviz to respect node order or reimplement as pure SVG.

        ::

            >>> session = supriya.Session()
            >>> with session.at(0):
            ...     group = session.add_group()
            ...     synth_a = group.add_synth(duration=15)
            ...
            >>> with session.at(5):
            ...     synth_b = group.add_synth(duration=15)
            ...     synth_c = group.add_synth(duration=5)
            ...
            >>> with session.at(7.5):
            ...     synth_d = synth_b.add_synth(duration=5, add_action="ADD_BEFORE")
            ...
            >>> with session.at(11):
            ...     _ = synth_d.move_node(synth_a, add_action="ADD_AFTER")
            ...
            >>> supriya.graph(session)  # doctest: +SKIP

        """
        node_mappings = []
        graph = uqbar.graphs.Graph(
            attributes={
                "bgcolor": "transparent",
                "fontname": "Arial",
                "penwidth": 2,
                "rankdir": "LR",
                "ranksep": 1.5,
            },
            edge_attributes={"penwidth": 2},
            node_attributes={
                "fontname": "Arial",
                "fontsize": 12,
                "penwidth": 2,
                "shape": "Mrecord",
                "style": ["filled", "rounded"],
            },
        )
        for offset, state in sorted(self.states.items()):
            cluster, node_mapping, _ = state._as_graphviz_graph()
            cluster.attributes.update(
                label="[{}]".format(offset), style=["solid", "rounded"]
            )
            graph.append(cluster)
            node_mappings.append(node_mapping)
        for first_mapping, second_mapping in iterate_nwise(node_mappings):
            for nrt_node, graphviz_node_one in first_mapping.items():
                if not isinstance(nrt_node, Synth):
                    continue
                graphviz_node_two = second_mapping.get(nrt_node)
                if graphviz_node_two is None:
                    continue
                graphviz_node_one["session_id"].attach(graphviz_node_two["session_id"])
        return graph

    def __render__(
        self,
        output_file_path: Optional[PathLike] = None,
        render_directory_path: Optional[PathLike] = None,
        **kwargs,
    ) -> pathlib.Path:
        _, file_path = self.render(
            output_file_path=output_file_path,
            render_directory_path=render_directory_path,
            **kwargs,
        )
        return file_path

    def __repr__(self) -> str:
        return "<{}>".format(type(self).__name__)

    def __session__(self) -> "Session":
        return self

    ### PRIVATE METHODS ###

    def _add_state_at(self, offset):
        old_state = self._find_state_before(offset)
        state = old_state._clone(offset)
        self.states[offset] = state
        self.offsets.insert(self.offsets.index(old_state.offset) + 1, offset)
        return state

    def _apply_transitions(self, offsets, chain=True):
        import supriya.nonrealtime

        if supriya.nonrealtime.DoNotPropagate._stack:
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
            previous_state = self._find_state_before(offset, with_node_tree=True)
            assert previous_state is not None
            result = supriya.nonrealtime.State._apply_transitions(
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
                next_state = self._find_state_after(offset, with_node_tree=True)
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
        input_count = self._options.input_bus_channel_count
        output_count = self._options.output_bus_channel_count
        first_private_bus_id = input_count + output_count
        allocators = {
            CalculationRate.AUDIO: supriya.realtime.BlockAllocator(
                heap_minimum=first_private_bus_id
            ),
            CalculationRate.CONTROL: supriya.realtime.BlockAllocator(),
        }
        mapping = {}
        if output_count:
            bus_group = self.audio_output_bus_group
            mapping[bus_group] = 0
            for bus_id, bus in enumerate(bus_group):
                mapping[bus] = bus_id
        if input_count:
            bus_group = self.audio_input_bus_group
            mapping[bus_group] = output_count
            for bus_id, bus in enumerate(bus_group, output_count):
                mapping[bus] = bus_id
        for bus in self._buses:
            if bus in mapping or bus.bus_group in mapping:
                continue
            allocator = allocators[bus.calculation_rate]
            if bus.bus_group is None:
                mapping[bus] = allocator.allocate(1)
            else:
                block_id = allocator.allocate(len(bus.bus_group))
                mapping[bus.bus_group] = block_id
                for bus, bus_id in zip(
                    bus.bus_group, range(block_id, block_id + len(bus.bus_group))
                ):
                    mapping[bus] = bus_id
        return mapping

    def _build_id_mapping_for_nodes(self):
        allocator = supriya.realtime.NodeIdAllocator()
        mapping = {self.root_node: 0}
        for offset in self.offsets[1:]:
            state = self.states[offset]
            nodes = sorted(state.start_nodes, key=lambda x: x.session_id)
            for node in nodes:
                mapping[node] = allocator.allocate_node_id()
                mapping[node] = node.session_id
        return mapping

    @staticmethod
    def _build_rand_seed_synthdef():
        import supriya.ugens
        from supriya import SynthDefBuilder

        with SynthDefBuilder(rand_id=0, rand_seed=0) as builder:
            supriya.ugens.RandID.ir(rand_id=builder["rand_id"])
            supriya.ugens.RandSeed.ir(seed=builder["rand_seed"], trigger=1)
            supriya.ugens.FreeSelf.kr(trigger=1)
        return builder.build()

    def _collect_bus_set_requests(self, bus_settings, offset):
        requests = []
        if offset in bus_settings:
            index_value_pairs = sorted(bus_settings[offset].items())
            request = supriya.commands.ControlBusSetRequest(
                index_value_pairs=index_value_pairs
            )
            requests.append(request)
        return requests

    def _collect_buffer_allocate_requests(
        self, buffer_open_states, id_mapping, start_buffers
    ):
        requests = []
        if not start_buffers:
            return requests
        for buffer_ in sorted(start_buffers, key=lambda x: x.session_id):
            arguments = dict(
                buffer_id=id_mapping[buffer_], frame_count=buffer_.frame_count
            )
            request_class = supriya.commands.BufferAllocateRequest
            if buffer_.file_path is not None:
                request_class = supriya.commands.BufferAllocateReadRequest
                arguments["file_path"] = buffer_.file_path
                arguments["starting_frame"] = buffer_.starting_frame
                channel_indices = buffer_.channel_count
                if isinstance(channel_indices, int):
                    channel_indices = tuple(range(buffer_.channel_count))
                    arguments["channel_indices"] = channel_indices
                    request_class = supriya.commands.BufferAllocateReadChannelRequest
                elif isinstance(buffer_.channel_count, tuple):
                    arguments["channel_indices"] = channel_indices
                    request_class = supriya.commands.BufferAllocateReadChannelRequest
            else:
                arguments["channel_count"] = buffer_.channel_count or 1
                arguments["frame_count"] = arguments["frame_count"] or 1
            try:
                request = request_class(**arguments)
            except TypeError:
                raise
            requests.append(request)
            buffer_open_states[id_mapping[buffer_]] = False
        return requests

    def _collect_buffer_free_requests(
        self, buffer_open_states, id_mapping, stop_buffers
    ):
        requests = []
        if not stop_buffers:
            return requests
        for buffer_ in sorted(stop_buffers, key=lambda x: x.session_id):
            if buffer_open_states[id_mapping[buffer_]]:
                close_request = supriya.commands.BufferCloseRequest(
                    buffer_id=id_mapping[buffer_]
                )
                requests.append(close_request)
            request = supriya.commands.BufferFreeRequest(buffer_id=id_mapping[buffer_])
            requests.append(request)
            del buffer_open_states[id_mapping[buffer_]]
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
                supriya.commands.BufferReadRequest,
                supriya.commands.BufferReadChannelRequest,
                supriya.commands.BufferWriteRequest,
            ):
                for request in buffer_requests:
                    buffer_id = request.buffer_id
                    open_state = buffer_open_states[buffer_id]
                    if open_state:
                        close_request = supriya.commands.BufferCloseRequest(
                            buffer_id=buffer_id
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
                    if event_type is supriya.commands.BufferReadRequest:
                        if "channel_indices" in payload:
                            if payload["channel_indices"] is not None:
                                event = supriya.commands.BufferReadChannelRequest(
                                    **payload
                                )
                            else:
                                payload.pop("channel_indices")
                                event = supriya.commands.BufferReadRequest(**payload)
                        else:
                            event = supriya.commands.BufferReadRequest(**payload)
                    else:
                        event = event_type(**payload)
                    offset_settings = buffer_settings.setdefault(offset, {})
                    event_type_settings = offset_settings.setdefault(event_type, [])
                    event_type_settings.append(event)
        return buffer_settings

    def _collect_bus_settings(self, id_mapping):
        bus_settings = {}
        for bus in self._buses:
            if bus.calculation_rate != CalculationRate.CONTROL:
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
        all_buffers = set(self.buffers.find_intersection(offset))
        all_nodes = set(self.nodes.find_intersection(offset))
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
        self, duration, id_mapping, node_actions, node_settings, start_nodes
    ):
        import supriya.nonrealtime

        requests = []
        for source, action in node_actions.items():
            if source in start_nodes:
                if isinstance(source, supriya.nonrealtime.Synth):
                    synth_kwargs = source.synth_kwargs
                    if source in node_settings:
                        synth_kwargs.update(node_settings.pop(source))
                    if "duration" in source.synthdef.parameter_names:
                        # need to propagate in session rendering timespan
                        # as many nodes have "infinite" duration
                        node_duration = source.duration
                        if (
                            duration < source.stop_offset
                        ):  # duration is session duration
                            node_duration = duration - source.start_offset
                        synth_kwargs["duration"] = float(node_duration)
                    for key, value in synth_kwargs.items():
                        if (
                            value in id_mapping
                            and source.synthdef.parameters[key].parameter_rate
                            == ParameterRate.SCALAR
                        ):
                            synth_kwargs[key] = id_mapping[value]
                    request = source._to_request(action, id_mapping, **synth_kwargs)
                else:
                    request = source._to_request(action, id_mapping)
            else:
                request = action._to_request(id_mapping)
            requests.append(request)
        return requests

    def _collect_node_free_requests(self, id_mapping, stop_nodes):
        requests = []
        if stop_nodes:
            free_ids, gate_ids = [], []
            for node in stop_nodes:
                node_id = id_mapping[node]
                if (
                    hasattr(node, "synthdef")
                    and "gate" in node.synthdef.parameter_names
                ):
                    gate_ids.append(node_id)
                elif node.duration:
                    free_ids.append(node_id)
            free_ids.sort()
            gate_ids.sort()
            if free_ids:
                request = supriya.commands.NodeFreeRequest(node_ids=free_ids)
                requests.append(request)
            if gate_ids:
                for node_id in gate_ids:
                    request = supriya.commands.NodeSetRequest(node_id=node_id, gate=0)
                    requests.append(request)
        return requests

    def _collect_node_settings(self, offset, state, id_mapping):
        result = collections.OrderedDict()
        if state.nodes_to_children is None:
            # Current state is sparse;
            # Use previous non-sparse state's nodes to order settings.
            state = self._find_state_before(offset, with_node_tree=True)
            iterator = state._iterate_nodes(self.root_node, state.nodes_to_children)
        else:
            iterator = state._iterate_nodes(self.root_node, state.nodes_to_children)
        for node in iterator:
            settings = node._collect_settings(
                offset, id_mapping=id_mapping, persistent=False
            )
            if settings:
                result[node] = settings
        return result

    def _collect_node_set_requests(self, id_mapping, node_settings):
        import supriya.nonrealtime

        scalar_rate = supriya.ParameterRate.SCALAR
        requests = []
        bus_prototype = (
            supriya.nonrealtime.Bus,
            supriya.nonrealtime.BusGroup,
            type(None),
        )
        buffer_prototype = (supriya.nonrealtime.Buffer, supriya.nonrealtime.BufferGroup)
        for node, settings in node_settings.items():
            parameters = {}
            if isinstance(node, supriya.nonrealtime.Synth):
                parameters = node.synthdef.parameters
            node_id = id_mapping[node]
            a_settings = {}
            c_settings = {}
            n_settings = {}
            for key, value in settings.items():
                if key in parameters and parameters[key].parameter_rate == scalar_rate:
                    continue
                if isinstance(value, bus_prototype):
                    if value is None:
                        c_settings[key] = -1
                    elif (
                        value.calculation_rate
                        == supriya.realtime.CalculationRate.CONTROL
                    ):
                        c_settings[key] = id_mapping[value]
                    else:
                        a_settings[key] = id_mapping[value]
                else:
                    if isinstance(value, buffer_prototype):
                        value = id_mapping[value]
                    n_settings[key] = value
            if n_settings:
                request = supriya.commands.NodeSetRequest(node_id=node_id, **n_settings)
                requests.append(request)
            if a_settings:
                request = supriya.commands.NodeMapToAudioBusRequest(
                    node_id=node_id, **a_settings
                )
                requests.append(request)
            if c_settings:
                request = supriya.commands.NodeMapToControlBusRequest(
                    node_id=node_id, **c_settings
                )
                requests.append(request)
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
            all_buffers,
            all_nodes,
            start_buffers,
            start_nodes,
            stop_buffers,
            stop_nodes,
        ) = self._collect_durated_objects(offset, is_last_offset)
        state = self._find_state_at(offset, clone_if_missing=True)
        node_actions = state.transitions
        node_settings = self._collect_node_settings(offset, state, id_mapping)
        requests += self._collect_synthdef_requests(start_nodes, visited_synthdefs)
        requests += self._collect_buffer_allocate_requests(
            buffer_open_states, id_mapping, start_buffers
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
            duration, id_mapping, node_actions, node_settings, start_nodes
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
            buffer_open_states, id_mapping, stop_buffers
        )
        return requests

    def _collect_synthdef_requests(self, start_nodes, visited_synthdefs):
        import supriya.nonrealtime

        requests = []
        synthdefs = set()
        for node in start_nodes:
            if not isinstance(node, supriya.nonrealtime.Synth):
                continue
            elif node.synthdef in visited_synthdefs:
                continue
            synthdefs.add(node.synthdef)
            visited_synthdefs.add(node.synthdef)
        synthdefs = sorted(synthdefs, key=lambda x: x.anonymous_name)
        for synthdef in synthdefs:
            request = supriya.commands.SynthDefReceiveRequest(
                synthdefs=synthdef, use_anonymous_names=True
            )
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
            self.offsets.insert(self.offsets.index(old_state.offset) + 1, offset)
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

    def _get_next_session_id(self, kind="node"):
        default = 0
        if kind == "node":
            default = 1000
        session_id = self._session_ids.setdefault(kind, default)
        self._session_ids[kind] += 1
        return session_id

    def _iterate_state_pairs(self, offset, with_node_tree=None):
        state_one = self._find_state_at(offset, clone_if_missing=True)
        state_two = self._find_state_after(
            state_one.offset, with_node_tree=with_node_tree
        )
        while state_two is not None:
            yield state_one, state_two
            state_one = state_two
            state_two = self._find_state_after(
                state_one.offset, with_node_tree=with_node_tree
            )

    def _setup_buses(self):
        import supriya.nonrealtime

        self._buses = collections.OrderedDict()
        self._audio_input_bus_group = None
        if self._options.input_bus_channel_count:
            self._audio_input_bus_group = supriya.nonrealtime.AudioInputBusGroup(self)
        self._audio_output_bus_group = None
        if self._options.output_bus_channel_count:
            self._audio_output_bus_group = supriya.nonrealtime.AudioOutputBusGroup(self)

    def _setup_initial_states(self):
        import supriya.nonrealtime

        offset = float("-inf")
        state = supriya.nonrealtime.State(self, offset)
        state._nodes_to_children = {self.root_node: None}
        state._nodes_to_parents = {self.root_node: None}
        self.states[offset] = state
        self.offsets.append(offset)
        offset = 0.0
        state = state._clone(offset)
        self.states[offset] = state
        self.offsets.append(offset)

    def _remove_state_at(self, offset):
        state = self._find_state_at(offset, clone_if_missing=False)
        if state is None:
            return
        assert state.is_sparse
        self.offsets.remove(offset)
        del self.states[offset]
        return state

    def _to_non_xrefd_osc_bundles(self, duration: Optional[float] = None):
        osc_bundles = []
        request_bundles = self._to_non_xrefd_request_bundles(duration=duration)
        for request_bundle in request_bundles:
            osc_bundles.append(request_bundle.to_osc())
        return osc_bundles

    def _to_non_xrefd_request_bundles(self, duration: Optional[float] = None):
        id_mapping = self._build_id_mapping()
        if self.duration == float("inf"):
            assert duration is not None and 0 < duration < float("inf")
        duration = duration or self.duration
        offsets = self.offsets[1:]
        if duration not in offsets:
            offsets.append(duration)
            offsets.sort()
        buffer_settings = self._collect_buffer_settings(id_mapping)
        bus_settings = self._collect_bus_settings(id_mapping)
        is_last_offset = False
        request_bundles = []
        buffer_open_states: Dict = {}
        visited_synthdefs: Set[SynthDef] = set()
        for offset in offsets:
            requests = []
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
            if is_last_offset:
                requests.append(NothingRequest())
            if requests:
                request_bundle = RequestBundle(
                    contents=requests, timestamp=float(offset)
                )
                request_bundles.append(request_bundle)
            if is_last_offset:
                break
        return request_bundles

    ### PUBLIC METHODS ###

    def at(self, offset, propagate=True) -> "supriya.nonrealtime.Moment":
        import supriya.nonrealtime

        offset = float(offset)
        assert 0 <= offset
        state = self._find_state_at(offset)
        if state:
            assert state.offset in self.states
        if not state:
            state = self._add_state_at(offset)
        return supriya.nonrealtime.Moment(self, offset, state, propagate)

    @SessionObject.require_offset
    def add_buffer(
        self,
        channel_count: Optional[int] = None,
        duration: Optional[float] = None,
        frame_count: Optional[int] = None,
        starting_frame: Optional[int] = None,
        file_path: Optional[PathLike] = None,
        offset: Optional[float] = None,
    ) -> "supriya.nonrealtime.Buffer":
        import supriya.nonrealtime

        start_moment = self.active_moments[-1]
        session_id = self._get_next_session_id("buffer")
        buffer_ = supriya.nonrealtime.Buffer(
            self,
            channel_count=channel_count,
            duration=duration,
            file_path=file_path,
            frame_count=frame_count,
            session_id=session_id,
            start_offset=offset,
            starting_frame=starting_frame,
        )
        start_moment.state.start_buffers.add(buffer_)
        with self.at(buffer_.stop_offset) as stop_moment:
            stop_moment.state.stop_buffers.add(buffer_)
        self._buffers.add(buffer_)
        return buffer_

    @SessionObject.require_offset
    def add_buffer_group(
        self,
        buffer_count: int = 1,
        channel_count: Optional[int] = None,
        duration: Optional[float] = None,
        frame_count: Optional[int] = None,
        offset: Optional[float] = None,
    ) -> "supriya.nonrealtime.BufferGroup":
        import supriya.nonrealtime

        start_moment = self.active_moments[-1]
        buffer_group = supriya.nonrealtime.BufferGroup(
            self,
            buffer_count=buffer_count,
            channel_count=channel_count,
            duration=duration,
            frame_count=frame_count,
            start_offset=offset,
        )
        for buffer_ in buffer_group:
            self._buffers.add(buffer_)
            start_moment.state.start_buffers.add(buffer_)
        with self.at(buffer_group.stop_offset) as stop_moment:
            for buffer_ in buffer_group:
                stop_moment.state.stop_buffers.add(buffer_)
        return buffer_group

    def add_bus(
        self, calculation_rate: CalculationRateLike = CalculationRate.CONTROL
    ) -> "supriya.nonrealtime.buses.Bus":
        import supriya.nonrealtime

        session_id = self._get_next_session_id("bus")
        bus = supriya.nonrealtime.Bus(
            self, calculation_rate=calculation_rate, session_id=session_id
        )
        self._buses[bus] = None  # ordered dictionary
        self._buses_by_session_id[session_id] = bus
        return bus

    def add_bus_group(
        self,
        bus_count: int = 1,
        calculation_rate: CalculationRateLike = CalculationRate.CONTROL,
    ) -> "supriya.nonrealtime.buses.BusGroup":
        import supriya.nonrealtime

        session_id = self._get_next_session_id("bus")
        bus_group = supriya.nonrealtime.BusGroup(
            self,
            bus_count=bus_count,
            calculation_rate=calculation_rate,
            session_id=session_id,
        )
        for bus in bus_group:
            self._buses[bus] = None  # ordered dictionary
            self._buses_by_session_id[bus.session_id] = bus
        self._buses_by_session_id[session_id] = bus_group
        return bus_group

    def add_group(
        self,
        add_action: Optional[AddActionLike] = None,
        duration: Optional[float] = None,
        offset=None,
    ) -> "supriya.nonrealtime.nodes.Group":
        return self.root_node.add_group(
            add_action=add_action, duration=duration, offset=offset
        )

    def add_synth(
        self,
        add_action: Optional[AddActionLike] = None,
        duration: Optional[float] = None,
        synthdef: Optional[SynthDef] = None,
        offset: Optional[float] = None,
        **synth_kwargs,
    ) -> "supriya.nonrealtime.nodes.Synth":
        return self.root_node.add_synth(
            add_action=add_action,
            duration=duration,
            offset=offset,
            synthdef=synthdef,
            **synth_kwargs,
        )

    @SessionObject.require_offset
    def cue_soundfile(
        self,
        file_path: PathLike,
        channel_count: Optional[int] = None,
        duration: Optional[float] = None,
        frame_count: int = 1024 * 32,
        starting_frame: int = 0,
        offset: Optional[float] = None,
    ) -> "supriya.nonrealtime.buffers.Buffer":
        if isinstance(file_path, str):
            file_path = pathlib.Path(file_path)
        if isinstance(file_path, pathlib.Path):
            assert file_path.exists()
            soundfile = supriya.soundfiles.SoundFile(str(file_path))
            channel_count = channel_count or soundfile.channel_count
        elif isinstance(file_path, type(self)):
            channel_count = channel_count or len(file_path.audio_output_bus_group)
        elif hasattr(file_path, "__session__"):
            channel_count = channel_count or getattr(
                file_path, "output_bus_channel_count"
            )
        buffer_ = self.add_buffer(
            channel_count=channel_count,
            duration=duration,
            frame_count=frame_count,
            offset=offset,
        )
        buffer_.read(
            file_path,
            leave_open=True,
            starting_frame_in_file=starting_frame,
            offset=offset,
        )
        return buffer_

    @staticmethod
    def is_session_like(expr) -> bool:
        if hasattr(expr, "__render__"):
            return True
        elif hasattr(expr, "__session__"):
            return True
        return False

    def move_node(
        self,
        node: "supriya.nonrealtime.nodes.Node",
        add_action: Optional[AddActionLike] = None,
        offset: Optional[float] = None,
    ) -> None:
        self.root_node.move_node(node, add_action=add_action, offset=offset)

    def rebuild_transitions(self) -> None:
        for state_one, state_two in self._iterate_state_pairs(
            float("-inf"), with_node_tree=True
        ):
            transitions = state_two._rebuild_transitions(state_one, state_two)
            state_two._transitions = transitions

    def render(
        self,
        output_file_path: Optional[PathLike] = None,
        duration: Optional[float] = None,
        header_format=HeaderFormat.AIFF,
        input_file_path=None,
        render_directory_path=None,
        sample_format=SampleFormat.INT24,
        sample_rate=44100,
        **kwargs,
    ) -> Tuple[int, pathlib.Path]:
        return asyncio.run(
            self.render_async(
                output_file_path=output_file_path,
                duration=duration,
                header_format=header_format,
                input_file_path=input_file_path,
                render_directory_path=render_directory_path,
                sample_format=sample_format,
                sample_rate=sample_rate,
                **kwargs,
            )
        )

    async def render_async(
        self,
        output_file_path: Optional[PathLike] = None,
        duration: Optional[float] = None,
        header_format=HeaderFormat.AIFF,
        input_file_path=None,
        render_directory_path=None,
        sample_format=SampleFormat.INT24,
        sample_rate=44100,
        **kwargs,
    ) -> Tuple[int, pathlib.Path]:
        duration = (duration or self.duration) or 0.0
        if not (0.0 < duration < float("inf")):
            raise ValueError(f"Invalid duration: {duration}")
        renderer = Renderer(
            session=self,
            header_format=header_format,
            render_directory_path=render_directory_path,
            sample_format=sample_format,
            sample_rate=sample_rate,
        )
        exit_code, file_path = await renderer.render(
            output_file_path, duration=duration, **kwargs
        )
        return exit_code, file_path

    @SessionObject.require_offset
    def set_rand_seed(
        self, rand_id: int = 0, rand_seed: int = 0, offset: Optional[float] = None
    ) -> "supriya.nonrealtime.Synth":
        return self.add_synth(
            add_action="ADD_TO_HEAD",
            duration=0,
            rand_id=rand_id,
            rand_seed=rand_seed,
            synthdef=self._build_rand_seed_synthdef(),
        )

    def to_lists(
        self,
        duration: Optional[float] = None,
        header_format=HeaderFormat.AIFF,
        sample_format=SampleFormat.INT24,
        sample_rate: int = 44100,
    ) -> List:
        renderer = Renderer(
            session=self,
            header_format=header_format,
            sample_format=sample_format,
            sample_rate=sample_rate,
        )
        return renderer.to_lists(duration=duration)

    def to_osc_bundles(
        self,
        duration: Optional[float] = None,
        header_format=HeaderFormat.AIFF,
        sample_format=SampleFormat.INT24,
        sample_rate: int = 44100,
    ) -> List[OscBundle]:
        renderer = Renderer(
            session=self,
            header_format=header_format,
            sample_format=sample_format,
            sample_rate=sample_rate,
        )
        return renderer.to_osc_bundles(duration=duration)

    def to_strings(self, include_controls=False, include_timespans=False) -> str:
        result = []
        previous_string = None
        for offset, state in sorted(self.states.items()):
            if offset < 0:
                continue
            self._apply_transitions(state.offset)
            query_tree_group = QueryTreeGroup.from_state(
                state,
                include_controls=include_controls,
                include_timespans=include_timespans,
            )
            string = str(query_tree_group)
            if string == previous_string:
                continue
            previous_string = string
            result.append("{}:".format(float(round(offset, 6))))
            result.extend(("    " + line for line in string.split("\n")))
        return "\n".join(result)

    ### PUBLIC PROPERTIES ###

    @property
    def active_moments(self) -> List["supriya.nonrealtime.Moment"]:
        return self._active_moments

    @property
    def audio_input_bus_group(self) -> "supriya.nonrealtime.AudioInputBusGroup":
        return self._audio_input_bus_group

    @property
    def audio_output_bus_group(self) -> "supriya.nonrealtime.AudioOutputBusGroup":
        return self._audio_output_bus_group

    @property
    def buffers(self):
        return self._buffers

    @property
    def buffers_by_session_id(self):
        return MappingProxyType(self._buffers_by_session_id)

    @property
    def buses(self):
        return self._buses

    @property
    def buses_by_session_id(self):
        return MappingProxyType(self._buses_by_session_id)

    @property
    def duration(self) -> float:
        duration = 0.0
        for duration in reversed(self.offsets):
            if duration < float("inf"):
                break
        if duration < 0.0:
            duration = 0.0
        if duration > 0.0 and self.padding:
            duration += self.padding
        return duration

    @property
    def input_(self):
        return self._input

    @property
    def input_bus_channel_count(self) -> int:
        return self.options.input_bus_channel_count

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def nodes(self):
        return self._nodes

    @property
    def nodes_by_session_id(self):
        return MappingProxyType(self._nodes_by_session_id)

    @property
    def offsets(self) -> List[float]:
        return self._offsets

    @property
    def options(self) -> scsynth.Options:
        return self._options

    @property
    def output_bus_channel_count(self) -> int:
        return self.options.output_bus_channel_count

    @property
    def padding(self) -> Optional[float]:
        return self._padding

    @property
    def root_node(self) -> "supriya.nonrealtime.RootNode":
        return self._root_node

    @property
    def states(self):
        return self._states

    @property
    def transcript(self):
        return self._transcript


class Renderer:
    """
    Renders non-realtime sessions as audio files.
    """

    ### INITIALIZER ###

    def __init__(
        self,
        session: "supriya.nonrealtime.sessions.Session",
        header_format: HeaderFormatLike = HeaderFormat.AIFF,
        render_directory_path: Optional[PathLike] = None,
        sample_format: SampleFormatLike = SampleFormat.INT24,
        sample_rate: int = 44100,
    ):
        self._compiled_sessions = {}
        self._dependency_graph = DependencyGraph()
        self._header_format = HeaderFormat.from_expr(header_format)
        self._prerender_tuples = []
        self._render_directory_path = pathlib.Path(
            render_directory_path or supriya.output_path
        ).resolve()
        self._renderable_prefixes = {}
        self._sample_format = SampleFormat.from_expr(sample_format)
        self._sample_rate = int(sample_rate)
        self._session = session
        self._session_input_paths = {}
        self._sessionables_to_sessions = {}

    ### PRIVATE METHODS ###

    def _build_datagram(self, osc_bundles):
        datagrams = []
        for osc_bundle in osc_bundles:
            datagram = osc_bundle.to_datagram(realtime=False)
            size = len(datagram)
            size = struct.pack(">i", size)
            datagrams.append(size)
            datagrams.append(datagram)
        datagram = b"".join(datagrams)
        return datagram

    def _build_file_path(self, datagram, input_file_path, session):
        # print('BUILDING FILE PATH')
        md5 = hashlib.md5()
        md5.update(datagram)
        hash_values = []
        if input_file_path is not None:
            hash_values.append(input_file_path)
        for value in (
            session.options.input_bus_channel_count,
            session.options.output_bus_channel_count,
            self.sample_rate,
            self.header_format,
            self.sample_format,
        ):
            hash_values.append(value)
        for value in hash_values:
            if not isinstance(value, str):
                value = str(value)
            value = value.encode()
            md5.update(value)
        md5 = md5.hexdigest()
        file_path = "session-{}.osc".format(md5)
        return pathlib.Path(file_path)

    def _build_render_command(
        self,
        input_file_path,
        output_file_path,
        session_osc_file_path,
        *,
        server_options: Optional[scsynth.Options] = None,
    ):
        options = new(server_options or scsynth.Options(), realtime=False)
        command = list(options)
        command.extend(["-N", session_osc_file_path])
        command.append(input_file_path or "_")
        command.extend(
            [
                output_file_path,
                self.sample_rate,
                self.header_format.name.lower(),  # Must be lowercase.
                self.sample_format.name.lower(),  # Must be lowercase.
            ]
        )
        return [str(_) for _ in command]

    def _build_xrefd_bundles(self, osc_bundles):
        extension = ".{}".format(self.header_format.name.lower())
        for osc_bundle in osc_bundles:
            for osc_message in osc_bundle.contents:
                contents = list(osc_message.contents)
                for i, x in enumerate(contents):
                    x = self._sessionable_to_session(x)
                    try:
                        if x not in self.renderable_prefixes:
                            continue
                    except TypeError:
                        continue
                    renderable_file_path = self.renderable_prefixes[x].with_suffix(
                        extension
                    )
                    contents[i] = str(renderable_file_path)
                osc_message.contents = tuple(contents)
        return osc_bundles

    def _build_dependency_graph_and_nonxrefd_osc_bundles_conditionally(
        self, expr, parent
    ):
        import supriya.nonrealtime

        expr = self._sessionable_to_session(expr)
        if isinstance(expr, supriya.nonrealtime.Session):
            if expr not in self.dependency_graph:
                self._build_dependency_graph_and_nonxrefd_osc_bundles(expr)
            self.dependency_graph.add(expr, parent=parent)
        elif hasattr(expr, "__render__"):
            self.dependency_graph.add(expr, parent=parent)

    def _build_dependency_graph_and_nonxrefd_osc_bundles(self, session, duration=None):
        input_ = session.input_
        if isinstance(input_, str):
            input_ = pathlib.Path(input_)
        input_ = self._sessionable_to_session(input_)
        non_xrefd_bundles = session._to_non_xrefd_osc_bundles(duration)
        self.compiled_sessions[session] = input_, non_xrefd_bundles
        if session is self.session:
            self.dependency_graph.add(session)
        self._build_dependency_graph_and_nonxrefd_osc_bundles_conditionally(
            input_, session
        )
        for non_xrefd_bundle in non_xrefd_bundles:
            for request in non_xrefd_bundle.contents:
                for x in request.contents:
                    self._build_dependency_graph_and_nonxrefd_osc_bundles_conditionally(
                        x, session
                    )

    def _collect_prerender_tuples(self, session, duration=None):
        import supriya.nonrealtime

        self._build_dependency_graph_and_nonxrefd_osc_bundles(
            session, duration=duration
        )
        assert self.dependency_graph.is_acyclic()
        extension = ".{}".format(self.header_format.name.lower())
        for renderable in self.dependency_graph:
            if isinstance(renderable, supriya.nonrealtime.Session):
                result = self._collect_session_prerender_tuple(renderable, extension)
                prerender_tuple, renderable_prefix = result
            else:
                result = self._collect_renderable_prerender_tuple(renderable)
                prerender_tuple, renderable_prefix = result
            self.prerender_tuples.append(prerender_tuple)
            self.renderable_prefixes[renderable] = renderable_prefix
        return self.prerender_tuples

    def _collect_renderable_prerender_tuple(self, renderable):
        renderable_prefix = renderable._build_file_path().with_suffix("")
        return (renderable,), renderable_prefix

    def _collect_session_prerender_tuple(self, session, extension):
        input_, non_xrefd_bundles = self.compiled_sessions[session]
        osc_bundles = self._build_xrefd_bundles(non_xrefd_bundles)
        input_file_path = input_
        if input_ and input_ in self.renderable_prefixes:
            input_file_path = self.renderable_prefixes[input_]
            input_file_path = input_file_path.with_suffix(extension)
        if input_file_path:
            input_file_path = self.get_path_relative_to_render_path(
                input_file_path, self.render_directory_path
            )
            self.session_input_paths[session] = input_file_path
        datagram = self._build_datagram(osc_bundles)
        renderable_prefix = self._build_file_path(
            datagram, input_file_path, session
        ).with_suffix("")
        return (session, datagram, input_, osc_bundles), renderable_prefix

    async def _render_datagram(
        self,
        session,
        input_file_path,
        output_file_path,
        session_osc_file_path,
        scsynth_path=None,
        **kwargs,
    ):
        relative_session_osc_file_path = session_osc_file_path
        logger.info(f"Rendering {relative_session_osc_file_path}.")
        if output_file_path.exists():
            logger.info(
                f"    Skipped {relative_session_osc_file_path}. Output already exists."
            )
            return 0
        server_options = session._options
        server_options = new(server_options, **kwargs)
        memory_size = server_options.memory_size
        for factor in range(1, 6):
            command = self._build_render_command(
                input_file_path,
                output_file_path.name,
                session_osc_file_path,
                server_options=server_options,
            )
            logger.info(f"    Command: {' '.join(command)}")
            exit_future = asyncio.get_running_loop().create_future()
            protocol = AsyncProcessProtocol(exit_future)
            await protocol.run(command, self.render_directory_path)
            await exit_future
            exit_code = exit_future.result()
            if exit_code == -6:
                logger.info(
                    f"    Out of memory. Increasing to {server_options.memory_size}."
                )
            else:
                logger.info(
                    f"    Rendered {relative_session_osc_file_path} with exit code {exit_code}."
                )
                break
            server_options = new(
                server_options, memory_size=memory_size * (2**factor)
            )
        return exit_code

    def _read_datagram(self, file_path):
        try:
            with open(str(file_path), "rb") as file_pointer:
                return file_pointer.read()
        except FileNotFoundError:
            return None

    def _sessionable_to_session(self, expr):
        if hasattr(expr, "__session__"):
            if expr not in self._sessionables_to_sessions:
                self._sessionables_to_sessions[expr] = expr.__session__()
            return self._sessionables_to_sessions[expr]
        return expr

    def _write_datagram(self, file_path, new_contents):
        logger.info(f"Writing {file_path.name}.")
        old_contents = None
        if file_path.exists():
            old_contents = file_path.read_bytes()
        if old_contents == new_contents:
            logger.info(f"    Skipped {file_path.name}. File already exists.")
        else:
            file_path.write_bytes(new_contents)
            logger.info(f"    Wrote {file_path.name}.")

    ### PUBLIC METHODS ###

    def to_lists(self, duration=None):
        osc_bundles = self.to_osc_bundles(duration=duration)
        return [osc_bundle.to_list() for osc_bundle in osc_bundles]

    def to_osc_bundles(self, duration=None):
        self._collect_prerender_tuples(self.session, duration=duration)
        (session, datagram, input_file_path, osc_bundles) = self.prerender_tuples[-1]
        return osc_bundles

    @classmethod
    def get_path_relative_to_render_path(cls, target_path, render_path):
        target_path = pathlib.Path(target_path)
        render_path = pathlib.Path(render_path)
        try:
            return target_path.relative_to(render_path)
        except ValueError:
            pass
        target_path = pathlib.Path(target_path)
        render_path = pathlib.Path(render_path)
        target_path_parents = set(target_path.parents)
        render_path_parents = set(render_path.parents)
        common_parents = target_path_parents.intersection(render_path_parents)
        if not common_parents:
            return target_path
        common_parent = sorted(common_parents)[-1]
        target_path = target_path.relative_to(common_parent)
        render_path = render_path.relative_to(common_parent)
        parts = [".." for _ in render_path.parts] + [target_path]
        return pathlib.Path().joinpath(*parts)

    async def render(
        self,
        output_file_path: Optional[PathLike] = None,
        duration: Optional[float] = None,
        scsynth_path: Optional[str] = None,
        **kwargs,
    ) -> Tuple[int, pathlib.Path]:
        import supriya.nonrealtime

        if output_file_path is not None:
            output_file_path = pathlib.Path(output_file_path).resolve()
        self._collect_prerender_tuples(self.session, duration=duration)
        assert self.prerender_tuples, self.prerender_tuples
        extension = f".{self.header_format.name.lower()}"
        visited_renderable_prefixes = []
        for prerender_tuple in self.prerender_tuples:
            renderable = prerender_tuple[0]
            renderable_prefix = self.renderable_prefixes[renderable]
            visited_renderable_prefixes.append(renderable_prefix.with_suffix("").name)
            relative_output_file_path = renderable_prefix.with_suffix(extension)
            if not isinstance(renderable, supriya.nonrealtime.Session):
                result = renderable.__render__(
                    output_file_path=self.render_directory_path
                    / relative_output_file_path
                )
                if asyncio.iscoroutine(result):
                    await result
                continue
            (session, datagram, input_, _) = prerender_tuple
            osc_file_path = renderable_prefix.with_suffix(".osc")
            input_file_path = self.session_input_paths.get(session)
            self._write_datagram(self.render_directory_path / osc_file_path, datagram)
            exit_code = await self._render_datagram(
                session,
                input_file_path,
                self.render_directory_path / relative_output_file_path,
                osc_file_path,
                scsynth_path=scsynth_path,
                **kwargs,
            )
            if exit_code:
                if (
                    platform.system() == "Windows"
                    and (
                        self.render_directory_path / relative_output_file_path
                    ).exists()
                ):
                    # scsynth.exe renders but exits non-zero
                    # https://github.com/supercollider/supercollider/issues/5769
                    # logger.info(
                    #     "    SuperCollider exited with non-zero but output exists!"
                    # )
                    pass
                else:
                    logger.info("    SuperCollider errored!")
                    raise NonrealtimeRenderError(exit_code)
        final_rendered_file_path = (
            self.render_directory_path / relative_output_file_path
        )
        if not final_rendered_file_path.exists():
            logger.info("    Output file is missing!")
            raise NonrealtimeOutputMissing(final_rendered_file_path)
        # TODO: Make this cross-platform
        if output_file_path is not None:
            shutil.copy(final_rendered_file_path, output_file_path)
        return (exit_code, output_file_path or final_rendered_file_path)

    ### PUBLIC PROPERTIES ###

    @property
    def compiled_sessions(self):
        return self._compiled_sessions

    @property
    def dependency_graph(self):
        return self._dependency_graph

    @property
    def header_format(self) -> HeaderFormat:
        return self._header_format

    @property
    def prerender_tuples(self):
        return self._prerender_tuples

    @property
    def render_directory_path(self) -> pathlib.Path:
        return self._render_directory_path

    @property
    def renderable_prefixes(self):
        return self._renderable_prefixes

    @property
    def sample_format(self) -> SampleFormat:
        return self._sample_format

    @property
    def sample_rate(self) -> int:
        return self._sample_rate

    @property
    def session(self) -> "supriya.nonrealtime.sessions.Session":
        return self._session

    @property
    def session_input_paths(self):
        return self._session_input_paths


class AsyncProcessProtocol(asyncio.SubprocessProtocol):
    def __init__(self, exit_future: asyncio.Future):
        self.buffer_ = ""
        self.exit_future = exit_future

    async def run(self, command: List[str], render_directory_path: pathlib.Path):
        _, _ = await asyncio.get_running_loop().subprocess_exec(
            lambda: self,
            *command,
            stdin=None,
            stderr=None,
            start_new_session=True,
            cwd=render_directory_path,
        )

    def handle_line(self, line):
        logger.debug(f"Received: {line}")

    def connection_made(self, transport):
        self.transport = transport

    def pipe_data_received(self, fd, data):
        # *nix and OSX return full lines,
        # but Windows will return partial lines
        # which obligates us to reconstruct them.
        text = self.buffer_ + data.decode().replace("\r\n", "\n")
        if "\n" in text:
            text, _, self.buffer_ = text.rpartition("\n")
            for line in text.splitlines():
                self.handle_line(line)
        else:
            self.buffer_ = text

    def process_exited(self):
        self.exit_future.set_result(self.transport.get_returncode())
