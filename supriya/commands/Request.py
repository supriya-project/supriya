import abc
import threading
import time
from supriya.system.SupriyaValueObject import SupriyaValueObject


class Request(SupriyaValueObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_condition',
        '_response',
        )

    _prototype = None

    ### INITIALIZER ###

    def __init__(self):
        self._condition = threading.Condition()
        self._response = None

    ### PRIVATE METHODS ###

    def _set_response(self, response):
        with self.condition:
            self._response = response
            self.condition.notify()

    ### PUBLIC METHODS ###

    def communicate(
        self,
        message=None,
        server=None,
        sync=True,
        timeout=1.0,
    ):
        import supriya.realtime
        server = server or supriya.realtime.Server.get_default_server()
        assert isinstance(server, supriya.realtime.Server)
        assert server.is_running
        message = message or self.to_osc_message()
        if not sync or not self.response_patterns:
            server.send_message(message)
            return None
        response_pattern = self.response_patterns[0]
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

    def to_datagram(self):
        return self.to_osc_message().to_datagram()

    def to_list(self, with_textual_osc_command=False):
        return self.to_osc_message(
            with_textual_osc_command=with_textual_osc_command
            ).to_list()

    @abc.abstractmethod
    def to_osc_message(self, with_textual_osc_command=False):
        raise NotImplementedError

    ### PUBLIC PROPERTIES ###

    @property
    def condition(self):
        return self._condition

    @property
    def request_command(self):
        return self.request_id.osc_command

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, response):
        import supriya.commands
        assert isinstance(response, supriya.commands.Response)
        with self.condition:
            self._response = response
            self.condition.notify()

    @property
    def response_patterns(self):
        return []

    @property
    @abc.abstractmethod
    def request_id(self):
        return NotImplementedError
