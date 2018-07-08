import socketserver
import threading
import time
from supriya.osc.OscBundle import OscBundle
from supriya.osc.OscMessage import OscMessage


class OscIO:

    class OscServer(socketserver.UDPServer):
        pass

    class OscHandler(socketserver.BaseRequestHandler):

        def handle(self):
            data = self.request[0]
            message = OscMessage.from_datagram(data)
            debug_osc = self.server.io_instance.debug_osc
            debug_udp = self.server.io_instance.debug_udp
            if debug_osc and message.address != '/status.reply':
                print('RECV', '{:0.6f}'.format(time.time()), message.to_list())
                if debug_udp:
                    for line in str(message).splitlines():
                        print('    ' + line)
            self.server.io_instance.osc_dispatcher(message)
            self.server.io_instance.response_dispatcher(message)

    def __init__(
        self,
        debug_osc=False,
        debug_udp=False,
        ip_address='127.0.0.1',
        port=57751,
        timeout=2,
        osc_dispatcher=None,
        response_dispatcher=None,
    ):
        self.debug_osc = bool(debug_osc)
        self.debug_udp = bool(debug_udp)
        self.ip_address = ip_address
        self.lock = threading.Lock()
        self.osc_dispatcher = osc_dispatcher
        self.server = None
        self.server_thread = None
        self.port = port
        self.response_dispatcher = response_dispatcher
        self.running = False
        self.timeout = timeout

    ### SPECIAL METHODS ###

    def __del__(self):
        self.quit()

    ### PUBLIC METHODS ###

    def boot(self, ip_address=None, port=None):
        with self.lock:
            if self.running:
                return
            if ip_address:
                self.ip_address = ip_address
            if port:
                self.port = port
            self.server = self.OscServer(
                (self.ip_address, self.port),
                self.OscHandler,
                bind_and_activate=False,
            )
            self.server.io_instance = self
            self.server_thread = threading.Thread(
                target=self.server.serve_forever,
            )
            self.server_thread.daemon = True
            self.server_thread.start()
            self.running = True

    def quit(self):
        with self.lock:
            if not self.running:
                return
            self.server.shutdown()
            self.server = None
            self.server_thread = None
            self.running = False

    def send(self, message):
        if not self.running:
            raise RuntimeError
        prototype = (str, tuple, OscBundle, OscMessage)
        if not isinstance(message, prototype):
            raise ValueError(message)
        if isinstance(message, str):
            message = OscMessage(message)
        elif isinstance(message, tuple):
            if not len(message):
                raise ValueError(message)
            message = OscMessage(message[0], *message[1:])
        if self.debug_osc:
            as_list = message.to_list()
            if as_list != [2]:
                print('SEND', '{:0.6f}'.format(time.time()), message.to_list())
                if self.debug_udp:
                    for line in str(message).splitlines():
                        print('    ' + line)
        datagram = message.to_datagram()
        self.server.socket.sendto(datagram, (self.ip_address, self.port))
