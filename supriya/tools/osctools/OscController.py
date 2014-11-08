# -*- encoding: utf-8 -*-
from __future__ import print_function
try:
    import queue
except ImportError:
    import Queue as queue
import socket
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class OscController(SupriyaObject):
    '''An OSC controller.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_debug',
        '_incoming_message_queue',
        '_listener',
        '_server',
        '_socket_instance',
        '_timeout',
        )

    class CleanableQueue(queue.Queue):

        def __init__(self, maximum_length=0):
            queue.Queue.__init__(self)
            self._maximum_length = int(maximum_length)

        def clean(self):
            while not self.empty() and self.maximum_length < self.qsize():
                self.get()

        @property
        def maximum_length(self):
            return self._maximum_length

    ### INITIALIZER ###

    def __init__(
        self,
        debug=False,
        server=None,
        timeout=2,
        ):
        from supriya.tools import osctools
        self._debug = bool(debug)
        self._server = server
        assert 0 < int(timeout)
        self._timeout = int(timeout)
        self._socket_instance = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM,
            )
        self._socket_instance.settimeout(self.timeout)
        self._listener = osctools.OscListener(
            client=self,
            debug=self.debug,
            )
        self._listener.start()
        self._socket_instance.bind(('', 0))

    ### SPECIAL METHODS ###

    def __del__(self):
        self._listener.quit(wait=True)

    ### PUBLIC METHODS ###

    def send(self, message):
        from supriya.tools import osctools
        from supriya.tools import requesttools
        prototype = (str, tuple, osctools.OscMessage, osctools.OscBundle)
        assert isinstance(message, prototype)
        if isinstance(message, str):
            message = osctools.OscMessage(message)
        elif isinstance(message, tuple):
            assert len(message)
            message = osctools.OscMessage(
                message[0],
                *message[1:]
                )
        if self.debug:
            if not isinstance(message, osctools.OscMessage) or \
                message.address not in (
                    '/status',
                    requesttools.RequestId.STATUS
                    ):
                print('SEND', repr(message))
                #for line in str(message).splitlines():
                #    print('    ' + line)
        datagram = message.to_datagram()
        self.socket_instance.sendto(
            datagram,
            (self.server.ip_address, self.server.port),
            )

    ### PUBLIC PROPERTIES ###

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, expr):
        self._debug = bool(expr)
        self.listener.debug = self.debug

    @property
    def listener(self):
        return self._listener

    @property
    def server(self):
        return self._server

    @property
    def socket_instance(self):
        return self._socket_instance

    @property
    def timeout(self):
        return self._timeout