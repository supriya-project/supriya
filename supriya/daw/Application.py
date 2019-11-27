import logging
import threading
from typing import Optional, Set

from uqbar.containers import UniqueTreeTuple

from supriya.commands import RequestBundle
from supriya.midi import MidiMessage
from supriya.realtime import Group, Server

from .DawNode import DawNode
from .DeviceType import DeviceType
from .MixerContext import MixerContext
from .SceneContainer import SceneContainer
from .Send import Send
from .Track import Track
from .TrackContainer import TrackContainer
from .Transport import Transport

logger = logging.getLogger("supriya.daw")


class Application(UniqueTreeTuple, MixerContext):
    """
    A DAW application.
    """

    ### CLASS VARIABLES ###

    _applications: Set["Application"] = set()

    ### INITIALIZER ###

    def __init__(self, *, channel_count=2):
        self._lock = threading.RLock()

        self._channel_count = channel_count
        self._controller = None
        self._midi_monitoring_tracks = []
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
        self._master_track.add_direct_out(
            target_bus_id=0, target_bus_count=self.channel_count
        )
        self._cue_track.add_direct_out(
            target_bus_id=self.channel_count, target_bus_count=self.channel_count
        )

    ### PRIVATE METHODS ###

    def _debug_tree(self, prefix, suffix=None):
        message = (
            f"{(prefix + ':').ljust(15)} {type(self).__name__}"
            f"{' (' + self.node.name + ')' if self.node else ''}"
        )
        if suffix:
            message += " " + suffix
        print(message)

    ### PUBLIC METHODS ###

    def add_scene(self):
        scene = self._scenes.add_scene()
        for child in self.depth_first():
            if isinstance(child, Track):
                child.slots.add_slot()
        return scene

    def add_return_track(self, channel_count=2, name=None) -> Track:
        """
        Add a return track.
        """
        track = Track(channel_count=channel_count, name=name)
        self.return_tracks.append(track)
        track.add_send(Send.DEFAULT)
        return track

    def add_track(self, channel_count=2, name=None) -> Track:
        """
        Add a track.
        """
        track = Track(channel_count=channel_count, name=name)
        self.tracks.append(track)
        track.add_send(Send.DEFAULT)
        return track

    def boot(self, server=None) -> "Application":
        """
        Boot the DAW application.
        """
        logger.debug("Booting")
        Application._applications.add(self)
        self._server = server or Server.default()
        if not self._server.is_running:
            self._server.boot()
        for alloc_node in reversed(list(self)):  # type: DawNode
            alloc_node._pre_allocate(self._server)
        self._node.allocate(target_node=self._server)
        for post_alloc_node in reversed(list(self)):  # type: DawNode
            post_alloc_node._post_allocate()
        logger.debug("Booted")
        return self

    def receive_midi_message(self, message: MidiMessage):
        moment = None
        if self.transport.clock.is_running:
            seconds = self.transport.clock.get_current_time()
            moment = self.transport.clock._seconds_to_moment(seconds)
        in_midi_messages = (message,)
        self._debug_tree("MIDI", suffix=type(message).__name__)
        for track in self._midi_monitoring_tracks:
            track.perform(moment, in_midi_messages)

    def quit(self) -> "Application":
        """
        Quit the DAW application.
        """
        logger.debug("Quitting")
        if self in Application._applications:
            Application._applications.remove(self)
        self._transport.stop()
        for node in list(reversed(list(self))):  # type: DawNode
            node._free()
        if self._server:
            if self._server.is_running:
                self._server.quit()
            self._server = None
        logger.debug("Quit")
        return self

    def send_requests(self, moment, requests):
        timestamp = moment.seconds if moment else None
        request_bundle = RequestBundle(timestamp=timestamp, contents=requests)
        if not (self.server and self.server.is_running):
            return
        request_bundle.communicate(apply_local=False, server=self.server, sync=False)

    def set_controller(self, controller, port_number=0, virtual=False):
        if self._controller and controller is not self._controller:
            self._controller.quit()
            self._controller.unregister(self.receive_midi_message)
        self._controller = controller
        if self._controller:
            if not controller.is_running:
                controller.boot(virtual=virtual)
            controller.register(self.receive_midi_message)
        return controller

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
