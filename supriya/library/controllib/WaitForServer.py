import time


class WaitForServer(object):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_called_back',
        '_message',
        )

    ### INITIALIZER ###

    def __init__(self, message=None):
        self._called_back = False
        if isinstance(message, (int, str)):
            message = tuple(message,)
        else:
            message = tuple(message)
        self._message = message

    ### SPECIAL METHODS ###

    def __call__(self, message):
        if message == self.message:
            self._called_back = True

    def __enter__(self):
        from supriya import controllib
        server = controllib.Server()
        server._osc_controller._listener.register_callback(
            self.message_key,
            self.__call__,
            )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        from supriya import controllib
        server = controllib.Server()
        while not self.called_back:
            time.sleep(0.05)
        server._osc_controller._listener.unregister_callback(
            self.message_key,
            self.__call__,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def called_back(self):
        return self._called_back

    @property
    def message(self):
        return self._message

    @property
    def message_key(self):
        if self.message is None:
            return None
        return self.message[0]
