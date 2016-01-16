# -*- encoding: utf-8 -*-
import bisect


class NRTSession(object):

    ### INITIALIZER ###

    def __init__(self):
        from supriya.tools import nonrealtimetools
        self.nodes = set()
        self.active_moments = []
        self.offsets = []
        self.moments = {}
        self.root_node = nonrealtimetools.NRTRootNode(self)
        self._setup_initial_moments()

    ### PRIVATE METHODS ###

    def _find_moment_after(self, offset):
        index = bisect.bisect(self.offsets, offset)
        if index < len(self.offsets):
            old_offset = self.offsets[index]
            if offset < old_offset:
                return self.moments[old_offset]
        return None

    def _find_moment_at(self, offset):
        return self.moments.get(offset, None)

    def _find_moment_before(self, offset):
        index = bisect.bisect_left(self.offsets, offset)
        if index == len(self.offsets):
            index -= 1
        old_offset = self.offsets[index]
        if offset <= old_offset:
            index -= 1
        if index < 0:
            return None
        old_offset = self.offsets[index]
        return self.moments[old_offset]

    def _setup_initial_moments(self):
        from supriya.tools import nonrealtimetools
        offset = float('-inf')
        moment = nonrealtimetools.NRTMoment(self, offset)
        moment.nodes_to_children[self.root_node] = None
        moment.nodes_to_parent[self.root_node] = None
        self.moments[offset] = moment
        self.offsets.append(offset)
        offset = 0
        moment = moment._clone(offset)
        self.moments[offset] = moment
        self.offsets.append(offset)

    ### PUBLIC METHODS ###

    def at(self, offset):
        assert 0 <= offset
        moment = self._find_moment_at(offset)
        if moment:
            return moment
        old_moment = self._find_moment_before(offset)
        new_moment = old_moment._clone(offset)
        self.moments[offset] = new_moment
        self.offsets.insert(
            self.offsets.index(old_moment.offset) + 1,
            offset,
            )
        return new_moment

    def add_group(self, add_action=None):
        return self.root_node.add_group(add_action=add_action)

    def add_synth(self, duration=None, add_action=None):
        return self.root_node.add_synth(duration=duration, add_action=add_action)

    def move_node(self, node, add_action=None):
        self.root_node.move_node(node, add_action=add_action)

    def report(self):
        states = []
        for offset in self.offsets[1:]:
            moment = self.moments[offset]
            state = moment.report()
            states.append(state)
        return states
