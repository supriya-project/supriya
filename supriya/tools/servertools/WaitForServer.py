import time


class WaitForServer(object):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_callback',
        '_called_back',
        '_server',
        '_timeout',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        address_pattern=None,
        argument_template=None,
        server=None,
        timeout=1.,
        ):
        from supriya import servertools
        from supriya import osctools
        self._called_back = False
        self._callback = osctools.OscCallback(
            address_pattern=address_pattern,
            argument_template=argument_template,
            is_one_shot=True,
            procedure=self.__call__,
            )
        server = server or servertools.Server.get_default_server()
        assert isinstance(server, servertools.Server), server
        self._server = server
        self._timeout = float(timeout)

    ### SPECIAL METHODS ###

    def __call__(self, message):
        self._called_back = True

    def __enter__(self):
        self.server._osc_controller.dispatcher.register_callback(self.callback)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        total_time = 0.
        sleep_time = 0.01
        while not self.called_back:
            if self.timeout <= total_time:
                raise Exception('Ran out of time.')
            total_time += sleep_time
            time.sleep(sleep_time)

    ### PUBLIC PROPERTIES ###

    @property
    def called_back(self):
        return self._called_back

    @property
    def callback(self):
        return self._callback

    @property
    def server(self):
        return self._server

    @property
    def timeout(self):
        return self._timeout
