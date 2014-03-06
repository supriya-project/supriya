import signal
import subprocess


class Server(object):
    r'''An scsynth server proxy.
    '''

    ### CLASS VARIABLES ###

    _instance = None

    ### CONSTRUCTOR ###

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Server, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    ### SPECIAL METHODS ###

    def __del__(self):
        self.quit()

    ### PUBLIC METHODS ###    

    def boot(self):
        import supriya
        server_port = 57751
        self._osc_controller = supriya.osc.OSCController(
            server_ip_address='127.0.0.1',
            server_port=server_port,
            )
        command = 'scsynth -u {}'.format(server_port)
        self._scsynth_process = subprocess.Popen(
            command.split(),
            )

    def send(self, message):
        self._osc_controller.send(message)

    def quit(self):
        self._osc_controller.__del__()
        self._osc_controller = None
        self._scsynth_process.send_signal(signal.SIGINT)
        self._scsynth_process.kill()
