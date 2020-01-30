import threading
import time

import supriya.system


class StatusWatcher(threading.Thread):

    ### CLASS VARIABLES ###

    __documentation_section__ = "Server Internals"

    __slots__ = ("_is_active", "_attempts", "_callback", "_server")

    max_attempts = 5
    sleep_base_time = 1.0
    exponential_backoff_factor = 1.5

    ### INITIALIZER ###

    def __init__(self, server):
        threading.Thread.__init__(self)
        self._attempts = 0
        self._server = server
        self._callback = None
        self.is_active = True
        self.daemon = True

    ### SPECIAL METHODS ###

    def __call__(self, response):
        if not self.is_active:
            return
        if response is None:
            return
        self._server._status = response
        self._attempts = 0
        supriya.system.PubSub.notify("server-status", response.to_dict())

    ### PUBLIC METHODS ###

    def run(self):
        import supriya.commands

        self._callback = self.server.osc_protocol.register(
            pattern="/status.reply", procedure=self.__call__
        )
        request = supriya.commands.StatusRequest()
        message = request.to_osc()
        while self._is_active and self.server.is_running:
            if self.max_attempts == self.attempts:
                print("+" * 80)
                print("SHUTTING DOWN")
                print("+" * 80)
                self.server._shutdown()
                break
            self._attempts += 1
            self.server.send_message(message)
            sleep_time = self.sleep_base_time * pow(
                self.exponential_backoff_factor, self._attempts
            )
            time.sleep(sleep_time)
        self.server.osc_protocol.unregister(self.callback)

    ### PUBLIC PROPERTIES ###

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, expr):
        self._is_active = bool(expr)

    @property
    def attempts(self):
        return self._attempts

    @property
    def callback(self):
        return self._callback

    @property
    def server(self):
        return self._server
