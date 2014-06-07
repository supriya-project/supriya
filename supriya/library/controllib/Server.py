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
        OscMessage('/done', '/quit')

    The server class is a singleton:

    ::

        >>> server_one = controllib.Server()
        >>> server_two = controllib.Server()
        >>> server_one is server_two
        True

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_osc_controller',
        '_server_session',
        )

    _instance = None

    ### CONSTRUCTOR ###

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            instance = super(Server, cls).__new__(
                cls, *args, **kwargs)
            instance._osc_controller = None
            instance._server_session = None
            cls._instance = instance
        return cls._instance

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __del__(self):
        self.quit()

    ### PUBLIC METHODS ###

    def boot(
        self,
        server_options=None,
        server_port=57751
        ):
        from supriya.library import controllib
        from supriya.library import osclib
        if self.server_session is not None:
            return
        self._osc_controller = osclib.OscController(
            server_ip_address='127.0.0.1',
            server_port=server_port,
            )
        server_options = server_options or controllib.ServerOptions()
        options_string = server_options.as_options_string(server_port)
        command = 'scsynth {}'.format(options_string)
        server_process = subprocess.Popen(
            command.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            )
        server_session = controllib.ServerSession(
            server_options=server_options,
            server_process=server_process,
            )
        time.sleep(0.25)
        self.send_message(("/g_new", 1, 0, 0))
        self._server_session = server_session
        return self

    def dump_osc(self, expr):
        self.send_message(r'/dumpOSC', expr)

    def notify(self, expr):
        self.send_message(r'/notify', expr)

    def quit(self):
        from supriya.library import controllib
        with controllib.WaitForServer(('/done', '/fail')):
            self.send_message(r'/quit')
        self._osc_controller.__del__()
        self._osc_controller = None
        self._server_session.server_process.send_signal(signal.SIGINT)
        self._server_session.server_process.kill()
        self._server_session.free()

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
    def server_session(self):
        return self._server_session
