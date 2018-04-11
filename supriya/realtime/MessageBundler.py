from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class MessageBundler(SupriyaObject):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Main Classes'

    __slots__ = (
        '_messages',
        '_result',
        '_send_to_server',
        '_server',
        '_sync',
        '_synchronizing_request',
        '_timestamp',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        send_to_server=True,
        server=None,
        sync=False,
        timestamp=None,
        ):
        import supriya.realtime
        self._result = None
        self._send_to_server = bool(send_to_server)
        server = server or supriya.realtime.Server()
        self._server = server
        self._messages = []
        self._sync = bool(sync)
        self._synchronizing_request = None
        if timestamp is not None:
            timestamp = float(timestamp)
        self._timestamp = timestamp

    ### SPECIAL METHODS ###

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.send_messages()

    ### PUBLIC METHODS ###

    def add_message(self, message):
        import supriya.osc
        from supriya.tools import requesttools
        prototype = (
            supriya.osc.OscMessage,
            supriya.osc.OscBundle,
            requesttools.Request,
            )
        assert isinstance(message, prototype)
        self._messages.append(message)

    def add_messages(self, messages):
        for message in messages:
            self.add_message(message)

    def add_synchronizing_request(self, request):
        from supriya.tools import requesttools
        assert isinstance(request, (type(None), requesttools.Request))
        self._synchronizing_request = request

    def send_messages(self):
        import supriya.osc
        from supriya.tools import requesttools
        messages = []
        prototype = (supriya.osc.OscMessage, supriya.osc.OscBundle)
        for message in self._messages:
            if not isinstance(message, prototype):
                message = message.to_osc_message()
            messages.append(message)
        if self._sync and not self._synchronizing_request:
            sync_id = self._server.next_sync_id
            sync_request = requesttools.SyncRequest(
                sync_id=sync_id,
                )
            message = sync_request.to_osc_message()
            messages.append(message)
        if 1 < len(messages) or self._timestamp is not None:
            self._result = supriya.osc.OscBundle(
                timestamp=self._timestamp,
                contents=messages,
                )
        else:
            self._result = messages[0]
        if not self._send_to_server:
            return
        if self._sync:
            sync_request = self._synchronizing_request or sync_request
            sync_request.communicate(
                message=self.result,
                server=self._server,
                )
        else:
            self._server.send_message(self._result)

    ### PUBLIC PROPERTIES ###

    @property
    def result(self):
        return self._result
