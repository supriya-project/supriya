import abc
from uqbar.objects import new
from supriya.commands.Requestable import Requestable


class Request(Requestable):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PRIVATE METHODS ###

    def _apply_local(self, server):
        pass

    def _get_response_pattern_and_message(self, server):
        response_pattern = self.response_patterns[0]
        message = self.to_osc()
        return response_pattern, message

    def _handle_async(self, sync, server):
        if not sync or not self.response_patterns:
            message = self.to_osc()
            server.send_message(message)
            return True

    def _linearize(self):
        if hasattr(self, 'callback') and self.callback:
            yield new(self, callback=None)
            yield from self.callback._linearize()
        else:
            yield self

    ### PUBLIC METHODS ###

    def to_datagram(self):
        return self.to_osc().to_datagram()

    def to_list(self, with_textual_osc_command=False):
        return self.to_osc(
            with_textual_osc_command=with_textual_osc_command
            ).to_list()

    @abc.abstractmethod
    def to_osc(self, with_textual_osc_command=False):
        raise NotImplementedError

    ### PUBLIC PROPERTIES ###

    @property
    def request_command(self):
        return self.request_id.osc_command

    @property
    def response_patterns(self):
        return []

    @property
    @abc.abstractmethod
    def request_id(self):
        return NotImplementedError
