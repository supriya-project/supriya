import threading
import time

from supriya.system.SupriyaValueObject import SupriyaValueObject


class Requestable(SupriyaValueObject):

    ### CLASS VARIABLES ###

    __slots__ = ('_condition', '_response')

    ### INITIALIZER ###

    def __init__(self):
        self._condition = threading.Condition()
        self._response = None

    ### PRIVATE METHODS ###

    def _get_response_pattern_and_message(self, server):
        raise NotImplementedError

    def _handle_async(self, sync, server):
        raise NotImplementedError

    def _linearize(self):
        raise NotImplementedError

    def _set_response(self, response):
        with self.condition:
            self._response = response
            self.condition.notify()

    ### PUBLIC METHODS ###

    def communicate(self, server=None, sync=True, timeout=1.0, apply_local=True):
        import supriya.realtime

        server = server or supriya.realtime.Server.get_default_server()
        assert isinstance(server, supriya.realtime.Server)
        assert server.is_running
        with server._lock:
            if apply_local:
                for request in self._linearize():
                    request._apply_local(server)
        # handle non-sync
        if self._handle_async(sync, server):
            return
        response_pattern, message = self._get_response_pattern_and_message(server)
        start_time = time.time()
        timed_out = False
        with self.condition:
            server.osc_io.register(
                pattern=response_pattern,
                procedure=self._set_response,
                once=True,
                parse_response=True,
            )
            server.send_message(message)
            while self.response is None:
                self.condition.wait(timeout)
                current_time = time.time()
                delta_time = current_time - start_time
                if timeout <= delta_time:
                    timed_out = True
                    break
        if timed_out:
            print('TIMED OUT:', repr(self))
            return None
        return self._response

    ### PUBLIC PROPERTIES ###

    @property
    def condition(self):
        return self._condition

    @property
    def response(self):
        return self._response
