import abc
import collections
import threading
import time
import supriya.osc
from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class Request(SupriyaValueObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_condition',
        '_response',
        )

    _prototype = None

    ### INITIALIZER ###

    def __init__(
        self,
        ):
        self._condition = threading.Condition()
        self._response = None

    ### SPECIAL METHODS ###

    def __repr__(self):
        import supriya.utils
        return supriya.utils.get_object_repr(self, multiline=True)

    ### PRIVATE METHODS ###

    def _coerce_completion_message_input(self, message):
        if message is None:
            return message
        elif isinstance(message, (supriya.osc.OscMessage, supriya.osc.OscBundle)):
            return message
        elif isinstance(message, Request):
            return message.to_osc_message()
        elif isinstance(message, collections.Sequence):
            return supriya.osc.OscMessage(*message)
        raise ValueError(message)

    def _coerce_completion_message_output(self, contents):
        if self.completion_message is not None:
            completion_message = self.completion_message.to_datagram()
            completion_message = bytearray(completion_message)
            contents.append(completion_message)

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
        if not sync or self.response_specification is None:
            server.send_message(message)
            return None
        start_time = time.time()
        timed_out = False
        with self.condition:
            with server.response_dispatcher.lock:
                callback = self.response_callback
                server.register_response_callback(callback)
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

    @abc.abstractmethod
    def to_osc_message(self, with_textual_osc_command=False):
        raise NotImplementedError

    def to_list(self, with_textual_osc_command=False):
        return self.to_osc_message(
            with_textual_osc_command=with_textual_osc_command
            ).to_list()

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
    def response_callback(self):
        import supriya.commands
        return supriya.commands.RequestCallback(
            is_one_shot=True,
            request=self,
            response_specification=self.response_specification,
            )

    @property
    def response_specification(self):
        return None
