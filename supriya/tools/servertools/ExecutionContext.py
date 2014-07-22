class ExecutionContext(object):

    __slots__ = (
        '_messages',
        '_server',
        '_timestamp',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        server=None,
        sync=False,
        timestamp=None,
        ):
        from supriya.tools import servertools
        server = server or servertools.Server()
        assert isinstance(server, servertools.Server)
        self._server = server
        self._timestamp = timestamp

    ### SPECIAL METHODS ###

    def __enter__(self):
        self._message = []
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        from supriya.tools import osctools
        messages = []
        prototype = (osctools.OscMessage, osctools.OscBundle)
        for message in self.messages:
            if not isinstance(message, prototype):
                message = message.as_osc_message()
            messages.append(message)
        osc_bundle = osctools.OscBundle(
            timestamp=self.timestamp,
            contents=messages,
            )
        self.server.send_message(osc_bundle)
        if self.sync:
            self.server.sync()

    ### PUBLIC METHODS ###

    def send_message(self, request):
        from supriya.tools import osctools
        from supriya.tools import requesttools
        prototype = (
            osctools.OscMessage,
            osctools.OscBundle,
            requesttools.Request,
            )
        assert isinstance(request, prototype)
        self._requests.append(request)

    def sync(self):
        self._sync = True