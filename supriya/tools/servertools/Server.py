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

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_ip_address',
        '_port',
        '_osc_controller',
        '_session',
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
        self._ip_address = ip_address
        self._port = port
        self._osc_controller = None
        self._session = None

    ### SPECIAL METHODS ###

    def __repr__(self):
        if not self.session:
            return '<Server: offline>'
        string = '<Server: {protocol}://{ip}:{port}, '
        string += '{inputs}i{outputs}o>'
        return string.format(
            protocol=self.session.server_options.protocol,
            ip=self.ip_address,
            port=self.port,
            inputs=self.session.server_options.input_bus_channel_count,
            outputs=self.session.server_options.output_bus_channel_count,
            )

    ### PUBLIC METHODS ###

    def boot(
        self,
        server_options=None,
        ):
        from supriya.tools import servertools
        from supriya.tools import osctools
        if self.session is not None:
            return
        self._osc_controller = osctools.OscController(
            server_ip_address=self.ip_address,
            server_port=self.port,
            )
        server_options = server_options or servertools.ServerOptions()
        options_string = server_options.as_options_string(self.port)
        command = 'scsynth {}'.format(options_string)
        server_process = subprocess.Popen(
            command.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            )
        session = servertools.Session(
            server_options=server_options,
            server_process=server_process,
            )
        time.sleep(0.25)
        self.send_message(("/g_new", 1, 0, 0))
        self._session = session
        return self

    def dump_osc(self, expr):
        self.send_message(r'/dumpOSC', expr)

    @staticmethod
    def get_default_server():
        if Server._default_server is None:
            Server._default_server = Server(
                ip_address='127.0.0.1',
                port=57751,
                )
        return Server._default_server

    def notify(self, expr):
        self.send_message(r'/notify', expr)

    def quit(self):
        from supriya.tools import servertools
        if self._session is None:
            return
        with servertools.WaitForServer('/(done|fail)', ['/quit']):
            self.send_message(r'/quit')
        self._session.server_process.send_signal(signal.SIGINT)
        self._session.server_process.kill()
        self._session.free()
        self._session = None

    def send_command(self, arguments):
        if self._osc_controller is not None:
            self.send_message(r'/cmd', arguments)

    def send_message(self, message):
        self._osc_controller.send(message)

    def sync(self, reply_int):
        self.send_message(r'/sync', reply_int)

    def update_status(self):
        self.send_message(r'/status')

    ### PUBLIC PROPERTIES ###

    @property
    def ip_address(self):
        return self._ip_address

    @property
    def port(self):
        return self._port

    @property
    def session(self):
        return self._session
