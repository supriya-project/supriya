# -*- encoding: utf-8 -*-
from __future__ import print_function
import socket
import sys
import threading
import traceback
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class OscListener(SupriyaObject, threading.Thread):
    r'''An OSC listener
    '''

    ### INITIALIZER ###

    def __init__(
        self,
        client=None,
        debug=False,
        timeout=1,
        ):
        threading.Thread.__init__(self)
        self.debug = bool(debug)
        self.client = client
        self.setDaemon(True)
        self.running = False
        self.timeout = int(timeout)

    ### PUBLIC METHODS ###

    def get_message(self):
        from supriya.tools import osctools
        try:
            data, address = self.client.socket_instance.recvfrom(2**13)
            if data:
                message = osctools.OscMessage.from_datagram(data)
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
                if self.debug:
                    if message.address != '/status.reply':
                        print('RECV', message)
                osc_dispatcher(message)
                response_dispatcher(message)
        except:
            sys.stderr.write('Exception in listener thread:\n')
            traceback.print_exc()