import time


class WaitForServer(object):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_callback',
        '_called_back',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        address_pattern=None,
        argument_template=None,
        ):
        from supriya import osclib
        self._called_back = False
        self._callback = osclib.OscCallback(
            address_pattern=address_pattern,
            argument_template=argument_template,
            is_one_shot=True,
            procedure=self.__call__,
            )

    ### SPECIAL METHODS ###

    def __call__(self, message):
        self._called_back = True

    def __enter__(self):
        from supriya import controllib
        server = controllib.Server()
        server._osc_controller.dispatcher.register_callback(self.callback)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        while not self.called_back:
            time.sleep(0.01)

    ### PUBLIC PROPERTIES ###

    @property
    def called_back(self):
        return self._called_back

    @property
    def callback(self):
        return self._callback
