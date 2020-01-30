from typing import Optional

from supriya.realtime.nodes import Synth

from .DawNode import DawNode
from .Receive import Receive
from .synthdefs import build_send_synthdef


class Send(DawNode):

    DEFAULT = object()

    ### INITIALIZER ###

    def __init__(self, source, target, *, post_fader=True):
        DawNode.__init__(self)
        if target is not self.DEFAULT:
            receive = getattr(target, "receive")
            if not isinstance(receive, Receive):
                raise ValueError(target)
        self._target = target
        self._cached_target = None
        self._post_fader = bool(post_fader)
        self._node = None
        self._channel_counts = None

    ### PRIVATE METHODS ###

    def _actual_state(self):
        return {
            "channel_counts": self.channel_counts,
            "in_bus_id": self.node["in_"] if self.node is not None else None,
            "out_bus_id": self.node["out"] if self.node is not None else None,
            "post_fader": (
                "post-fader" in self.node.parent.name
                if self.node is not None
                else self.post_fader
            ),
            "target": self.cached_target,
        }

    def _expected_state(self):
        state = {
            "channel_counts": (
                self.source.channel_count,
                self.actual_target.channel_count,
            ),
            "in_bus_id": int(self.source.bus_group),
            "post_fader": self.post_fader,
            "out_bus_id": (
                int(self.actual_target.receive.succeeding_bus_group)
                if self.graph_order < self.actual_target.receive.graph_order
                else int(self.actual_target.receive.preceding_bus_group)
            ),
            "target": self.actual_target,
        }
        return state

    def _free(self) -> bool:
        if not DawNode._free(self):
            return False
        self.cached_target.receive._remove_incoming_send(self)
        if self.node is not None:
            self.node.release()
            self._node = None
        self._channel_counts = None
        return True

    def _post_allocate(self):
        DawNode._post_allocate(self)
        self._reallocate()

    def _pre_allocate(self, server) -> bool:
        if not DawNode._pre_allocate(self, server):
            return False
        actual_target = self.actual_target
        actual_target.receive._add_incoming_send(self)
        self._cached_target = actual_target
        self._channel_counts = (self.source.channel_count, actual_target.channel_count)
        return True

    def _reallocate(self):
        DawNode._reallocate(self)
        if not (self.source.server and self.actual_target.server):
            if self.node is not None:
                self.node.release()
            self._debug_tree("Bailing")
            return
        actual_state = self._actual_state()
        expected_state = self._expected_state()
        if actual_state == expected_state:
            self._debug_tree("Matches")
            return
        self._debug_tree("Recreating")
        if actual_state["target"] != expected_state["target"]:
            actual_state["target"].receive._remove_incoming_send(self)
            expected_state["target"].receive._add_incoming_send(self)
        self._cached_target = expected_state["target"]
        if self.node is not None:
            self.node.release()
        self._channel_counts = expected_state["channel_counts"]
        self._node = Synth(
            name=f"to {self.cached_target.node.name}",
            synthdef=build_send_synthdef(*self.channel_counts),
            in_=expected_state["in_bus_id"],
            out=expected_state["out_bus_id"],
        )
        if self.post_fader:
            self.parent.post_fader_group.append(self.node)
        else:
            self.parent.pre_fader_group.append(self.node)

    ### PUBLIC PROPERTIES ###

    @property
    def actual_target(self):
        if self.target is self.DEFAULT:
            return self.parent.parent.default_send_target
        return self.target

    @property
    def cached_target(self):
        return self._cached_target

    @property
    def channel_counts(self):
        return self._channel_counts

    @property
    def node(self) -> Optional[Synth]:
        return self._node

    @property
    def post_fader(self):
        return self._post_fader

    @property
    def source(self):
        for parent in self.parentage:
            if hasattr(parent, "sends"):
                return parent

    @property
    def target(self):
        return self._target
