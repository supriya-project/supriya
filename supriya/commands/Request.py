import abc

from uqbar.objects import new

from supriya.commands.Requestable import Requestable


class Request(Requestable):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PRIVATE METHODS ###

    def _apply_local(self, server):
        pass

    def _get_response_patterns_and_requestable(self, server):
        success_pattern, failure_pattern = self.response_patterns
        return success_pattern, failure_pattern, self

    def _handle_async(self, sync, server):
        if not sync or self.response_patterns[0] is None:
            message = self.to_osc()
            server.send_message(message)
            return True

    def _linearize(self):
        if hasattr(self, "callback") and self.callback:
            yield new(self, callback=None)
            yield from self.callback._linearize()
        else:
            yield self

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def to_osc(self, *, with_placeholders=False, with_request_name=False):
        raise NotImplementedError

    ### PUBLIC PROPERTIES ###

    @property
    def request_name(self):
        return self.request_id.request_name

    @property
    def response_patterns(self):
        return None, None

    @property
    @abc.abstractmethod
    def request_id(self):
        return NotImplementedError
