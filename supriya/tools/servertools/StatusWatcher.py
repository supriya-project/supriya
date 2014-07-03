# -*- encoding: utf-8 -*-
import threading
import time
from supriya.tools import osctools


class StatusWatcher(threading.Thread):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_active',
        '_attempts',
        '_osc_callback',
        '_server',
        )

    ### INITIALIZER ###

    def __init__(self, server):
        threading.Thread.__init__(self)
        self._attempts = 0
        self._server = server
        self._osc_callback = osctools.OscCallback(
            address_pattern='/status.reply',
            procedure=lambda message: self.__call__(message),
            )
        self.active = True
        self.daemon = True

    ### SPECIAL METHODS ###

    def __call__(self, message):
        from supriya.tools import responsetools
        if not self.active:
            return
        response = responsetools.ResponseManager.handle_message(message)
        self._server._server_status = response
        self._attempts = 0

    ### PUBLIC METHODS ###

    def run(self):
        from supriya.tools import servertools
        self.server.register_osc_callback(self.osc_callback)
        message = servertools.CommandManager.make_status_message()
        while self._active:
            if 5 < self.attempts:
                self.server.quit()
                break
            self.server.send_message(message)
            self._attempts += 1
            time.sleep(0.2)
        self.server.unregister_osc_callback(self.osc_callback)

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
    def osc_callback(self):
        return self._osc_callback

    @property
    def server(self):
        return self._server



