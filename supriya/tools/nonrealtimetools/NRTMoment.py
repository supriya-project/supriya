# -*- encoding: utf-8 -*-


class NRTMoment(object):

    def __init__(self, session, timestep):
        self.dirty = False
        self.node_commands = []
        self.nodes_to_children = {}
        self.nodes_to_parent = {}
        self.session = session
        self.timestep = timestep

    def __enter__(self):
        if self.session.active_moments:
            self.session.active_moments[-1]._refresh()
        self.session.active_moments.append(self)

    def __exit__(self, exc_type, exc_value, traceback):
        self._session.active_moments.pop()
        self._refresh()

    def _refresh(self):
        if not self.dirty:
            pass
        self.dirty = False
