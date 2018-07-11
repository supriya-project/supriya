import threading
import time
import supriya.system


class StatusWatcher(threading.Thread):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Server Internals'

    __slots__ = (
        '_active',
        '_attempts',
        '_callback',
        '_server',
        )

    max_attempts = 5

    ### INITIALIZER ###

    def __init__(self, server):
        threading.Thread.__init__(self)
        self._attempts = 0
        self._server = server
        self._callback = None
        self.active = True
        self.daemon = True

    ### SPECIAL METHODS ###

    def __call__(self, response):
        if not self.active:
            return
        if response is None:
            return
        self._server._status = response
        self._attempts = 0
        supriya.system.PubSub.notify(
            'server-status',
            response.to_dict(),
            )

    ### PUBLIC METHODS ###

    def run(self):
        import supriya.commands
        self._callback = self.server.osc_io.register(
            pattern='/status.reply',
            procedure=self.__call__,
            parse_response=True,
        )
        request = supriya.commands.StatusRequest()
        message = request.to_osc_message()
        while self._active:
            if self.max_attempts == self.attempts:
                self.server.quit()
                break
            self.server.send_message(message)
            self._attempts += 1
            time.sleep(0.1)
        self.server.osc_io.unregister(self.callback)

    ### PUBLIC PROPERTIES ###

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, expr):
        self._active = bool(expr)

    @property
    def attempts(self):
        return self._attempts

    @property
    def callback(self):
        return self._callback

    @property
    def server(self):
        return self._server
