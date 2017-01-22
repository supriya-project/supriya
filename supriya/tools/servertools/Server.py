# -*- encoding: utf-8 -*-
from __future__ import print_function
import atexit
import os
import subprocess
import time
from supriya.tools.systemtools import PubSub
from supriya.tools.systemtools import SupriyaObject


class Server(SupriyaObject):
    """
    An scsynth server proxy.

    ::

        >>> from supriya import servertools
        >>> server = servertools.Server.get_default_server()
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
        '_meters',
        '_node_id_allocator',
        '_nodes',
        '_osc_controller',
        '_osc_dispatcher',
        '_port',
        '_recorder',
        '_response_dispatcher',
        '_root_node',
        '_server_options',
        '_server_process',
        '_status',
        '_status_watcher',
        '_sync_id',
        '_synthdefs',
        )

    _default_server = None

    _servers = {}

    ### CONSTRUCTOR ###

    def __new__(
        cls,
        ip_address='127.0.0.1',
        port=57751,
        **kwargs
        ):
        key = (ip_address, port)
        if key not in cls._servers:
            instance = object.__new__(cls)
            instance.__init__(
                ip_address=ip_address,
                port=port,
                **kwargs
                )
            cls._servers[key] = instance
        return cls._servers[key]

    ### INITIALIZER ###

    def __init__(
        self,
        ip_address='127.0.0.1',
        port=57751,
        ):
        from supriya.tools import osctools
        from supriya.tools import responsetools
        from supriya.tools import servertools

        if hasattr(self, 'is_running') and self.is_running:
            return

        ### NET ADDRESS ###

        self._ip_address = ip_address
        self._port = port

        ### OSC MESSAGING ###

        self._latency = 0.1
        self._response_dispatcher = responsetools.ResponseDispatcher()
        self._osc_dispatcher = osctools.OscDispatcher()
        self._osc_controller = osctools.OscController(server=self)
        for callback in (
            responsetools.BufferResponseCallback(self),
            responsetools.ControlBusResponseCallback(self),
            responsetools.NodeResponseCallback(self),
            responsetools.SynthDefResponseCallback(self),
            ):
            self.register_response_callback(callback)

        fail_callback = osctools.OscCallback(
            address_pattern='/fail',
            procedure=lambda message: print('FAILED:', message),
            )
        self.register_osc_callback(fail_callback)

        ### ALLOCATORS ###

        self._audio_bus_allocator = None
        self._buffer_allocator = None
        self._control_bus_allocator = None
        self._node_id_allocator = None

        ### SERVER PROCESS ###

        self._is_running = False
        self._server_options = servertools.ServerOptions()
        self._server_process = None
        self._status = None
        self._status_watcher = None

        ### PROXIES ###

        self._audio_input_bus_group = None
        self._audio_output_bus_group = None
        self._default_group = None
        self._root_node = None
        self._meters = servertools.ServerMeters(self)
        self._recorder = servertools.ServerRecorder(self)

        ### PROXY MAPPINGS ###

        self._audio_buses = {}
        self._control_buses = {}
        self._control_bus_proxies = {}
        self._buffers = {}
        self._buffer_proxies = {}
        self._nodes = {}
        self._synthdefs = {}

        ### DEBUG ###

        self.debug_osc = False
        self.debug_subprocess = False
        self.debug_udp = False

        ### REGISTER WITH ATEXIT ###

        atexit.register(self.quit)

    ### SPECIAL METHODS ###

    def __contains__(self, expr):
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        if not isinstance(expr, servertools.ServerObjectProxy):
            return False
        elif expr.server is not self:
            return False
        elif isinstance(expr, servertools.Node):
            node_id = expr.node_id
            if node_id in self._nodes and self._nodes[node_id] is expr:
                return True
        elif isinstance(expr, synthdeftools.SynthDef):
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

    def __graph__(self):
        def recurse(graph, parent_graphviz_node, parent_server_node):
            if not isinstance(parent_server_node, servertools.Group):
                return
            for child_server_node in parent_server_node:
                if isinstance(child_server_node, servertools.Group):
                    name = 'Group {}'.format(child_server_node.node_id)
                else:
                    name = 'Synth {}'.format(child_server_node.node_id)
                child_graphviz_node = documentationtools.GraphvizNode(
                    name=name,
                    )
                graph.append(child_graphviz_node)
                documentationtools.GraphvizEdge()(
                    parent_graphviz_node,
                    child_graphviz_node,
                    )
                recurse(graph, child_graphviz_node, child_server_node)
        from abjad.tools import documentationtools
        from supriya.tools import servertools
        graph = documentationtools.GraphvizGraph(
            name='server',
            )
        root_graphviz_node = documentationtools.GraphvizNode(name='Root Node')
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

    def _get_buffer_proxy(self, buffer_id):
        from supriya.tools import servertools
        buffer_proxy = self._buffer_proxies.get(buffer_id)
        if not buffer_proxy:
            buffer_proxy = servertools.BufferProxy(
                buffer_id=buffer_id,
                server=self,
                )
            self._buffer_proxies[buffer_id] = buffer_proxy
        return buffer_proxy

    def _get_control_bus_proxy(self, bus_id):
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        control_bus_proxy = self._control_bus_proxies.get(bus_id)
        if not control_bus_proxy:
            control_bus_proxy = servertools.BusProxy(
                bus_id=bus_id,
                calculation_rate=synthdeftools.CalculationRate.CONTROL,
                server=self,
                )
            self._control_bus_proxies[bus_id] = control_bus_proxy
        return control_bus_proxy

    def _setup(self):
        self._setup_notifications()
        self._setup_status_watcher()
        self._setup_allocators(self.server_options)
        self._setup_proxies()
        self._setup_system_synthdefs()

    def _setup_allocators(self, server_options):
        from supriya.tools import servertools
        self._audio_bus_allocator = servertools.BlockAllocator(
            heap_maximum=server_options.audio_bus_channel_count,
            heap_minimum=server_options.first_private_bus_id,
            )
        self._buffer_allocator = servertools.BlockAllocator(
            heap_maximum=server_options.buffer_count,
            )
        self._control_bus_allocator = servertools.BlockAllocator(
            heap_maximum=server_options.control_bus_channel_count,
            )
        self._node_id_allocator = servertools.NodeIdAllocator(
            initial_node_id=server_options.initial_node_id,
            )
        self._sync_id = 0

    def _setup_notifications(self):
        from supriya.tools import requesttools
        request = requesttools.NotifyRequest(True)
        request.communicate(server=self)

    def _setup_proxies(self):
        from supriya.tools import servertools
        self._audio_input_bus_group = servertools.AudioInputBusGroup(self)
        self._audio_output_bus_group = servertools.AudioOutputBusGroup(self)
        self._root_node = servertools.RootNode(server=self)
        self._nodes[0] = self._root_node
        default_group = servertools.Group()
        default_group.allocate(
            add_action=servertools.AddAction.ADD_TO_HEAD,
            node_id_is_permanent=True,
            target_node=self.root_node,
            )
        self._default_group = default_group

    def _setup_status_watcher(self):
        from supriya.tools import servertools
        self._status = None
        self._status_watcher = servertools.StatusWatcher(self)
        self._status_watcher.start()

    def _setup_system_synthdefs(self):
        from supriya import synthdefs
        from supriya.tools import synthdeftools
        system_synthdefs = []
        for name in dir(synthdefs):
            if not name.startswith('system_'):
                continue
            system_synthdef = getattr(synthdefs, name)
            if not isinstance(system_synthdef, synthdeftools.SynthDef):
                continue
            system_synthdefs.append(system_synthdef)
        synthdeftools.SynthDef._allocate_synthdefs(system_synthdefs, self)

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

    ### PUBLIC METHODS ###

    def boot(
        self,
        server_options=None,
        **kwargs
        ):
        from supriya import new
        from supriya import supriya_configuration
        from supriya.tools import servertools
        if self.is_running:
            return self
        scsynth_path = supriya_configuration.scsynth_path
        self._osc_controller.boot()
        server_options = server_options or servertools.ServerOptions()
        assert isinstance(server_options, servertools.ServerOptions)
        if kwargs:
            server_options = new(server_options, **kwargs)
        options_string = server_options.as_options_string(self.port)
        command = '{} {} -V -1'.format(scsynth_path, options_string)
        #command = '{} {}'.format(scsynth_path, options_string)
        if self.debug_subprocess:
            print(command)
        self._server_process = subprocess.Popen(command, shell=True)
        time.sleep(0.25)
        self._is_running = True
        self._server_options = server_options
        self._setup()
        self.sync()
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

            >>> from supriya import servertools
            >>> server = servertools.Server()
            >>> server.boot()
            <Server: udp://127.0.0.1:57751, 8i8o>

        ::

            >>> group_a = servertools.Group().allocate()
            >>> group_b = servertools.Group().allocate()
            >>> group_c = servertools.Group().allocate(target_node=group_a)

        ::

            >>> from supriya import synthdeftools
            >>> from supriya import ugentools
            >>> with synthdeftools.SynthDefBuilder(
            ...     amplitude=0.0,
            ...     frequency=440.0,
            ...     ) as builder:
            ...     sin_osc = ugentools.SinOsc.ar(
            ...         frequency=builder['frequency'],
            ...         )
            ...     sin_osc *= builder['amplitude']
            ...     out = ugentools.Out.ar(
            ...         bus=0,
            ...         source=[sin_osc, sin_osc],
            ...         )
            ...
            >>> synthdef = builder.build()
            >>> synthdef.allocate()
            <SynthDef: e41193ac8b7216f49ff0d477876a3bf3>

        ::

            >>> synth = servertools.Synth(synthdef).allocate(
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
        from supriya.tools import responsetools
        query_tree_group = responsetools.QueryTreeGroup.from_group(
            self.root_node,
            include_controls=include_controls,
            )
        return query_tree_group

    def query_remote_nodes(self, include_controls=False):
        """
        Queries all nodes on scsynth.

        ::

            >>> from supriya import servertools
            >>> server = servertools.Server()
            >>> server.boot()
            <Server: udp://127.0.0.1:57751, 8i8o>

        ::

            >>> group_a = servertools.Group().allocate()
            >>> group_b = servertools.Group().allocate()
            >>> group_c = servertools.Group().allocate(target_node=group_a)

        ::

            >>> from supriya import synthdeftools
            >>> from supriya import ugentools
            >>> with synthdeftools.SynthDefBuilder(
            ...     amplitude=0.0,
            ...     frequency=440.0,
            ...     ) as builder:
            ...     sin_osc = ugentools.SinOsc.ar(
            ...         frequency=builder['frequency'],
            ...         )
            ...     sin_osc *= builder['amplitude']
            ...     out = ugentools.Out.ar(
            ...         bus=0,
            ...         source=[sin_osc, sin_osc],
            ...         )
            ...
            >>> synthdef = builder.build()
            >>> synthdef.allocate()
            <SynthDef: e41193ac8b7216f49ff0d477876a3bf3>

        ::

            >>> synth = servertools.Synth(synthdef).allocate(
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
        from supriya.tools import requesttools
        request = requesttools.GroupQueryTreeRequest(
            node_id=0,
            include_controls=include_controls,
            )
        response = request.communicate(server=self)
        return response.query_tree_group

    def quit(self):
        from supriya.tools import requesttools
        if not self.is_running:
            return
        PubSub.notify('server-quitting')
        if self.recorder.is_recording:
            self.recorder.stop()
        request = requesttools.QuitRequest()
        request.communicate(server=self)
        self._is_running = False
        if not self._server_process.terminate():
            self._server_process.wait()
        self._osc_controller.quit()
        self._teardown()
        PubSub.notify('server-quit')
        return self

    def register_osc_callback(self, osc_callback):
        self._osc_dispatcher.register_callback(osc_callback)

    def register_response_callback(self, response_callback):
        self.response_dispatcher.register_callback(response_callback)

    def send_message(self, message):
        if not message or not self.is_running:
            return
        self._osc_controller.send(message)

    def sync(self, sync_id=None):
        from supriya.tools import requesttools
        if not self.is_running:
            return
        if sync_id is None:
            sync_id = self.next_sync_id
        request = requesttools.SyncRequest(sync_id=sync_id)
        request.communicate(server=self)
        return self

    def unregister_osc_callback(self, osc_callback):
        self._osc_dispatcher.unregister_callback(osc_callback)

    def unregister_response_callback(self, response_callback):
        self.response_dispatcher.unregister_callback(response_callback)

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
        self._osc_controller.debug_osc = self.debug_osc

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
        self._osc_controller.debug_udp = self.debug_udp

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
    def port(self):
        return self._port

    @property
    def recorder(self):
        return self._recorder

    @property
    def response_dispatcher(self):
        return self._response_dispatcher

    @property
    def root_node(self):
        return self._root_node

    @property
    def server_options(self):
        return self._server_options

    @property
    def status(self):
        return self._status
