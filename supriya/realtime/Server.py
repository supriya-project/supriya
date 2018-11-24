import os
import pathlib
import signal
import atexit
import re
import subprocess
import supriya.exceptions
import threading
import time
import uqbar.graphs
import uqbar.io
from supriya import utils
from supriya.system import PubSub
from supriya.system.SupriyaObject import SupriyaObject
from typing import Dict, Tuple


class Server(SupriyaObject):
    """
    An scsynth server proxy.

    ::

        >>> import supriya.realtime
        >>> server = supriya.realtime.Server.get_default_server()
        >>> server.boot()
        <Server: udp://127.0.0.1:57751, 8i8o>

    ::

        >>> server.quit()
        <Server: offline>

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Main Classes'

    __slots__ = (
        '_audio_bus_allocator',
        '_audio_buses',
        '_audio_input_bus_group',
        '_audio_output_bus_group',
        '_buffer_allocator',
        '_buffers',
        '_buffer_proxies',
        '_control_bus_allocator',
        '_control_buses',
        '_control_bus_proxies',
        '_debug_subprocess',
        '_debug_osc',
        '_debug_udp',
        '_default_group',
        '_ip_address',
        '_is_running',
        '_latency',
        '_lock',
        '_meters',
        '_node_id_allocator',
        '_nodes',
        '_osc_io',
        '_pending_nodes',
        '_port',
        '_recorder',
        '_root_node',
        '_server_options',
        '_server_process',
        '_status',
        '_status_watcher',
        '_sync_id',
        '_synthdefs',
    )

    _default_server = None

    _servers: Dict[Tuple[str, int], 'Server'] = {}

    ### CONSTRUCTOR ###

    def __new__(cls, ip_address='127.0.0.1', port=57751, **kwargs):
        key = (ip_address, port)
        if key not in cls._servers:
            instance = object.__new__(cls)
            instance.__init__(ip_address=ip_address, port=port, **kwargs)
            cls._servers[key] = instance
        return cls._servers[key]

    ### INITIALIZER ###

    def __init__(self, ip_address='127.0.0.1', port=57751):
        import supriya.osc
        import supriya.commands
        import supriya.realtime

        if hasattr(self, 'is_running') and self.is_running:
            return

        ### NET ADDRESS ###

        self._ip_address = ip_address
        self._port = port

        ### OSC MESSAGING ###

        self._latency = 0.1
        self._lock = threading.Lock()
        self._osc_io = supriya.osc.OscIO()

        ### ALLOCATORS ###

        self._audio_bus_allocator = None
        self._buffer_allocator = None
        self._control_bus_allocator = None
        self._node_id_allocator = None
        self._sync_id = 0

        ### SERVER PROCESS ###

        self._is_running = False
        self._server_options = supriya.realtime.ServerOptions()
        self._server_process = None
        self._status = None
        self._status_watcher = None

        ### PROXIES ###

        self._audio_input_bus_group = None
        self._audio_output_bus_group = None
        self._default_group = None
        self._root_node = None
        self._meters = supriya.realtime.ServerMeters(self)
        self._recorder = supriya.realtime.ServerRecorder(self)

        ### PROXY MAPPINGS ###

        self._audio_buses = {}
        self._buffer_proxies = {}
        self._buffers = {}
        self._control_bus_proxies = {}
        self._control_buses = {}
        self._nodes = {}
        self._pending_nodes = {}
        self._synthdefs = {}

        ### DEBUG ###

        self.debug_osc = False
        self.debug_subprocess = False
        self.debug_udp = False

        ### REGISTER WITH ATEXIT ###

        atexit.register(self.quit)

    ### SPECIAL METHODS ###

    def __contains__(self, expr):
        import supriya.realtime
        import supriya.synthdefs

        if not isinstance(expr, supriya.realtime.ServerObjectProxy):
            return False
        if expr.server is not self:
            return False
        if isinstance(expr, supriya.realtime.Node):
            node_id = expr.node_id
            if node_id in self._nodes and self._nodes[node_id] is expr:
                return True
        if isinstance(expr, supriya.synthdefs.SynthDef):
            name = expr.actual_name
            if name in self._synthdefs and self._synthdefs[name] == expr:
                return True
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

            >>> server = supriya.Server().boot()
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
            match = re.match('b(?P<id>\d+)', item)
            if match:
                id_ = int(match.groupdict()['id'])
                return supriya.realtime.Buffer(id_).allocate(server=self)
            match = re.match('c(?P<id>\d+)', item)
            if match:
                id_ = int(match.groupdict()['id'])
                return supriya.realtime.Bus(id_, 'control').allocate(server=self)
            match = re.match('a(?P<id>\d+)', item)
            if match:
                id_ = int(match.groupdict()['id'])
                return supriya.realtime.Bus(id_, 'audio').allocate(server=self)
            result = self.root_node[item]
        elif isinstance(item, int):
            result = self._nodes.get(item)
        else:
            raise ValueError(item)
        if isinstance(result, set) and len(result) == 1:
            return tuple(result)[0]
        return result

    def __graph__(self):
        '''
        Graph server.

        ::

            >>> import supriya
            >>> server = supriya.Server().boot()
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
            digraph server {
                "Root Node";
                "Group 1";
                "Group 1000";
                "Synth 1001";
                "Group 1002";
                "Synth 1003";
                "Synth 1004";
                "Root Node" -> "Group 1";
                "Group 1" -> "Group 1000";
                "Group 1000" -> "Synth 1001";
                "Group 1000" -> "Group 1002";
                "Group 1002" -> "Synth 1003";
                "Group 1002" -> "Synth 1004";
            }

        ::

            >>> supriya.graph(server)  # doctest: +SKIP

        '''

        def recurse(graph, parent_graphviz_node, parent_server_node):
            if not isinstance(parent_server_node, supriya.realtime.Group):
                return
            for child_server_node in parent_server_node:
                if isinstance(child_server_node, supriya.realtime.Group):
                    name = 'Group {}'.format(child_server_node.node_id)
                else:
                    name = 'Synth {}'.format(child_server_node.node_id)
                child_graphviz_node = uqbar.graphs.Node(name=name)
                graph.append(child_graphviz_node)
                parent_graphviz_node.attach(child_graphviz_node)
                recurse(graph, child_graphviz_node, child_server_node)

        import supriya.realtime

        graph = uqbar.graphs.Graph(name='server')
        root_graphviz_node = uqbar.graphs.Node(name='Root Node')
        graph.append(root_graphviz_node)
        recurse(graph, root_graphviz_node, self.root_node)
        return graph

    def __repr__(self):
        if not self.is_running:
            return '<Server: offline>'
        string = '<Server: {protocol}://{ip}:{port}, '
        string += '{inputs}i{outputs}o>'
        return string.format(
            protocol=self.server_options.protocol,
            ip=self.ip_address,
            port=self.port,
            inputs=self.server_options.input_bus_channel_count,
            outputs=self.server_options.output_bus_channel_count,
        )

    def __str__(self):
        if self.is_running:
            return str(self.query_remote_nodes(True))
        return ''

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

    def _handle_buffer_info_response(self, response):
        for item in response.items:
            buffer_proxy = self._get_buffer_proxy(item.buffer_id)
            if buffer_proxy:
                buffer_proxy._handle_response(item)

    def _handle_control_bus_set_response(self, response):
        for item in response:
            bus_id = item.bus_id
            bus_proxy = self._get_control_bus_proxy(bus_id)
            bus_proxy._value = item.bus_value

    def _handle_control_bus_setn_response(self, response):
        for item in response:
            starting_bus_id = item.starting_bus_id
            for i, value in enumerate(item.bus_values):
                bus_id = starting_bus_id + i
                bus_proxy = self._get_control_bus_proxy(bus_id)
                bus_proxy._value = value

    def _handle_node_info_response(self, response):
        from supriya.commands import NodeAction
        from supriya.realtime import Group, Synth

        with self._lock:
            node_id = response.node_id
            node = self._nodes.get(node_id)
            if node is not None:
                node._handle_response(response)
            elif response.action == NodeAction.NODE_CREATED:
                if response.is_group:
                    node = Group()
                else:
                    node = Synth()
                node._register_with_local_server(server=self, node_id=response.node_id)
                parent = self._nodes[response.parent_group_id]
                node._set_parent(parent)
                if response.previous_node_id:
                    previous_child = self._nodes[response.previous_node_id]
                    index = parent.index(previous_child)
                    parent._children.insert(index + 1, node)
                else:
                    parent._children.append(node)

    def _handle_synthdef_removed_response(self, response):
        synthdef_name = response.synthdef_name
        synthdef = self._synthdefs.get(synthdef_name)
        if synthdef is None:
            return
        synthdef._handle_response(response)

    def _setup(self):
        self._setup_notifications()
        self._setup_status_watcher()
        self._setup_allocators(self.server_options)
        self._setup_proxies()
        self._setup_system_synthdefs()

    def _setup_allocators(self, server_options):
        import supriya.realtime

        self._audio_bus_allocator = supriya.realtime.BlockAllocator(
            heap_maximum=server_options.audio_bus_channel_count,
            heap_minimum=server_options.first_private_bus_id,
        )
        self._buffer_allocator = supriya.realtime.BlockAllocator(
            heap_maximum=server_options.buffer_count
        )
        self._control_bus_allocator = supriya.realtime.BlockAllocator(
            heap_maximum=server_options.control_bus_channel_count
        )
        self._node_id_allocator = supriya.realtime.NodeIdAllocator(
            initial_node_id=server_options.initial_node_id
        )
        self._sync_id = 0

    def _setup_notifications(self):
        import supriya.commands

        request = supriya.commands.NotifyRequest(True)
        request.communicate(server=self)

    def _setup_proxies(self):
        import supriya.realtime

        self._pending_nodes = {}
        self._audio_input_bus_group = supriya.realtime.AudioInputBusGroup(self)
        self._audio_output_bus_group = supriya.realtime.AudioOutputBusGroup(self)
        self._root_node = supriya.realtime.RootNode(server=self)
        self._nodes[0] = self._root_node
        default_group = supriya.realtime.Group()
        default_group.allocate(
            add_action=supriya.AddAction.ADD_TO_HEAD,
            node_id_is_permanent=True,
            target_node=self.root_node,
        )
        self._default_group = default_group

    def _setup_osc_callbacks(self):
        self._osc_io.register(
            pattern='/b_info',
            procedure=self._handle_buffer_info_response,
            parse_response=True,
        )
        self._osc_io.register(
            pattern='/c_set',
            procedure=self._handle_control_bus_set_response,
            parse_response=True,
        )
        self._osc_io.register(
            pattern='/c_setn',
            procedure=self._handle_control_bus_setn_response,
            parse_response=True,
        )
        for pattern in (
            '/n_end',
            '/n_go',
            '/n_info',
            '/n_move',
            '/n_off',
            '/n_on',
            '/n_set',
            '/n_setn',
        ):
            self._osc_io.register(
                pattern=pattern,
                procedure=self._handle_node_info_response,
                parse_response=True,
            )
        self._osc_io.register(
            pattern='/d_removed',
            procedure=self._handle_synthdef_removed_response,
            parse_response=True,
        )

        def failed(message):
            print('FAILED:', message)

        self._osc_io.register(pattern='/fail', procedure=failed)

    def _setup_status_watcher(self):
        import supriya.realtime

        self._status = None
        self._status_watcher = supriya.realtime.StatusWatcher(self)
        self._status_watcher.start()

    def _setup_system_synthdefs(self):
        import supriya.assets.synthdefs
        import supriya.synthdefs

        system_synthdefs = []
        for name in dir(supriya.assets.synthdefs):
            if not name.startswith('system_'):
                continue
            system_synthdef = getattr(supriya.assets.synthdefs, name)
            if not isinstance(system_synthdef, supriya.synthdefs.SynthDef):
                continue
            system_synthdefs.append(system_synthdef)
        supriya.synthdefs.SynthDef._allocate_synthdefs(system_synthdefs, self)

    def _teardown(self):
        self._teardown_proxies()
        self._teardown_allocators()
        self._teardown_status_watcher()

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
        for x in tuple(self._synthdefs.values()):
            x.free()
        self._control_bus_proxies = None
        self._buffer_proxies = None
        self._default_group = None
        self._root_node = None
        self._audio_input_bus_group = None
        self._audio_output_bus_group = None
        self._nodes.clear()
        self._synthdefs.clear()

    def _teardown_status_watcher(self):
        self._status_watcher.active = False
        self._status_watcher = None
        self._status = None

    def _read_scsynth_boot_output(self):
        start_time = time.time()
        timeout = 10
        while True:
            line = self._server_process.stdout.readline().decode().rstrip()
            if self.debug_subprocess and line:
                print('Boot:', line)
            if line.startswith('SuperCollider 3 server ready'):
                break
            elif line.startswith('ERROR:'):
                raise supriya.exceptions.ServerCannotBoot(line)
            elif line.startswith(
                'Exception in World_OpenUDP: bind: Address already in use'
            ):
                raise supriya.exceptions.ServerCannotBoot(line)
            elif (time.time() - start_time) > timeout:
                raise supriya.exceptions.ServerCannotBoot(line)

    ### PUBLIC METHODS ###

    def boot(self, scsynth_path=None, server_options=None, **kwargs):
        import supriya.realtime

        if self.is_running:
            return self
        scsynth_path = scsynth_path or os.environ.get('SCSYNTH_PATH')
        if not scsynth_path:
            scsynth_path_candidates = uqbar.io.find_executable('scsynth')
            if not scsynth_path_candidates:
                raise RuntimeError('Cannot find scsynth')
            scsynth_path = scsynth_path_candidates[0]
        scsynth_path = pathlib.Path(scsynth_path).absolute()
        if not scsynth_path.exists():
            raise RuntimeError('{} does not exist'.format(scsynth_path))

        self._osc_io.boot(ip_address=self.ip_address, port=self.port)
        self._setup_osc_callbacks()

        server_options = server_options or supriya.realtime.ServerOptions()
        assert isinstance(server_options, supriya.realtime.ServerOptions)
        if kwargs:
            server_options = utils.new(server_options, **kwargs)
        options_string = server_options.as_options_string(self.port)
        command = '{} {}'.format(scsynth_path, options_string)
        if self.debug_subprocess:
            print('Boot:', command)
        process = self._server_process = subprocess.Popen(
            command,
            shell=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            start_new_session=True,
        )
        try:
            self._read_scsynth_boot_output()
        except supriya.exceptions.ServerCannotBoot:
            self._osc_io.quit()
            try:
                process_group = os.getpgid(process.pid)
                os.killpg(process_group, signal.SIGINT)
                process.terminate()
                process.wait()
            except ProcessLookupError:
                pass
            raise
        self._is_running = True
        self._server_options = server_options
        self._setup()
        PubSub.notify('server-booted')
        return self

    @staticmethod
    def get_default_server():
        if Server._default_server is None:
            Server._default_server = Server()
        return Server._default_server

    def query_local_nodes(self, include_controls=False):
        """
        Queries all node proxies in Python.

        ::

            >>> import supriya.realtime
            >>> server = supriya.realtime.Server()
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

            >>> response = server.query_remote_nodes(include_controls=True)
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
        import supriya.commands

        query_tree_group = supriya.commands.QueryTreeGroup.from_group(
            self.root_node, include_controls=include_controls
        )
        return query_tree_group

    def query_remote_nodes(self, include_controls=False):
        """
        Queries all nodes on scsynth.

        ::

            >>> import supriya.realtime
            >>> server = supriya.realtime.Server()
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

            >>> response = server.query_local_nodes(include_controls=False)
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
        import supriya.commands

        request = supriya.commands.GroupQueryTreeRequest(
            node_id=0, include_controls=include_controls
        )
        response = request.communicate(server=self)
        return response.query_tree_group

    def quit(self):
        import supriya.commands

        if not self.is_running:
            return
        PubSub.notify('server-quitting')
        if self.recorder.is_recording:
            self.recorder.stop()
        request = supriya.commands.QuitRequest()
        request.communicate(server=self)
        self._is_running = False
        if not self._server_process.terminate():
            self._server_process.wait()
        self._osc_io.quit()
        self._teardown()
        PubSub.notify('server-quit')
        return self

    def send_message(self, message):
        if not message or not self.is_running:
            return
        self._osc_io.send(message)

    def sync(self, sync_id=None):
        import supriya.commands

        if not self.is_running:
            return
        if sync_id is None:
            sync_id = self.next_sync_id
        request = supriya.commands.SyncRequest(sync_id=sync_id)
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
    def control_bus_allocator(self):
        return self._control_bus_allocator

    @property
    def debug_osc(self):
        return self._debug_osc

    @debug_osc.setter
    def debug_osc(self, expr):
        self._debug_osc = bool(expr)
        self._osc_io.debug_osc = self.debug_osc

    @property
    def debug_subprocess(self):
        return self._debug_subprocess

    @debug_subprocess.setter
    def debug_subprocess(self, expr):
        self._debug_subprocess = bool(expr)

    @property
    def debug_udp(self):
        return self._debug_udp

    @debug_udp.setter
    def debug_udp(self, expr):
        self._debug_udp = bool(expr)
        self._osc_io.debug_udp = self.debug_udp

    @property
    def default_group(self):
        return self._default_group

    @property
    def ip_address(self):
        return self._ip_address

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
    def osc_io(self):
        return self._osc_io

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
    def server_options(self):
        return self._server_options

    @property
    def status(self):
        return self._status
