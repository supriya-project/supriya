import Queue
import re
import socket
import time


class OSCController(object):
    '''An OSC controller.

    ::

        >>> import supriya
        >>> controller = supriya.controllib.OSCController(\
        ...     server_ip_address='127.0.0.1',
        ...     server_port=57751,
        ...     )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_debug_messages',
        '_incoming_message_queue',
        '_listener',
        '_maximum_queue_length',
        '_server_ip_address',
        '_server_port',
        '_socket',
        '_timeout',
        '_verbose',
        )

    class CleanableQueue(Queue.Queue):

        def __init__(self, maximum_length=0):
            Queue.Queue.__init__(self)
            self._maximum_length = int(maximum_length)

        def clean(self):
            while not self.empty() and self.maximum_length < self.qsize():
                self.get()

        @property
        def maximum_length(self):
            return self._maximum_length

    ### INITIALIZER ###

    def __init__(self,
        maximum_queue_length=3,
        server_ip_address='127.0.0.1',
        server_port=57751,
        debug_messages=False,
        timeout=2,
        verbose=True,
        ):
        import supriya
        assert 0 < int(maximum_queue_length)
        self._maximum_queue_length = int(maximum_queue_length)
        self._server_ip_address = server_ip_address
        self._server_port = int(server_port)
        self._debug_messages = bool(debug_messages)
        assert 0 < int(timeout)
        self._timeout = int(timeout)
        self._verbose = bool(verbose)
        self._socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM,
            )
        self._socket.settimeout(self.timeout)
        self._incoming_message_queue = self.CleanableQueue(
            maximum_length=self._maximum_queue_length,
            )
        self._listener = supriya.controllib.OSCListener(self.socket)
        self._listener.register_callback(
            None,
            self._incoming_message_queue.put,
            )
        if self._verbose:
            self._listener.register_callback(
                None,
                self._print_message,
                )
        self._listener.start()
        # TODO: We need to understand how socket binding actually works.
        #       It appears we can simply bind to any port, and we'll get
        #       information back from scsynth.  This seems too much like magic.
        self._socket.bind(('', 0))

    ### SPECIAL METHODS ###

    def __del__(self):
        self._listener.quit(wait=True)

    ### PRIVATE METHODS ###

    def _print_message(self, message):
        print message

    ### PUBLIC PROPERTIES ###

    @property
    def debug_messages(self):
        return self._debug_messages

    @property
    def incoming_message_queue(self):
        return self._incoming_message_queue

    @property
    def listener(self):
        return self._listener

    @property
    def maximum_queue_length(self):
        return self._maximum_queue_length

    @property
    def server_ip_address(self):
        return self._server_ip_address

    @property
    def server_port(self):
        return self._server_port

    @property
    def socket(self):
        return self._socket

    @property
    def timeout(self):
        return self._timeout

    @property
    def verbose(self):
        return self._verbose

    ### PUBLIC METHODS ###

    def receive(self, keys=None):
        import supriya
        assert isinstance(keys, (type(None), tuple))
        while True:
            try:
                message = self.incoming_message_queue.get(
                    timeout=self.timeout,
                    )
                if self.debug_messages:
                    print supriya.controllib.OSCMessage.decode(message)
                if not keys or message[0] in keys:
                    return message
            except Queue.Empty:
                raise IOError('Timeout waiting for reply from SC server.')

    def send(self, message):
        import supriya
        prototype = (str, tuple, supriya.controllib.OSCMessage)
        assert isinstance(message, prototype)
        if isinstance(message, str):
            message = supriya.controllib.OSCMessage(address=message)
        elif isinstance(message, tuple):
            assert len(message)
            message = supriya.controllib.OSCMessage(
                address=message[0],
                expr=message[1:],
                )
        if self.debug_messages:
            print supriya.controllib.OSCMessage.decode(message)
        self.socket.sendto(
            message.encode(),
            (self.server_ip_address, self.server_port),
            )
