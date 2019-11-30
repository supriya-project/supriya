from typing import Optional
from uuid import UUID, uuid4

import supriya.xdaw  # noqa
from supriya.enums import AddAction
from supriya.querytree import QueryTreeGroup

from .bases import Allocatable, Mixer
from .sends import DirectOut
from .tracks import CueTrack, MasterTrack, Track, TrackContainer


class Context(Allocatable, Mixer):

    ### INITIALIZER ###

    def __init__(self, *, channel_count=None, name=None, uuid=None):
        Allocatable.__init__(self, channel_count=channel_count, name=name)
        Mixer.__init__(self)
        self._uuid = uuid or uuid4()
        self._master_track = MasterTrack()
        self._master_track.postfader_sends._append(
            DirectOut(0, self.effective_channel_count)
        )
        self._cue_track = CueTrack()
        self._cue_track.postfader_sends._append(
            DirectOut(self.effective_channel_count, 2)
        )
        self._tracks = TrackContainer("node", AddAction.ADD_TO_HEAD, label="Tracks")
        self._mutate(slice(None), [self._tracks, self._master_track, self._cue_track])

    ### SPECIAL METHODS ###

    def __str__(self):
        line = f"<{type(self).__name__} [...] {self.uuid}>"
        if self.node_proxy is not None:
            line = f"<{type(self).__name__} [{int(self.node_proxy)}] {self.uuid}>"
        lines = [line]
        for child in self:
            for line in str(child).splitlines():
                lines.append(f"    {line}")
        return "\n".join(lines)

    ### PRIVATE METHODS ###

    def _allocate(self, new_provider, target_node, add_action):
        super()._allocate(new_provider, target_node, add_action)
        self._node_proxies["node"] = new_provider.add_group(
            target_node=target_node, add_action=add_action, name=self.label
        )

    def _cleanup(self):
        Track._update_activation(self)

    ### PUBLIC METHODS ###

    def add_track(self, *, name=None) -> Track:
        with self.lock([self]):
            track = Track(name=name)
            self._tracks._append(track)
            return track

    def delete(self):
        with self.lock([self]):
            if self.parent:
                self.parent.remove_contexts(self)

    def move(self, container: "supriya.xdaw.Application", position: int):
        with self.lock([self, container]):
            container._contexts._mutate(slice(position, position), [self])

    def query(self):
        if self.provider.server is None:
            raise ValueError
        return QueryTreeGroup(
            node_id=self.node_proxy.identifier,
            children=[
                QueryTreeGroup(
                    node_id=self.tracks.node_proxy.identifier,
                    children=[track.query() for track in self.tracks],
                ),
                self.master_track.query(),
                self.cue_track.query(),
            ],
        ).annotate(self.provider.annotation_map)

    def remove_tracks(self, *tracks: "supriya.xdaw.Track"):
        with self.lock([self, *tracks]):
            if not all(track in self.tracks for track in tracks):
                raise ValueError
            for track in tracks:
                self._tracks._remove(track)

    def set_channel_count(self, channel_count: Optional[int]):
        with self.lock([self]):
            if channel_count is not None:
                assert 1 <= channel_count <= 8
                channel_count = int(channel_count)
            self._set(channel_count=channel_count)

    ### PUBLIC PROPERTIES ###

    @property
    def cue_track(self) -> CueTrack:
        return self._cue_track

    @property
    def master_track(self) -> MasterTrack:
        return self._master_track

    @property
    def tracks(self) -> TrackContainer:
        return self._tracks

    @property
    def uuid(self) -> UUID:
        return self._uuid
