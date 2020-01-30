import atexit
import logging
import re
import threading
import time
from typing import Set

from uqbar.objects import new

import supriya.exceptions
from supriya.commands import (  # type: ignore
    FailResponse,
    GroupQueryTreeRequest,
    NotifyRequest,
    QuitRequest,
    SyncRequest,
)
from supriya.enums import NodeAction
from supriya.querytree import QueryTreeGroup, QueryTreeSynth

from .allocators import BlockAllocator, NodeIdAllocator
from .process import BootOptions
from .meters import Meters
from .recorder import Recorder

# TODO: Implement connect() and disconnect()
# TODO: Handle clientID return via [/done /notify 0 64] for allocators


logger = logging.getLogger("supriya.server")


class Server:
    """
    An scsynth server proxy.

    ::

        >>> import supriya.realtime
        >>> server = supriya.realtime.Server.default()
        >>> server.boot()
        <Server: udp://127.0.0.1:57751, 8i8o>

    ::

        >>> server.quit()
        <Server: offline>

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Main Classes"

    _default_server = None

    _servers: Set["Server"] = set()

    ### CONSTRUCTOR ###

    """
    def __new__(cls, ip_address="127.0.0.1", port=57751, **kwargs):
        key = (ip_address, port)
        if key not in cls._servers:
            instance = object.__new__(cls)
            instance.__init__(ip_address=ip_address, port=port, **kwargs)
            cls._servers[key] = instance
        return cls._servers[key]
    """

    ### INITIALIZER ###

    def __init__(self, ip_address=None, port=None):
        import supriya.osc

        type(self)._servers.add(self)

        ### NET ADDRESS ###

        self._ip_address = ip_address or "127.0.0.1"
        self._port = port or 57751

        ### OSC MESSAGING ###

        self._latency = 0.1
        self._lock = threading.Lock()
        self._osc_protocol = supriya.osc.ThreadedOscProtocol()

        ### ALLOCATORS ###

        self._audio_bus_allocator = None
        self._buffer_allocator = None
        self._control_bus_allocator = None
        self._node_id_allocator = None
        self._sync_id = 0

        ### SERVER PROCESS ###

        self._client_id = None
        self._maximum_logins = None
        self._is_owner = False
        self._is_running = False
        self._options = BootOptions()
        self._server_process = None
        self._status = None
        self._status_watcher = None

        ### PROXIES ###

        self._audio_input_bus_group = None
        self._audio_output_bus_group = None
        self._default_group = None
        self._root_node = None
        self._meters = Meters(self)
        self._recorder = Recorder(self)

        ### PROXY MAPPINGS ###

        self._audio_buses = {}
        self._buffer_proxies = {}
        self._buffers = {}
        self._control_bus_proxies = {}
        self._control_buses = {}
        self._nodes = {}
        self._pending_synths = {}
        self._synthdefs = {}

        ### DEBUG ###

        self.debug_request_names = False

        ### REGISTER WITH ATEXIT ###

        atexit.register(self._shutdown)

    ### SPECIAL METHODS ###

    def __contains__(self, expr):
        import supriya.realtime
        import supriya.synthdefs

        if isinstance(expr, supriya.realtime.Node):
            if expr.server is not self:
                return False
            node_id = expr.node_id
            if node_id in self._nodes and self._nodes[node_id] is expr:
                return True
        elif isinstance(expr, supriya.synthdefs.SynthDef):
            name = expr.actual_name
            if name in self._synthdefs and self._synthdefs[name] == expr:
                return True
        elif isinstance(expr, supriya.realtime.ServerObject):
            return expr.server is self
        return False

    def __enter__(self):
        self.boot()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.sync()
        self.quit()

    def __getitem__(self, item):
        """
        Get ``item`` from server.

        ::

            >>> server = supriya.Server.default().boot()
            >>> supriya.Synth(name='foo').allocate()
            <+ Synth: 1000 (foo)>

        ::

            >>> server[1000]
            <+ Synth: 1000 (foo)>

        ::

            >>> server['foo']
            <+ Synth: 1000 (foo)>

        ::

            >>> server['b10']
            <+ Buffer: 10>

        ::

            >>> server['a0']
            <+ Bus: 0 (audio)>

        ::

            >>> server['c16']
            <+ Bus: 16 (control)>

        ::

            >>> server = server.quit()
            >>> server['c16']
            Traceback (most recent call last):
            ...
            supriya.exceptions.ServerOffline

        """
        import supriya

        if not self.is_running:
            raise supriya.exceptions.ServerOffline
        if isinstance(item, str):
            match = re.match(r"b(?P<id>\d+)", item)
            if match:
                id_ = int(match.groupdict()["id"])
                return supriya.realtime.Buffer(id_).allocate(server=self)
            match = re.match(r"c(?P<id>\d+)", item)
            if match:
                id_ = int(match.groupdict()["id"])
                return supriya.realtime.Bus(id_, "control").allocate(server=self)
            match = re.match(r"a(?P<id>\d+)", item)
            if match:
                id_ = int(match.groupdict()["id"])
                return supriya.realtime.Bus(id_, "audio").allocate(server=self)
            result = self.root_node[item]
        elif isinstance(item, int):
            result = self._nodes.get(item)
        else:
            raise ValueError(item)
        if isinstance(result, set) and len(result) == 1:
            return tuple(result)[0]
        return result

    def __graph__(self):
        """
        Graph server.

        ::

            >>> import supriya
            >>> server = supriya.Server.default().boot()
            >>> group = supriya.Group([
            ...     supriya.Synth(),
            ...     supriya.Group([
            ...         supriya.Synth(),
            ...         supriya.Synth(),
            ...         ]),
            ...     ]).allocate()

        ::

            >>> graph = server.__graph__()
            >>> print(format(graph, 'graphviz'))
            digraph G {
                graph [bgcolor=transparent,
                    color=lightslategrey,
                    dpi=72,
                    fontname=Arial,
                    outputorder=edgesfirst,
                    overlap=prism,
                    penwidth=2,
                    rankdir=TB,
                    ranksep=0.5,
                    splines=spline,
                    style="dotted, rounded"];
                node [fontname=Arial,
                    fontsize=12,
                    penwidth=2,
                    shape=Mrecord,
                    style="filled, rounded"];
                edge [penwidth=2];
                "root-node-0" [fillcolor=lightsalmon2,
                    label="{ <f_0_0> RootNode | <f_0_1> id: 0 }"];
                "group-1" [fillcolor=lightsteelblue2,
                    label="{ <f_0_0> Group | <f_0_1> id: 1 }"];
                "group-1000" [fillcolor=lightsteelblue2,
                    label="{ <f_0_0> Group | <f_0_1> id: 1000 }"];
                "synth-1001" [fillcolor=lightgoldenrod2,
                    label="{ <f_0_0> Synth | <f_0_1> id: 1001 }"];
                "group-1002" [fillcolor=lightsteelblue2,
                    label="{ <f_0_0> Group | <f_0_1> id: 1002 }"];
                "synth-1003" [fillcolor=lightgoldenrod2,
                    label="{ <f_0_0> Synth | <f_0_1> id: 1003 }"];
                "synth-1004" [fillcolor=lightgoldenrod2,
                    label="{ <f_0_0> Synth | <f_0_1> id: 1004 }"];
                "root-node-0" -> "group-1";
                "group-1" -> "group-1000";
                "group-1000" -> "synth-1001";
                "group-1000" -> "group-1002";
                "group-1002" -> "synth-1003";
                "group-1002" -> "synth-1004";
            }

        ::

            >>> supriya.graph(server)  # doctest: +SKIP

        """

        return self.root_node.__graph__()

    def __repr__(self):
        if not self.is_running:
            return "<Server: offline>"
        string = "<Server: {protocol}://{ip}:{port}, "
        string += "{inputs}i{outputs}o>"
        return string.format(
            protocol=self.options.protocol,
            ip=self.ip_address,
            port=self.port,
            inputs=self.options.input_bus_channel_count,
            outputs=self.options.output_bus_channel_count,
        )

    def __str__(self):
        if self.is_running:
            return str(self.query_remote_nodes(True))
        return ""

    ### PRIVATE METHODS ###

    def _as_node_target(self):
        return self.default_group

    def _get_buffer_proxy(self, buffer_id):
        import supriya.realtime

        buffer_proxy = self._buffer_proxies.get(buffer_id)
        if not buffer_proxy:
            buffer_proxy = supriya.realtime.BufferProxy(
                buffer_id=buffer_id, server=self
            )
            self._buffer_proxies[buffer_id] = buffer_proxy
        return buffer_proxy

    def _get_control_bus_proxy(self, bus_id):
        import supriya.realtime
        import supriya.synthdefs

        control_bus_proxy = self._control_bus_proxies.get(bus_id)
        if not control_bus_proxy:
            control_bus_proxy = supriya.realtime.BusProxy(
                bus_id=bus_id,
                calculation_rate=supriya.CalculationRate.CONTROL,
                server=self,
            )
            self._control_bus_proxies[bus_id] = control_bus_proxy
        return control_bus_proxy

    def _handle_buffer_info_response(self, message):
        from supriya.commands import Response

        response = Response.from_osc_message(message)
        for item in response.items:
            buffer_proxy = self._get_buffer_proxy(item.buffer_id)
            if buffer_proxy:
                buffer_proxy._handle_response(item)

    def _handle_control_bus_set_response(self, message):
        from supriya.commands import Response

        response = Response.from_osc_message(message)
        for item in response:
            bus_id = item.bus_id
            bus_proxy = self._get_control_bus_proxy(bus_id)
            bus_proxy._value = item.bus_value

    def _handle_control_bus_setn_response(self, message):
        from supriya.commands import Response

        response = Response.from_osc_message(message)
        for item in response:
            starting_bus_id = item.starting_bus_id
            for i, value in enumerate(item.bus_values):
                bus_id = starting_bus_id + i
                bus_proxy = self._get_control_bus_proxy(bus_id)
                bus_proxy._value = value

    def _handle_node_info_response(self, message):
        from supriya.realtime import Group, Synth
        from supriya.commands import Response

        response = Response.from_osc_message(message)
        with self._lock:
            node_id = response.node_id
            node = self._nodes.get(node_id)
            if node is not None:
                node._handle_response(response)
            elif response.action == NodeAction.NODE_CREATED:
                if response.is_group:
                    node = Group()
                else:
                    node = self._pending_synths.pop(node_id, Synth())
                node._register_with_local_server(server=self, node_id=response.node_id)
                parent = self._nodes[response.parent_id]
                node._set_parent(parent)
                if response.previous_node_id:
                    previous_child = self._nodes[response.previous_node_id]
                    index = parent.index(previous_child)
                    parent._children.insert(index + 1, node)
                else:
                    parent._children.append(node)

    def _handle_synthdef_removed_response(self, message):
        from supriya.commands import Response

        response = Response.from_osc_message(message)
        synthdef_name = response.synthdef_name
        self._synthdefs.pop(synthdef_name, None)

    def _setup_allocators(self):
        self._audio_bus_allocator = BlockAllocator(
            heap_maximum=self._options.audio_bus_channel_count,
            heap_minimum=self._options.first_private_bus_id,
        )
        self._buffer_allocator = BlockAllocator(heap_maximum=self._options.buffer_count)
        self._control_bus_allocator = BlockAllocator(
            heap_maximum=self._options.control_bus_channel_count
        )
        self._node_id_allocator = NodeIdAllocator(
            initial_node_id=self._options.initial_node_id, client_id=self.client_id
        )
        self._sync_id = self.client_id << 26

    def _setup_notifications(self):
        request = NotifyRequest(True)
        response = request.communicate(server=self)
        if isinstance(response, FailResponse):
            self._shutdown()
            raise supriya.exceptions.TooManyClients
        self._client_id, self._maximum_logins = response.action[1], response.action[2]

    def _setup_default_groups(self):
        default_groups = [
            supriya.Group(node_id_is_permanent=True) for _ in range(self.maximum_logins)
        ]
        self.root_node.extend(default_groups)
        self._default_group = default_groups[self.client_id]

    def _setup_proxies(self):
        import supriya.realtime

        self._audio_input_bus_group = supriya.realtime.AudioInputBusGroup(self)
        self._audio_output_bus_group = supriya.realtime.AudioOutputBusGroup(self)
        self._root_node = supriya.realtime.RootNode(server=self)
        self._nodes[0] = self._root_node

    def _setup_osc_callbacks(self):
        self._osc_protocol.register(
            pattern="/b_info", procedure=self._handle_buffer_info_response,
        )
        self._osc_protocol.register(
            pattern="/c_set", procedure=self._handle_control_bus_set_response,
        )
        self._osc_protocol.register(
            pattern="/c_setn", procedure=self._handle_control_bus_setn_response,
        )
        for pattern in (
            "/n_end",
            "/n_go",
            "/n_info",
            "/n_move",
            "/n_off",
            "/n_on",
            "/n_set",
            "/n_setn",
        ):
            self._osc_protocol.register(
                pattern=pattern, procedure=self._handle_node_info_response,
            )
        self._osc_protocol.register(
            pattern="/d_removed", procedure=self._handle_synthdef_removed_response,
        )

        def failed(message):
            logger.warning("Fail: {}".format(message))

        self._osc_protocol.register(pattern="/fail", procedure=failed)

    def _setup_status_watcher(self):
        self._status = None
        self._status_watcher = StatusWatcher(self)
        self._status_watcher.start()

    def _setup_system_synthdefs(self, local_only=False):
        import supriya.assets.synthdefs
        import supriya.synthdefs

        system_synthdefs = []
        for name in dir(supriya.assets.synthdefs):
            if not name.startswith("system_"):
                continue
            system_synthdef = getattr(supriya.assets.synthdefs, name)
            if not isinstance(system_synthdef, supriya.synthdefs.SynthDef):
                continue
            system_synthdefs.append(system_synthdef)
        if local_only:
            for synthdef in system_synthdefs:
                synthdef._register_with_local_server(self)
        else:
            supriya.synthdefs.SynthDef._allocate_synthdefs(system_synthdefs, self)

    def _shutdown(self):
        if not self.is_running:
            return
        elif self.is_owner:
            self.quit()
        else:
            self.disconnect()

    def _teardown_allocators(self):
        self._audio_bus_allocator = None
        self._buffer_allocator = None
        self._control_bus_allocator = None
        self._node_id_allocator = None
        self._sync_id = 0

    def _teardown_proxies(self):
        for set_ in tuple(self._audio_buses.values()):
            for x in tuple(set_):
                x.free()
        for set_ in tuple(self._buffers.values()):
            for x in tuple(set_):
                x.free()
        for set_ in tuple(self._control_buses.values()):
            for x in tuple(set_):
                x.free()
        for x in tuple(self._nodes.values()):
            x.free()
        self._audio_buses.clear()
        self._audio_input_bus_group = None
        self._audio_output_bus_group = None
        self._buffers.clear()
        self._buffer_proxies.clear()
        self._control_buses.clear()
        self._control_bus_proxies.clear()
        self._default_group = None
        self._nodes.clear()
        self._root_node = None
        self._synthdefs.clear()

    def _teardown_status_watcher(self):
        if self._status_watcher is not None:
            self._status_watcher.is_active = False
        self._status_watcher = None
        self._status = None

    ### PUBLIC METHODS ###

    def boot(self, scsynth_path=None, options=None, **kwargs):
        if self.is_running:
            return self
        self._options = new(options or BootOptions(), **kwargs)
        scsynth_path = BootOptions.find_scsynth(scsynth_path)
        self._server_process = self._options.boot(scsynth_path, self.port)
        self._is_owner = True
        self._connect()
        return self

    def _connect(self):
        self._is_running = True
        self._osc_protocol.connect(ip_address=self.ip_address, port=self.port)
        self._setup_osc_callbacks()
        self._setup_status_watcher()
        self._setup_notifications()
        self._setup_allocators()
        self._setup_proxies()
        if self.client_id == 0:
            self._setup_default_groups()
            self._setup_system_synthdefs()

    def _rehydrate(self):
        from supriya.realtime import Group, Synth

        def recurse(query_tree_node, node):
            for query_tree_child in query_tree_node.children:
                if isinstance(query_tree_child, QueryTreeGroup):
                    group = Group()
                    group._register_with_local_server(
                        node_id=query_tree_child.node_id, server=self
                    )
                    node._children.append(group)
                    recurse(query_tree_child, group)
                elif isinstance(query_tree_child, QueryTreeSynth):
                    synth = Synth()
                    synth._register_with_local_server(
                        node_id=query_tree_child.node_id, server=self
                    )
                    node._children.append(synth)
                    for query_tree_control in query_tree_child.children:
                        pass

        recurse(self.query_remote_nodes(include_controls=True), self.root_node)

    def connect(self):
        if self.is_running:
            return
        self._is_owner = False
        self._connect()
        if self.client_id > 0:
            self._setup_system_synthdefs(local_only=True)
            self._rehydrate()
        self._default_group = self._nodes[self.client_id + 1]
        return self

    def disconnect(self, force=False):
        if not self.is_running:
            raise supriya.exceptions.ServerOffline
        if self._is_owner and not force:
            raise supriya.exceptions.OwnedServerShutdown(
                "Cannot disconnect from owned server with force flag."
            )
        self._disconnect()
        return self

    def _disconnect(self):
        self._is_running = False
        self._is_owner = False
        self._client_id = None
        self._maximum_logins = None
        self._osc_protocol.disconnect()
        self._teardown_proxies()
        self._teardown_allocators()
        self._teardown_status_watcher()

    def quit(self, force=False):
        if not self.is_running:
            return
        if not self._is_owner and not force:
            raise supriya.exceptions.UnownedServerShutdown(
                "Cannot quit unowned server without force flag."
            )
        if self.recorder.is_recording:
            self.recorder.stop()
        QuitRequest().communicate(server=self)
        if self._server_process is not None and not self._server_process.terminate():
            self._server_process.wait()
        self._disconnect()
        return self

    @classmethod
    def default(cls):
        if cls._default_server is None:
            cls._default_server = Server()
        return cls._default_server

    @classmethod
    def kill(cls, supernova=False):
        BootOptions.kill(supernova=supernova)

    def query_local_nodes(self, include_controls=False):
        """
        Queries all node proxies in Python.

        ::

            >>> import supriya.realtime
            >>> server = supriya.Server.default()
            >>> server.boot()
            <Server: udp://127.0.0.1:57751, 8i8o>

        ::

            >>> group_a = supriya.realtime.Group().allocate()
            >>> group_b = supriya.realtime.Group().allocate()
            >>> group_c = supriya.realtime.Group().allocate(target_node=group_a)

        ::

            >>> import supriya.synthdefs
            >>> import supriya.ugens
            >>> with supriya.synthdefs.SynthDefBuilder(
            ...     amplitude=0.0,
            ...     frequency=440.0,
            ...     ) as builder:
            ...     sin_osc = supriya.ugens.SinOsc.ar(
            ...         frequency=builder['frequency'],
            ...         )
            ...     sin_osc *= builder['amplitude']
            ...     out = supriya.ugens.Out.ar(
            ...         bus=0,
            ...         source=[sin_osc, sin_osc],
            ...         )
            ...
            >>> synthdef = builder.build()
            >>> synthdef.allocate()
            <SynthDef: e41193ac8b7216f49ff0d477876a3bf3>

        ::

            >>> synth = supriya.realtime.Synth(synthdef).allocate(
            ...     target_node=group_b,
            ...     )

        ::

            >>> response = server.query_local_nodes(include_controls=True)
            >>> print(response)
            NODE TREE 0 group
                1 group
                    1001 group
                        1003 e41193ac8b7216f49ff0d477876a3bf3
                            amplitude: 0.0, frequency: 440.0
                    1000 group
                        1002 group

        ::

            >>> server.quit()
            <Server: offline>

        Returns server query-tree group response.
        """
        query_tree_group = QueryTreeGroup.from_group(
            self.root_node, include_controls=include_controls
        )
        return query_tree_group

    def query_remote_nodes(self, include_controls=False):
        """
        Queries all nodes on scsynth.

        ::

            >>> import supriya.realtime
            >>> server = supriya.Server.default()
            >>> server.boot()
            <Server: udp://127.0.0.1:57751, 8i8o>

        ::

            >>> group_a = supriya.realtime.Group().allocate()
            >>> group_b = supriya.realtime.Group().allocate()
            >>> group_c = supriya.realtime.Group().allocate(target_node=group_a)

        ::

            >>> import supriya.synthdefs
            >>> import supriya.ugens
            >>> with supriya.synthdefs.SynthDefBuilder(
            ...     amplitude=0.0,
            ...     frequency=440.0,
            ...     ) as builder:
            ...     sin_osc = supriya.ugens.SinOsc.ar(
            ...         frequency=builder['frequency'],
            ...         )
            ...     sin_osc *= builder['amplitude']
            ...     out = supriya.ugens.Out.ar(
            ...         bus=0,
            ...         source=[sin_osc, sin_osc],
            ...         )
            ...
            >>> synthdef = builder.build()
            >>> synthdef.allocate()
            <SynthDef: e41193ac8b7216f49ff0d477876a3bf3>

        ::

            >>> synth = supriya.realtime.Synth(synthdef).allocate(
            ...     target_node=group_b,
            ...     )

        ::

            >>> response = server.query_remote_nodes(include_controls=False)
            >>> print(response)
            NODE TREE 0 group
                1 group
                    1001 group
                        1003 e41193ac8b7216f49ff0d477876a3bf3
                    1000 group
                        1002 group

        ::

            >>> server.quit()
            <Server: offline>

        Returns server query-tree group response.
        """
        request = GroupQueryTreeRequest(node_id=0, include_controls=include_controls)
        response = request.communicate(server=self)
        return response.query_tree_group

    def reboot(self, options=None, **kwargs):
        self.quit()
        self.boot(options=options, **kwargs)
        return self

    def send_message(self, message, with_request_name=False):
        if not message or not self.is_running:
            return
        self._osc_protocol.send(
            message, with_request_name=with_request_name or self.debug_request_names
        )

    def sync(self, sync_id=None):
        if not self.is_running:
            return
        if sync_id is None:
            sync_id = self.next_sync_id
        request = SyncRequest(sync_id=sync_id)
        request.communicate(server=self)
        return self

    ### PUBLIC PROPERTIES ###

    @property
    def audio_bus_allocator(self):
        return self._audio_bus_allocator

    @property
    def audio_input_bus_group(self):
        return self._audio_input_bus_group

    @property
    def audio_output_bus_group(self):
        return self._audio_output_bus_group

    @property
    def buffer_allocator(self):
        return self._buffer_allocator

    @property
    def client_id(self):
        return self._client_id

    @property
    def control_bus_allocator(self):
        return self._control_bus_allocator

    @property
    def debug_request_names(self):
        return self._debug_request_names

    @debug_request_names.setter
    def debug_request_names(self, expr):
        self._debug_request_names = bool(expr)

    @property
    def default_group(self):
        return self._default_group

    @property
    def ip_address(self):
        return self._ip_address

    @property
    def is_owner(self):
        return self._is_owner

    @property
    def is_running(self):
        return self._is_running

    @property
    def latency(self):
        return self._latency

    @latency.setter
    def latency(self, latency):
        self._latency = float(latency)

    @property
    def maximum_logins(self):
        return self._maximum_logins

    @property
    def meters(self):
        return self._meters

    @property
    def next_sync_id(self):
        sync_id = self._sync_id
        self._sync_id += 1
        return sync_id

    @property
    def node_id_allocator(self):
        return self._node_id_allocator

    @property
    def osc_protocol(self):
        return self._osc_protocol

    @property
    def port(self):
        return self._port

    @property
    def recorder(self):
        return self._recorder

    @property
    def root_node(self):
        return self._root_node

    @property
    def options(self):
        return self._options

    @property
    def status(self):
        return self._status


class StatusWatcher(threading.Thread):

    ### CLASS VARIABLES ###

    __documentation_section__ = "Server Internals"

    __slots__ = ("_is_active", "_attempts", "_callback", "_server")

    max_attempts = 5
    sleep_base_time = 1.0
    exponential_backoff_factor = 1.5

    ### INITIALIZER ###

    def __init__(self, server):
        threading.Thread.__init__(self)
        self._attempts = 0
        self._server = server
        self._callback = None
        self.is_active = True
        self.daemon = True

    ### SPECIAL METHODS ###

    def __call__(self, response):
        if not self.is_active:
            return
        if response is None:
            return
        self._server._status = response
        self._attempts = 0

    ### PUBLIC METHODS ###

    def run(self):
        import supriya.commands

        self._callback = self.server.osc_protocol.register(
            pattern="/status.reply", procedure=self.__call__
        )
        request = supriya.commands.StatusRequest()
        message = request.to_osc()
        while self._is_active and self.server.is_running:
            if self.max_attempts == self.attempts:
                print("+" * 80)
                print("SHUTTING DOWN")
                print("+" * 80)
                self.server._shutdown()
                break
            self._attempts += 1
            self.server.send_message(message)
            sleep_time = self.sleep_base_time * pow(
                self.exponential_backoff_factor, self._attempts
            )
            time.sleep(sleep_time)
        self.server.osc_protocol.unregister(self.callback)

    ### PUBLIC PROPERTIES ###

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, expr):
        self._is_active = bool(expr)

    @property
    def attempts(self):
        return self._attempts

    @property
    def callback(self):
        return self._callback

    @property
    def server(self):
        return self._server
