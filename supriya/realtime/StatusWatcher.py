import threading
import time
from supriya.tools import systemtools


class StatusWatcher(threading.Thread):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Server Internals'

    __slots__ = (
        '_active',
        '_attempts',
        '_response_callback',
        '_server',
        )

    max_attempts = 5

    ### INITIALIZER ###

    def __init__(self, server):
        from supriya.tools import responsetools
        threading.Thread.__init__(self)
        self._attempts = 0
        self._server = server
        self._response_callback = responsetools.ResponseCallback(
            procedure=lambda message: self.__call__(message),
            prototype=(
                responsetools.StatusResponse,
                ),
            )
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
        systemtools.PubSub.notify(
            'server-status',
            response.to_dict(),
            )

    ### PUBLIC METHODS ###

    def run(self):
        from supriya.tools import requesttools
        self.server.register_response_callback(self.response_callback)
        request = requesttools.StatusRequest()
        message = request.to_osc_message()
        while self._active:
            if self.max_attempts == self.attempts:
                self.server.quit()
                break
            self.server.send_message(message)
            self._attempts += 1
            time.sleep(0.1)
        self.server.unregister_response_callback(self.response_callback)

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
    def response_callback(self):
        return self._response_callback

    @property
    def server(self):
        return self._server
