# -*- encoding: utf-8 -*-
import threading
import time


class StatusWatcher(threading.Thread):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_active',
        '_attempts',
        '_response_callback',
        '_server',
        )

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
        self._server._server_status = response
        self._attempts = 0

    ### PUBLIC METHODS ###

    def run(self):
        from supriya.tools import servertools
        self.server.register_response_callback(self.response_callback)
        message = servertools.CommandManager.make_status_message()
        while self._active:
            if 5 < self.attempts:
                self.server.quit()
                break
            self.server.send_message(message)
            self._attempts += 1
            time.sleep(0.2)
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