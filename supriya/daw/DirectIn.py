from supriya.realtime import Synth

from .DawNode import DawNode
from .Receive import Receive
from .synthdefs import build_send_synthdef


class DirectIn(DawNode):

    ### INITIALIZER ###

    def __init__(self, source_bus_id, source_bus_count, target):
        DawNode.__init__(self)
        assert source_bus_id >= 0
        assert source_bus_count > 0
        self._source_bus_id = int(source_bus_id)
        self._source_bus_count = int(source_bus_count)
        if not isinstance(getattr(target, "receive", None), Receive):
            raise ValueError(target)
        self._target = target
        self._channel_counts = None
        self._node = None

    ### PRIVATE METHODS ###

    def _actual_state(self):
        return {
            "channel_counts": self.channel_counts,
            "in_bus_id": self.node["in_"] if self.node is not None else None,
            "out_bus_id": self.node["out"] if self.node is not None else None,
        }

    def _expected_state(self):
        return {
            "channel_counts": (self.source_bus_count, self.target.channel_count),
            "in_bus_id": self.source_bus_id,
            "out_bus_id": int(self.target.bus_group),
        }

    def _free(self) -> bool:
        if not DawNode._free(self):
            return False
        if self.node is not None:
            self.node.free()
        self._channel_counts = None
        return True

    def _pre_allocate(self, server) -> bool:
        if not DawNode._pre_allocate(self, server):
            return False
        self._channel_counts = (self.source_bus_count, self.target.channel_count)
        return True

    def _post_allocate(self):
        DawNode._post_allocate(self)
        self._reallocate()

    def _reallocate(self):
        if not self._source.server:
            if self._node is not None:
                self._node.release()
                self._node = None
            return
        actual_state = self._actual_state()
        expected_state = self._expected_state()
        if actual_state == expected_state:
            return
        if self._node is not None:
            self._node.release()
        self._node = Synth(
            name="direct out",
            synthdef=build_send_synthdef(*self.channel_counts),
            in_=self.source_bus_id,
            out=int(self.target.bus_group),
        )
        self.parent.post_fader_group.append(self.node)

    ### PUBLIC PROPERTIES ###

    @property
    def channel_counts(self):
        return self._channel_counts

    @property
    def source_bus_id(self):
        return self._source_bus_id

    @property
    def source_bus_count(self):
        return self._source_bus_count

    @property
    def target(self):
        return self._target
