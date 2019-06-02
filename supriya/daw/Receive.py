import abc

from .DawNode import DawNode


class Receive(DawNode):

    ### INITIALIZER ###

    def __init__(self):
        DawNode.__init__(self)
        self._incoming_sends = set()

    ### PRIVATE METHODS ###

    def _iterate_sends(self):
        for send in sorted(self._incoming_sends, key=lambda x: x.graph_order):
            yield send

    def _pre_allocate(self, server) -> bool:
        if not DawNode._pre_allocate(self, server):
            return False
        for send in self._iterate_sends():
            send._reallocate()
        return True

    def _add_incoming_send(self, send):
        self._incoming_sends.add(send)

    def _free(self) -> bool:
        if not DawNode._free(self):
            return False
        for send in self._iterate_sends():
            send._free()
        return True

    def _post_allocate(self):
        DawNode._post_allocate(self)
        for send in self._iterate_sends():
            send._reallocate()

    def _reallocate(self):
        DawNode._reallocate(self)
        for send in self._iterate_sends():
            send._reallocate()

    def _remove_incoming_send(self, send):
        try:
            self._incoming_sends.remove(send)
        except KeyError:
            pass

    ### PUBLIC PROPERTIES ###

    @property
    @abc.abstractmethod
    def preceding_bus_group(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def succeeding_bus_group(self):
        raise NotImplementedError
