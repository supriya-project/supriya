class ExecutionContext(object):

    __slots__ = (
        '_messages',
        '_server',
        '_sync',
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
        self._messages = []
        self._server = server
        self._sync = bool(sync)
        if timestamp is not None:
            timestamp = float(timestamp)
        self._timestamp = timestamp

    ### SPECIAL METHODS ###

    def __enter__(self):
        self._messages = []
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        from supriya.tools import osctools
        from supriya.tools import requesttools
        messages = []
        prototype = (osctools.OscMessage, osctools.OscBundle)
        for message in self._messages:
            if not isinstance(message, prototype):
                message = message.to_osc_message()
            messages.append(message)
        if self._sync:
            sync_id = self._server.next_sync_id
            sync_request = requesttools.SyncRequest(
                sync_id=sync_id,
                )
            message = sync_request.to_osc_message()
            messages.append(message)
        osc_bundle = osctools.OscBundle(
            timestamp=self._timestamp,
            contents=messages,
            )
        if self._sync:
            sync_request.communicate(
                message=osc_bundle,
                server=self._server,
                )
        else:
            self._server.send_message(osc_bundle)

    ### PUBLIC METHODS ###

    def send_message(self, message):
        from supriya.tools import osctools
        from supriya.tools import requesttools
        prototype = (
            osctools.OscMessage,
            osctools.OscBundle,
            requesttools.Request,
            )
        assert isinstance(message, prototype)
        self._messages.append(message)

    def sync(self, sync=True):
        self._sync = bool(sync)