from typing import Optional

from uqbar.containers import UniqueTreeTuple

from supriya.realtime import Group, Server

from .DawNode import DawNode
from .DeviceType import DeviceType
from .MixerContext import MixerContext
from .SceneContainer import SceneContainer
from .Send import Send
from .Track import Track
from .TrackContainer import TrackContainer
from .Transport import Transport


class Application(UniqueTreeTuple, MixerContext):
    """
    A DAW application.
    """

    ### INITIALIZER ###

    def __init__(self, *, channel_count=2):
        self._channel_count = channel_count
        self._scenes = SceneContainer()
        self._scenes._parent = self
        self._server = None
        self._soloed_tracks = set()

        self._transport = Transport()
        self._tracks = TrackContainer()
        self._return_tracks = TrackContainer(name="return track container")
        self._master_track = Track(
            device_types=(DeviceType.AUDIO,),
            channel_count=channel_count,
            name="master track",
        )
        self._cue_track = Track(
            device_types=(DeviceType.AUDIO,),
            channel_count=channel_count,
            name="cue track",
        )

        UniqueTreeTuple.__init__(
            self,
            children=[
                self._transport,
                self._tracks,
                self._return_tracks,
                self._master_track,
                self._cue_track,
            ],
        )
        self._node = Group(children=[_.node for _ in self], name="application")

    ### PUBLIC METHODS ###

    def add_scene(self):
        scene = self._scenes.add_scene()
        for child in self.depth_first():
            if isinstance(child, Track):
                child.slots.add_slot()
        return scene

    def add_track(self, channel_count=2, name=None) -> Track:
        """
        Add a track.
        """
        track = Track(channel_count=channel_count, name=name)
        self.tracks.append(track)
        track.add_send(Send.DEFAULT)
        return track

    def boot(self, server=None) -> None:
        """
        Boot the DAW application.
        """
        self._server = server or Server.default()
        if not self._server.is_running:
            self._server.boot()
        for alloc_node in reversed(self):  # type: DawNode
            alloc_node._pre_allocate(self._server)
        self._node.allocate(target_node=self._server)
        for post_alloc_node in reversed(self):  # type: DawNode
            post_alloc_node._post_allocate()

    def quit(self) -> None:
        """
        Quit the DAW application.
        """
        self._node.free()
        for node in reversed(self):  # type: DawNode
            node._free()
        self._server.quit()
        self._server = None

    ### PUBLIC PROPERTIES ###

    @property
    def channel_count(self) -> int:
        """
        Get the application channel count.
        """
        return self._channel_count

    @property
    def cue_track(self) -> Track:
        """
        Get the application cue track.
        """
        return self._cue_track

    @property
    def node(self) -> Group:
        """
        Get the application's underlying server node.
        """
        return self._node

    @property
    def master_track(self) -> Track:
        """
        Get the application's master track.
        """
        return self._master_track

    @property
    def server(self) -> Optional[Server]:
        """
        Get the application's underlying server.
        """
        return self._server

    @property
    def return_tracks(self) -> TrackContainer:
        """
        Get the application's track container.
        """
        return self._return_tracks

    @property
    def tracks(self) -> TrackContainer:
        """
        Get the application's track container.
        """
        return self._tracks

    @property
    def transport(self) -> Transport:
        """
        Get the application's transport.
        """
        return self._transport
