import signal
import subprocess
import time


class Server(object):
    r'''An scsynth server proxy.

    ::

        >>> from supriya import servertools
        >>> server = servertools.Server.get_default_server()
        >>> server.boot()
        <supriya.tools.servertools.Server.Server object at 0x...>

    ::

        >>> server.quit()
        RECV: OscMessage('/done', '/quit')

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_ip_address',
        '_port',
        '_osc_controller',
        '_server_session',
        )

    _default_server = None

    ### INITIALIZER ###

    def __init__(self, ip_address='127.0.0.1', port=57751):
        self._ip_address = ip_address
        self._port = port
        self._osc_controller = None
        self._server_session = None

    ### SPECIAL METHODS ###

    def __del__(self):
        self.quit()

    ### PUBLIC METHODS ###

    def boot(
        self,
        server_options=None,
        ):
        from supriya.tools import servertools
        from supriya.tools import osclib
        if self.server_session is not None:
            return
        self._osc_controller = osclib.OscController(
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
        server_session = servertools.ServerSession(
            server_options=server_options,
            server_process=server_process,
            )
        time.sleep(0.25)
        self.send_message(("/g_new", 1, 0, 0))
        self._server_session = server_session
        return self

    def dump_osc(self, expr):
        self.send_message(r'/dumpOSC', expr)

    @staticmethod
    def get_default_server():
        if Server._default_server is None:
            Server._default_server = Server()
        return Server._default_server

    def notify(self, expr):
        self.send_message(r'/notify', expr)

    def quit(self):
        from supriya.tools import servertools
        if self._server_session is None:
            return
        with servertools.WaitForServer('/(done|fail)', ['/quit']):
            self.send_message(r'/quit')
        self._server_session.server_process.send_signal(signal.SIGINT)
        self._server_session.server_process.kill()
        self._server_session.free()
        self._server_session = None

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
    def server_session(self):
        return self._server_session
