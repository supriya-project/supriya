from supriya.realtime import Group

from .DawContainer import DawContainer
from .Track import Track


class TrackContainer(DawContainer):

    ### INITIALIZER ###

    def __init__(self, name=None):
        DawContainer.__init__(self)
        self._node = Group(name=name or "track container")
        self._soloed_tracks = set()

    ### PRIVATE METHODS ###

    def _collect_roots(self, new_items, old_items):
        return DawContainer._collect_roots(
            self, new_items, old_items, prototype=(type(self), Track)
        )

    def _process_roots(self, roots):
        for root in roots:
            if isinstance(root, Track):
                root._update_activation()
            else:
                for track in root:
                    track._update_activation()

    ### PRIVATE PROPERTIES ###

    @property
    def _node_class(self):
        return Track
