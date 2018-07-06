import socket
import sys
import threading
import time
import traceback
from supriya.system.SupriyaObject import SupriyaObject


class OscListener(SupriyaObject, threading.Thread):
    """
    An OSC listener
    """

    ### INITIALIZER ###

    def __init__(
        self,
        client=None,
        debug_osc=False,
        debug_udp=False,
        timeout=1,
    ):
        threading.Thread.__init__(self)
        self.debug_osc = bool(debug_osc)
        self.debug_udp = bool(debug_udp)
        self.client = client
        self.setDaemon(True)
        self.running = False
        self.timeout = int(timeout)

    ### SPECIAL METHODS ###

    def __del__(self):
        self.quit()

    ### PUBLIC METHODS ###

    def get_message(self):
        import supriya.osc
        try:
            data, address = self.client.socket_instance.recvfrom(2 ** 13)
            if data:
                message = supriya.osc.OscMessage.from_datagram(data)
                return message
            return None
        except socket.timeout:
            return None

    def quit(self, wait=False):
        self.running = False
        if wait:
            self.join(2)

    def run(self):
        self.running = True
        self.client.socket_instance.settimeout(0.5)
        osc_dispatcher = self.client.server._osc_dispatcher
        response_dispatcher = self.client.server._response_dispatcher
        try:
            while self.running:
                message = self.get_message()
                if message is None:
                    continue
                if self.debug_osc:
                    if message.address != '/status.reply':
                        print('RECV', '{:0.6f}'.format(time.time()), message.to_list())
                        if self.debug_udp:
                            for line in str(message).splitlines():
                                print('    ' + line)
                osc_dispatcher(message)
                response_dispatcher(message)
        except Exception:
            sys.stderr.write('Exception in listener thread:\n')
            traceback.print_exc()
