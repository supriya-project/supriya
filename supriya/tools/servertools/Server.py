# -*- encoding: utf-8 -*-
from __future__ import print_function
import signal
import subprocess
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
        RECV: OscMessage('/done', '/quit')
        <Server: offline>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_audio_bus_allocator',
        '_audio_busses',
        '_audio_input_bus',
        '_audio_output_bus',
        '_buffer_allocator',
        '_buffers',
        '_control_bus_allocator',
        '_control_busses',
        '_default_group',
        '_ip_address',
        '_is_running',
        '_node_id_allocator',
        '_nodes',
        '_osc_controller',
        '_port',
        '_root_node',
        '_server_options',
        '_server_process',
        '_server_status',
        '_status_watcher',
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
        if hasattr(self, 'is_running') and self.is_running:
            return
        self._audio_bus_allocator = None
        self._audio_busses = None
        self._audio_input_bus = None
        self._audio_output_bus = None
        self._buffer_allocator = None
        self._buffers = None
        self._control_bus_allocator = None
        self._control_busses = None
        self._default_group = None
        self._ip_address = ip_address
        self._is_running = False
        self._node_id_allocator = None
        self._nodes = None
        self._osc_controller = None
        self._port = port
        self._root_node = None
        self._server_options = None
        self._server_process = None
        self._server_status = None
        self._status_watcher = None
        self._synthdefs = None

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
            if name in self._synthdefs and self._synthdefs[name] is expr:
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

    def _register_buffer(self, buffer_):
        from supriya.tools import servertools
        assert isinstance(buffer_, servertools.Buffer)
        assert buffer_.server is None

    def _register_control_bus(self, control_bus):
        from supriya.tools import servertools
        assert isinstance(control_bus, servertools.ControlBus)
        assert control_bus.server is None

    def _register_node(self, node):
        from supriya.tools import servertools
        assert isinstance(node, servertools.Node)
        assert node.server is None

    def _setup_server_state(self):
        from supriya.tools import servertools
        options = self.server_options
        self._audio_bus_allocator = servertools.BlockAllocator(
            heap_maximum=options.audio_bus_channel_count,
            heap_minimum=options.first_private_bus_id,
            )
        self._audio_input_bus = servertools.AudioInputBus(self)
        self._audio_output_bus = servertools.AudioOutputBus(self)
        self._buffer_allocator = servertools.BlockAllocator(
            heap_maximum=options.buffer_count,
            )
        self._control_bus_allocator = servertools.BlockAllocator(
            heap_maximum=options.control_bus_channel_count,
            )
        self._node_id_allocator = servertools.NodeIdAllocator(
            initial_node_id=options.initial_node_id,
            )
        self._audio_busses = {}
        self._buffers = {}
        self._control_busses = {}
        self._nodes = {}
        self._synthdefs = {}
        self._root_node = servertools.RootNode(server=self)
        self._default_group = servertools.Group()
        self._default_group._node_id = 1
        self._default_group._parent = self._root_node
        self._default_group._server = self
        self._nodes[0] = self._root_node
        self._nodes[1] = self._default_group
        self._root_node._children.append(self._default_group)
        self.send_message(('/g_new', 1, 0, 0))
        self._server_status = None

    def _teardown_server_state(self):
        self._audio_bus_allocator = None
        self._audio_input_bus = None
        self._audio_output_bus = None
        self._buffer_allocator = None
        self._control_bus_allocator = None
        self._node_id_allocator = None
        for x in tuple(self._audio_busses.values()):
            x.free()
        for x in tuple(self._buffers.values()):
            x.free()
        for x in tuple(self._control_busses.values()):
            x.free()
        for x in tuple(self._nodes.values()):
            x.free()
        self._default_group = None
        self._root_node = None
        self._server_status = None

    def _unregister_audio_bus(self, audio_bus):
        from supriya.tools import servertools
        assert isinstance(audio_bus, servertools.AudioBus)
        if audio_bus.server is None:
            return
        elif audio_bus.server is not self:
            raise ValueError

    def _unregister_buffer(self, buffer_):
        from supriya.tools import servertools
        assert isinstance(buffer_, servertools.Buffer)
        if buffer_.server is None:
            return
        elif buffer_.server is not self:
            raise ValueError

    def _unregister_control_bus(self, control_bus):
        from supriya.tools import servertools
        assert isinstance(control_bus, servertools.ControlBus)
        if control_bus.server is None:
            return
        elif control_bus.server is not self:
            raise ValueError

    def _unregister_node(self, node):
        from supriya.tools import servertools
        assert isinstance(node, servertools.Node)
        if node.server is None:
            return
        elif node.server is not self:
            raise ValueError

    ### PUBLIC METHODS ###

    def boot(
        self,
        server_options=None,
        ):
        from supriya.tools import osctools
        from supriya.tools import servertools
        from supriya.tools import systemtools
        if self.is_running:
            return
        server_options = server_options or servertools.ServerOptions()
        options_string = server_options.as_options_string(self.port)
        command = 'scsynth {}'.format(options_string)
        server_process = subprocess.Popen(
            command.split(),
            bufsize=0,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            )

        error = b'Exception in World_OpenUDP: bind: Address already in use'
        success = b'SuperCollider 3 server ready.'
        reader = systemtools.NonBlockingStreamReader(server_process.stdout)
        with reader:
            while True:
                time.sleep(0.01)
                line = reader.readline(timeout=0.01)
                if line is None:
                    continue
                elif error in line:
                    raise Exception(error)
                elif success in line:
                    break

        self._is_running = True
        self._osc_controller = osctools.OscController(
            server_ip_address=self.ip_address,
            server_port=self.port,
            )
        self._server_options = server_options
        self._server_process = server_process
        self._setup_server_state()
        return self

    @staticmethod
    def get_default_server():
        if Server._default_server is None:
            Server._default_server = Server()
        return Server._default_server

    def query_local_state(self):
        pass

    def query_server_state(self):
        pass

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
        self._server_process.send_signal(signal.SIGINT)
        self._server_process.kill()
        self._teardown_server_state()
        return self

    def register_osc_callback(self, osc_callback):
        self._osc_controller.register_callback(osc_callback)

    def send_message(self, message):
        if not message or not self.is_running:
            return
        self._osc_controller.send(message)

    def unregister_osc_callback(self, osc_callback):
        self._osc_controller.unregister_callback(osc_callback)

    ### PUBLIC PROPERTIES ###

    @property
    def audio_bus_allocator(self):
        return self._audio_bus_allocator

    @property
    def audio_input_bus(self):
        return self._audio_input_bus

    @property
    def audio_output_bus(self):
        return self._audio_output_bus

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
    def root_node(self):
        return self._root_node

    @property
    def server_options(self):
        return self._server_options