# -*- encoding: utf-8 -*-
from __future__ import print_function
import atexit
import pexpect
import sys
import time


class Server(object):
    r'''An scsynth server proxy.

    ::

        >>> from supriya import servertools
        >>> server = servertools.Server.get_default_server()
        >>> server.boot()
        <Server: udp://127.0.0.1:57751, 8i8o>

    ::

        >>> server.quit()
        <Server: offline>

    '''

    ### CLASS VARIABLES ###

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
        '_default_group',
        '_ip_address',
        '_is_running',
        '_node_id_allocator',
        '_nodes',
        '_osc_controller',
        '_osc_dispatcher',
        '_port',
        '_response_manager',
        '_root_node',
        '_server_options',
        '_server_process',
        '_server_status',
        '_status_watcher',
        '_sync_id',
        '_synthdefs',
        )

    _default_server = None

    _servers = {}

    ### CONSTRUCTOR ###

    def __new__(cls, ip_address='127.0.0.1', port=57751):
        key = (ip_address, port)
        if key not in cls._servers:
            instance = object.__new__(cls)
            instance.__init__(
                ip_address=ip_address,
                port=port,
                )
            cls._servers[key] = instance
        return cls._servers[key]

    ### INITIALIZER ###

    def __init__(self, ip_address='127.0.0.1', port=57751):
        from supriya.tools import osctools
        from supriya.tools import responsetools

        if hasattr(self, 'is_running') and self.is_running:
            return

        ### NET ADDRESS ###

        self._ip_address = ip_address
        self._port = port

        ### OSC MESSAGING ###

        self._osc_dispatcher = osctools.OscDispatcher()
        self._osc_controller = osctools.OscController(server=self)
        self._response_manager = responsetools.ResponseManager()
        for callback in (
            responsetools.BufferResponseCallback(self),
            responsetools.ControlBusResponseCallback(self),
            responsetools.NodeResponseCallback(self),
            responsetools.SynthDefResponseCallback(self),
            ):
            self.register_osc_callback(callback)

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
        self._server_options = None
        self._server_process = None
        self._server_status = None
        self._status_watcher = None

        ### PROXIES ###

        self._audio_input_bus_group = None
        self._audio_output_bus_group = None
        self._default_group = None
        self._root_node = None

        ### PROXY MAPPINGS ###

        self._audio_buses = {}
        self._control_buses = {}
        self._control_bus_proxies = {}
        self._buffers = {}
        self._buffer_proxies = {}
        self._nodes = {}
        self._synthdefs = {}

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
        elif isinstance(expr, synthdeftools.StaticSynthDef):
            name = expr.actual_name
            if name in self._synthdefs and self._synthdefs[name] == expr:
                return True
        return False

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
                rate=synthdeftools.Rate.CONTROL,
                server=self,
                )
            self._control_bus_proxies[bus_id] = control_bus_proxy
        return control_bus_proxy

    def _setup(self):
        self._setup_allocators(self.server_options)
        self._setup_proxies()
        self._setup_notifications()
        self._setup_status_watcher()

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
        from supriya.tools import servertools
        notify_message = servertools.CommandManager.make_notify_message(1)
        with servertools.WaitForServer(
            address_pattern='/done',
            argument_template=('/notify', 0),
            server=self,
            ):
            self.send_message(notify_message)

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
        self._server_status = None
        self._status_watcher = servertools.StatusWatcher(self)
        self._status_watcher.start()

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
        self._control_bus_proxies = None
        self._buffer_proxies = None
        self._default_group = None
        self._root_node = None
        self._audio_input_bus_group = None
        self._audio_output_bus_group = None

    def _teardown_status_watcher(self):
        self._status_watcher.active = False
        self._status_watcher = None
        self._server_status = None

    ### PUBLIC METHODS ###

    def boot(
        self,
        server_options=None,
        ):
        from supriya.tools import servertools
        if self.is_running:
            return
        server_options = server_options or servertools.ServerOptions()
        options_string = server_options.as_options_string(self.port)
        command = 'scsynth {}'.format(options_string)
        server_process = pexpect.spawn(command)
        time.sleep(0.1)
        error = 'Exception in World_OpenUDP: bind: Address already in use'
        success = 'SuperCollider 3 server ready.'
        string = server_process.read_nonblocking(timeout=1.0)
        if 2 < sys.version_info[0]:
            string = str(string, 'utf-8')
        while True:
            try:
                char = server_process.read_nonblocking(timeout=1.0)
                if 2 < sys.version_info[0]:
                    char = str(char, 'utf-8')
                string += char
            except (pexpect.TIMEOUT, pexpect.EOF):
                break
        if error in string:
            raise Exception(error)
        assert success in string, string

        self._is_running = True
        self._server_options = server_options
        self._server_process = server_process
        self._setup()
        self.sync()
        return self

    @staticmethod
    def get_default_server():
        if Server._default_server is None:
            Server._default_server = Server()
        return Server._default_server

    def query_local_nodes(self, include_controls=False):
        r'''Queries all node proxies in Python.

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
            >>> builder = synthdeftools.SynthDefBuilder(
            ...     amplitude=0.0,
            ...     frequency=440.0,
            ...     )
            >>> sin_osc = ugentools.SinOsc.ar(
            ...     frequency=builder['frequency'],
            ...     )
            >>> sin_osc *= builder['amplitude']
            >>> out = ugentools.Out.ar(
            ...     bus=(0, 1),
            ...     source=sin_osc,
            ...     )
            >>> builder.add_ugen(out)
            >>> synthdef = builder.build()
            >>> synthdef.allocate()
            >>> server.sync()
            <Server: udp://127.0.0.1:57751, 8i8o>

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
                        1003 f1c3ea5063065be20688f82b415c1108
                            amplitude: 0.0, frequency: 440.0
                    1000 group
                        1002 group

        ::

            >>> server.quit()
            <Server: offline>

        Returns server query-tree group response.
        '''
        from supriya.tools import responsetools
        query_tree_group = responsetools.QueryTreeGroup.from_group(
            self.root_node,
            include_controls=include_controls,
            )
        return query_tree_group

    def query_remote_nodes(self, include_controls=False):
        r'''Queries all nodes on scsynth.

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
            >>> builder = synthdeftools.SynthDefBuilder(
            ...     amplitude=0.0,
            ...     frequency=440.0,
            ...     )
            >>> sin_osc = ugentools.SinOsc.ar(
            ...     frequency=builder['frequency'],
            ...     )
            >>> sin_osc *= builder['amplitude']
            >>> out = ugentools.Out.ar(
            ...     bus=(0, 1),
            ...     source=sin_osc,
            ...     )
            >>> builder.add_ugen(out)
            >>> synthdef = builder.build()
            >>> synthdef.allocate()
            >>> server.sync()
            <Server: udp://127.0.0.1:57751, 8i8o>

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
                        1003 f1c3ea5063065be20688f82b415c1108
                    1000 group
                        1002 group

        ::

            >>> server.quit()
            <Server: offline>

        Returns server query-tree group response.
        '''
        from supriya.tools import servertools
        wait = servertools.WaitForServer(
            address_pattern='/g_queryTree.reply',
            server=self,
            )
        message = servertools.CommandManager.make_group_query_tree_message(
            node_id=0,
            include_controls=include_controls,
            )
        with wait:
            self.send_message(message)
        reply = wait.received_message
        response = self._response_manager(reply)
        return response

    def quit(self):
        from supriya.tools import servertools
        if not self.is_running:
            return
        wait = servertools.WaitForServer(
            address_pattern='/(done|fail)',
            argument_template=('/quit',),
            server=self,
            )
        with wait:
            self.send_message('/quit')
        self._is_running = False
        if not self._server_process.terminate():
            self._server_process.wait()
        #self._server_process.send_signal(signal.SIGINT)
        #self._server_process.kill()
        self._teardown()
        return self

    def register_osc_callback(self, osc_callback):
        self._osc_dispatcher.register_osc_callback(osc_callback)

    def send_message(self, message):
        #from supriya.tools import osctools
        if not message or not self.is_running:
            return
        #if isinstance(message, osctools.OscMessage) and message.address != 2:
        #    print('SEND:', message)
        self._osc_controller.send(message)

    def sync(self, sync_id=None):
        from supriya.tools import servertools
        if not self.is_running:
            return
        if sync_id is None:
            sync_id = self._sync_id
            self._sync_id += 1
        else:
            sync_id = int(sync_id)
        message = servertools.CommandManager.make_sync_message(sync_id)
        wait = servertools.WaitForServer(
            address_pattern='/synced',
            argument_template=(sync_id,),
            server=self,
            )
        with wait:
            self.send_message(message)
        return self

    def unregister_osc_callback(self, osc_callback):
        self._osc_dispatcher.unregister_osc_callback(osc_callback)

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
    def default_group(self):
        return self._default_group

    @property
    def ip_address(self):
        return self._ip_address

    @property
    def is_running(self):
        return self._is_running

    @property
    def node_id_allocator(self):
        return self._node_id_allocator

    @property
    def port(self):
        return self._port

    @property
    def response_manager(self):
        return self._response_manager

    @property
    def root_node(self):
        return self._root_node

    @property
    def server_options(self):
        return self._server_options

    @property
    def server_status(self):
        return self._server_status
