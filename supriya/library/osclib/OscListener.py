# -*- encoding: utf-8 -*-
from __future__ import print_function
import socket
import sys
import threading
import traceback


class OscListener(threading.Thread):
    r'''An OSC listener
    '''

    ### INITIALIZER ###

    def __init__(self, client, timeout=1):
        threading.Thread.__init__(self)
        self.client = client
        self.setDaemon(True)
        self.running = False
        self.timeout = int(timeout)

    ### PUBLIC METHODS ###

    def get_message(self):
        from supriya.library import osclib
        try:
            data, address = self.client.socket_instance.recvfrom(2**13)
            if data:
                message = osclib.OscMessage.from_datagram(data)
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
        try:
            while self.running:
                message = self.get_message()
                if message is None:
                    continue
                self.client.dispatcher(message)
        except:
            sys.stderr.write('Exception in listener thread:\n')
            traceback.print_exc()
