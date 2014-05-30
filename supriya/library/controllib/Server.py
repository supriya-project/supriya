import signal
import subprocess
import time


class Server(object):
    r'''An scsynth server proxy.

    ::

        >>> from supriya import controllib
        >>> server = controllib.Server()
        >>> server.boot()
        <supriya.library.controllib.Server.Server object at 0x...>

    ::

        >>> server.quit()
        OscMessage('/done', u'/quit')

    The server class is a singleton:

    ::

        >>> server_one = controllib.Server()
        >>> server_two = controllib.Server()
        >>> server_one is server_two
        True

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_audio_bus_allocator',
        '_buffer_allocator',
        '_control_bus_allocator',
        '_is_running',
        '_node_id_allocator',
        '_options',
        '_osc_controller',
        '_scsynth_process',
        )

    _instance = None

    ### CONSTRUCTOR ###

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            instance = super(Server, cls).__new__(
                cls, *args, **kwargs)
            instance._audio_bus_allocator = None
            instance._buffer_allocator = None
            instance._control_bus_allocator = None
            instance._is_running = None
            instance._node_id_allocator = None
            instance._options = None
            instance._osc_controller = None
            instance._scsynth_process = None
            cls._instance = instance
        return cls._instance

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __del__(self):
        self.quit()

    ### PRIVATE METHODS ###

    def _create_new_allocators(self):
        from supriya.library import controllib
        self._audio_bus_allocator = controllib.ContiguousBlockAllocator(
            size=self.options.numAudioBusChannels,
            position=self.options.firstPrivateBus,
            )
        self._buffer_allocator = controllib.ContiguousBlockAllocator(
            size=self.options.numBuffers,
            )
        self._control_bus_allocator = controllib.ContiguousBlockAllocator(
            size=self.options.numControlBusChannels,
            )
        self._node_id_allocator = controllib.NodeIDAllocator(
            initial_node_id=self.options.initialNodeID,
            )

    ### PUBLIC METHODS ###

    def boot(
        self,
        options=None,
        server_port=57751
        ):
        from supriya.library import controllib
        from supriya.library import osclib
        if self.is_running:
            return
        options = options or controllib.ServerOptions()
        assert isinstance(options, controllib.ServerOptions)
        self._options = options
        self._create_new_allocators()
        self._osc_controller = osclib.OscController(
            server_ip_address='127.0.0.1',
            server_port=server_port,
            )
        options_string = options.as_options_string(server_port)
        command = 'scsynth {}'.format(options_string)
        self._scsynth_process = subprocess.Popen(
            command.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            )
        time.sleep(0.5)
        self.send_message(("/g_new", 1, 0, 0))
        self._is_running = True
        return self

    def dump_osc(self, expr):
        self.send_message(r'/dumpOSC', expr)

    def notify(self, expr):
        self.send_message(r'/notify', expr)

    def quit(self):
        self.send_message(r'/quit')
        self._osc_controller.receive((r'/done', r'/fail'))
        self._osc_controller.__del__()
        self._osc_controller = None
        self._scsynth_process.send_signal(signal.SIGINT)
        self._scsynth_process.kill()
        self._create_new_allocators()
        self._is_running = False

    def send_command(self, arguments):
        if self._osc_controller is not None:
            self.send_message(r'/cmd', arguments)

    def send_message(self, message):
        from supriya.library import controllib
        assert self is controllib.Server()
        self._osc_controller.send(message)

    def sync(self, reply_int):
        self.send_message(r'/sync', reply_int)

    def update_status(self):
        self.send_message(r'/status')

    ### PUBLIC PROPERTIES ###

    @property
    def audio_bus_allocator(self):
        return self._audio_bus_allocator

    @property
    def buffer_allocator(self):
        return self._buffer_allocator

    @property
    def control_bus_allocator(self):
        return self._control_bus_allocator

    @property
    def default_group(self):
        from supriya.library import controllib
        group = controllib.Group(
            node_id=1,
            server=self,
            send_to_server=False,
            )
        return group

    @property
    def is_running(self):
        return self._is_running

    @property
    def node_id_allocator(self):
        return self._node_id_allocator

    @property
    def options(self):
        return self._options
