import time


class WaitForServer(object):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_callbacks',
        '_called_back',
        '_message',
        )

    ### INITIALIZER ###

    def __init__(self, message=None):
        from supriya import osclib
        self._called_back = False
        if isinstance(message, (int, str)):
            message = tuple(message,)
        else:
            message = tuple(message)
        self._message = message
        self._callbacks = [
            osclib.OscCallback(x, self.__call__)
            for x in message
            ]

    ### SPECIAL METHODS ###

    def __call__(self, message):
        if message.address in self.message:
            self._called_back = True

    def __enter__(self):
        from supriya import controllib
        server = controllib.Server()
        for callback in self._callbacks:
            server._osc_controller.dispatcher.register_callback(callback)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        from supriya import controllib
        server = controllib.Server()
        while not self.called_back:
            time.sleep(0.05)
        for callback in self._callbacks:
            server._osc_controller.dispatcher.unregister_callback(callback)

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
