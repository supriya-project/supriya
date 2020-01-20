import enum
import time
from collections import deque
from threading import RLock
from typing import Optional, Tuple

from uqbar.containers import UniqueTreeTuple

from supriya.nonrealtime.Session import Session
from supriya.osc import OscIO
from supriya.provider import Provider

from .bases import Container
from .clips import Scene
from .contexts import Context
from .controllers import Controller
from .transports import Transport


class Application(UniqueTreeTuple):

    ### CLASS VARIABLES ###

    class Status(enum.IntEnum):
        OFFLINE = 0
        REALTIME = 1
        NONREALTIME = 2

    ### INITIALIZER ###

    def __init__(self, channel_count=2):
        # non-tree objects
        self._channel_count = int(channel_count)
        self._lock = RLock()
        self._status = self.Status.OFFLINE
        # tree objects
        self._contexts = Container(label="Contexts")
        self._controllers = Container(label="Controllers")
        self._scenes = Container(label="Scenes")
        self._transport = Transport()
        UniqueTreeTuple.__init__(
            self,
            children=[self._transport, self._controllers, self._scenes, self._contexts],
        )

    ### SPECIAL METHODS ###

    def __str__(self):
        return "\n".join(
            [
                f"<{type(self).__name__} [{self.status.name}] {hex(id(self))}>",
                *(f"    {line}" for child in self for line in str(child).splitlines()),
            ]
        )

    ### PRIVATE METHODS ###

    def _set_items(self, new_items, old_items, start_index, stop_index):
        UniqueTreeTuple._set_items(self, new_items, old_items, start_index, stop_index)
        for item in new_items:
            item._set(application=self)
        for item in old_items:
            item._set(application=None)

    ### PUBLIC METHODS ###

    def add_context(self, *, name=None):
        with self.lock:
            if self.status == self.Status.NONREALTIME:
                raise ValueError
            context = Context(name=name)
            self._contexts._append(context)
            if self.status == self.Status.REALTIME:
                provider = Provider.realtime(port=OscIO.find_free_port())
                with provider.at():
                    context._set(provider=provider)
            return context

    def add_controller(self, *, name=None) -> Controller:
        with self.lock:
            controller = Controller(name=name)
            self._controllers._append(controller)
        return controller

    def add_scene(self, *, name=None) -> Scene:
        from supriya.xdaw.clips import Slot

        with self.lock:
            scene = Scene(name=name)
            self._scenes._append(scene)
            tracks = deque()
            for context in self.contexts:
                tracks.extend(context.tracks)
            while tracks:
                track = tracks.pop()
                if track.tracks:
                    tracks.extend(track.tracks)
                while len(track.slots) < len(self.scenes):
                    track.slots._append(Slot())
        return scene

    def boot(self):
        with self.lock:
            if self.status == self.Status.REALTIME:
                return
            elif self.status == self.Status.NONREALTIME:
                raise ValueError
            elif not self.contexts:
                raise ValueError
            for context in self.contexts:
                provider = Provider.realtime(port=OscIO.find_free_port())
                with provider.at():
                    context._set(provider=provider)
            time.sleep(0.1)  # wait for /done messages
            self._status = self.Status.REALTIME
        return self

    def flush(self):
        pass

    @classmethod
    def new(cls, context_count=1, track_count=4, scene_count=8):
        application = cls()
        for _ in range(context_count):
            context = application.add_context()
            for _ in range(track_count):
                context.add_track()
        for _ in range(scene_count):
            application.add_scene()
        return application

    def perform(self, midi_messages, moment=None):
        with self.lock:
            if self.status != self.Status.REALTIME:
                return
            for context in self.contexts:
                context.perform(midi_messages, moment=moment)

    def quit(self):
        self.transport.stop()
        with self.lock:
            if self.status == self.Status.OFFLINE:
                return
            elif self.status == self.Status.NONREALTIME:
                raise ValueError
            for context in self.contexts:
                provider = context.provider
                with provider.at():
                    context._set(provider=None)
                if provider is not None:
                    provider.quit()
            self._status = self.Status.OFFLINE
        return self

    def remove_contexts(self, *contexts: Context):
        with self.lock:
            if not all(context in self.contexts for context in contexts):
                raise ValueError
            for context in contexts:
                provider = context.provider
                if provider is not None:
                    with provider.at():
                        self._contexts._remove(context)
                    provider.quit()
                else:
                    self._contexts._remove(context)
            if not len(self):
                self._status = self.Status.OFFLINE

    def remove_controllers(self, *controllers: Controller):
        with self.lock:
            if not all(controller in self.controllers for controller in controllers):
                raise ValueError
            for controller in controllers:
                self._controllers._remove(controller)

    def remove_scenes(self, *scenes: Scene):
        with self.lock:
            if not all(scene in self.scenes for scene in scenes):
                raise ValueError
            indices = sorted(self.scenes.index(scene) for scene in scenes)
            tracks = deque()
            for context in self.contexts:
                tracks.extend(context.tracks)
            while tracks:
                track = tracks.pop()
                if track.tracks:
                    tracks.extend(track.tracks)
                for index in reversed(indices):
                    track.slots._remove(track.slots[index])

    def render(self) -> Session:
        with self.lock:
            if self.status != self.Status.OFFLINE:
                raise ValueError
            self._status == self.Status.NONREALTIME
            provider = Provider.nonrealtime()
            with provider.at():
                for context in self.contexts:
                    context._set(provider=provider)
            # Magic happens here
            with provider.at(provider.session.duration or 10):
                for context in self.contexts:
                    context._set(provider=None)
            self._status = self.Status.OFFLINE
            return provider.session

    def serialize(self):
        return {
            "kind": type(self).__name__,
            "spec": {
                "channel_count": self.channel_count,
                "contexts": [context.serialize() for context in self.contexts],
                "transport": self.transport.serialize(),
            },
        }

    def set_channel_count(self, channel_count: int):
        with self.lock:
            assert 1 <= channel_count <= 8
            self._channel_count = int(channel_count)
            for context in self.contexts:
                if context.provider:
                    with context.provider.at():
                        context._reconcile()
                else:
                    context._reconcile()

    ### PUBLIC PROPERTIES ###

    @property
    def channel_count(self) -> int:
        return self._channel_count

    @property
    def contexts(self) -> Tuple[Context, ...]:
        return self._contexts

    @property
    def controllers(self) -> Tuple[Controller, ...]:
        return self._controllers

    @property
    def lock(self) -> RLock:
        return self._lock

    @property
    def parent(self) -> None:
        return None

    @property
    def primary_context(self) -> Optional[Context]:
        if not self.contexts:
            return None
        return self.contexts[0]

    @property
    def scenes(self) -> Tuple[Scene, ...]:
        return self._scenes

    @property
    def status(self):
        return self._status

    @property
    def transport(self) -> Transport:
        return self._transport
