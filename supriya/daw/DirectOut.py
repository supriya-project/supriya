from supriya.realtime import Synth

from .DawNode import DawNode
from .synthdefs import build_send_synthdef


class DirectOut(DawNode):

    ### INITIALIZER ###

    def __init__(self, source, target_bus_id, target_bus_count):
        DawNode.__init__(self)
        self._source = source
        assert target_bus_id >= 0
        assert target_bus_count > 0
        self._target_bus_id = int(target_bus_id)
        self._target_bus_count = int(target_bus_count)
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
            "channel_counts": (self.source.channel_count, self.target_bus_count),
            "in_bus_id": int(self.source.bus_group),
            "out_bus_id": self.target_bus_id,
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
        self._channel_counts = (self.source.channel_count, self.target_bus_count)
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
            in_=int(self.source.bus_group),
            out=self.target_bus_id,
        )
        self.parent.post_fader_group.append(self.node)

    ### PUBLIC PROPERTIES ###

    @property
    def channel_counts(self):
        return self._channel_counts

    @property
    def source(self):
        return self._source

    @property
    def target_bus_id(self):
        return self._target_bus_id

    @property
    def target_bus_count(self):
        return self._target_bus_count
