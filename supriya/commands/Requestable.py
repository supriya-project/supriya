import logging
import threading
import time

from supriya.system.SupriyaValueObject import SupriyaValueObject

logger = logging.getLogger("supriya.osc")


class Requestable(SupriyaValueObject):

    ### CLASS VARIABLES ###

    __slots__ = ("_condition", "_response")

    ### INITIALIZER ###

    def __init__(self):
        self._condition = threading.Condition()
        self._response = None

    ### PRIVATE METHODS ###

    def _get_response_patterns_and_requestable(self, server):
        raise NotImplementedError

    def _handle_async(self, sync, server):
        raise NotImplementedError

    def _linearize(self):
        raise NotImplementedError

    def _sanitize_node_id(self, node_id, with_placeholders):
        if not isinstance(node_id, int) and with_placeholders:
            return -1
        return int(node_id)

    def _set_response(self, response):
        with self.condition:
            self._response = response
            self.condition.notify()

    ### PUBLIC METHODS ###

    def communicate(self, server=None, sync=True, timeout=1.0, apply_local=True):
        import supriya.realtime

        server = server or supriya.realtime.Server.default()
        assert isinstance(server, supriya.realtime.Server)
        assert server.is_running
        with server._lock:
            if apply_local:
                for request in self._linearize():
                    request._apply_local(server)
        # handle non-sync
        if self._handle_async(sync, server):
            return
        (
            success_pattern,
            failure_pattern,
            requestable,
        ) = self._get_response_patterns_and_requestable(server)
        start_time = time.time()
        timed_out = False
        with self.condition:
            try:
                server.osc_io.register(
                    pattern=success_pattern,
                    failure_pattern=failure_pattern,
                    procedure=self._set_response,
                    once=True,
                    parse_response=True,
                )
            except Exception:
                print(self)
                raise
            server.send_message(requestable)
            while self.response is None:
                self.condition.wait(timeout)
                current_time = time.time()
                delta_time = current_time - start_time
                if timeout <= delta_time:
                    timed_out = True
                    break
        if timed_out:
            logger.warning("Timed out: {!r}".format(self))
            return None
        return self._response

    def to_datagram(self, *, with_placeholders=False, with_request_name=False):
        return self.to_osc(
            with_placeholders=with_placeholders, with_request_name=with_request_name
        ).to_datagram()

    def to_list(self, *, with_placeholders=False, with_request_name=False):
        return self.to_osc(
            with_placeholders=with_placeholders, with_request_name=with_request_name
        ).to_list()

    ### PUBLIC PROPERTIES ###

    @property
    def condition(self):
        return self._condition

    @property
    def response(self):
        return self._response
