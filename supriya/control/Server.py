import signal
import subprocess
import time


class Server(object):
    r'''An scsynth server proxy.

    ::

        >>> from supriya import control
        >>> server = control.Server()
        >>> server.boot()
        >>> server.quit()
        ['/done', '/quit']

    The server class is a singleton:

    ::

        >>> server_one = control.Server()
        >>> server_two = control.Server()
        >>> server_one is server_two
        True

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_osc_controller',
        '_scsynth_process',
        )

    _instance = None

    ### CONSTRUCTOR ###

    def __init__(self):
        self._osc_controller = None
        self._scsynth_process = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Server, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    ### SPECIAL METHODS ###

    def __del__(self):
        self.quit()

    def _send_message(self, message):
        self._osc_controller.send(message)

    ### PUBLIC METHODS ###

    def boot(
        self,
        inputs=2,
        outputs=2,
        samplerate=48000,
        ):
        import supriya
        server_port = 57751
        self._osc_controller = supriya.control.OSCController(
            server_ip_address='127.0.0.1',
            server_port=server_port,
            )
        command = 'scsynth -u {port} -S {samplerate} -i {inputs} -o {outputs}'
        command = command.format(
            inputs=inputs,
            outputs=outputs,
            port=server_port,
            samplerate=samplerate,
            )
        self._scsynth_process = subprocess.Popen(
            command.split(),
            )
        time.sleep(0.5)

    def dump_osc(self, expr):
        self._send_message(r'/dumpOSC', expr)

    def notify(self, expr):
        self._send_message(r'/notify', expr)

    def quit(self):
        self._send_message(r'/quit')
        self._osc_controller.receive((r'/done', r'/fail'))
        self._osc_controller.__del__()
        self._osc_controller = None
        self._scsynth_process.send_signal(signal.SIGINT)
        self._scsynth_process.kill()

    def send_command(self, arguments):
        if self._osc_controller is not None:
            self._send_message(r'/cmd', arguments)

    def sync(self, reply_int):
        self._send_message(r'/sync', reply_int)

    def update_status(self):
        self._send_message(r'/status')
