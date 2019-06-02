from .DeviceType import DeviceType
from .Send import Send
from .Track import Track
from .TrackContainer import TrackContainer


class GroupTrack(Track):
    """
    A group track.
    """

    ### INITIALIZER ###

    def __init__(self, *, channel_count=2, name=None):
        Track.__init__(
            self,
            device_types=(DeviceType.AUDIO,),
            channel_count=channel_count,
            name=name,
        )
        self._tracks = TrackContainer()
        self._mutate([self.tracks, self.receive, self.devices, self.sends])
        self._node[:] = [
            self.input_synth,
            self.tracks.node,
            self.devices.node,
            self.sends.pre_fader_group,
            self.output_synth,
            self.sends.post_fader_group,
        ]

    ### PUBLIC METHODS ###

    def add_track(self, channel_count=2, name=None) -> Track:
        track = Track(channel_count=channel_count, name=name)
        self.tracks.append(track)
        track.add_send(Send.DEFAULT)
        return track

    @classmethod
    def group(cls, tracks, name=None):
        print("Grouping...")
        if not tracks:
            raise ValueError("No tracks to group")
        if not all(isinstance(track, Track) for track in tracks):
            raise ValueError("Cannot group non-tracks")
        if len(set(track.application for track in tracks)) > 1:
            raise ValueError("All tracks must share same application")
        if len(set(track.parent for track in tracks)) > 1:
            raise ValueError("All tracks must share same parent")
        group_track = cls(name=name)
        group_track.add_send(Send.DEFAULT)
        index = tracks[0].parent.index(tracks[0])
        tracks[0].parent.insert(index, group_track)
        group_track.tracks.extend(tracks)
        return group_track

    def ungroup(self) -> None:
        self._debug_tree("Ungrouping")
        if self.parent is None:
            raise ValueError("Cannot ungroup without parent")
        index = self.parent.index(self)
        self.parent[index : index + 1] = self.tracks[:]

    ### PUBLIC PROPERTIES ###

    @property
    def receive(self):
        return self._receive

    @property
    def tracks(self):
        return self._tracks
