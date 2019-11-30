import enum
import time
from threading import RLock
from typing import Optional, Tuple

from uqbar.containers import UniqueTreeTuple

from supriya.nonrealtime.Session import Session
from supriya.osc import OscIO
from supriya.provider import Provider

from .bases import Container
from .clips import Scene
from .contexts import Context
from .transports import Transport


class Application(UniqueTreeTuple):

    ### CLASS VARIABLES ###

    class Status(enum.IntEnum):
        OFFLINE = 0
        REALTIME = 1
        NONREALTIME = 2

    ### INITIALIZER ###

    def __init__(self, channel_count=2):
        UniqueTreeTuple.__init__(self)
        self._channel_count = int(channel_count)
        self._contexts = Container(label="Contexts")
        self._lock = RLock()
        self._scenes: Tuple[Scene, ...] = ()
        self._status = self.Status.OFFLINE
        self._transport = Transport()
        self._mutate(slice(None), [self._transport, self._contexts])
        self._contexts._application = self
        self._transport._application = self

    ### SPECIAL METHODS ###

    def __str__(self):
        lines = [f"<{type(self).__name__} {hex(id(self))}>"]
        for child in self:
            for line in str(child).splitlines():
                lines.append(f"    {line}")
        return "\n".join(lines)

    ### PUBLIC METHODS ###

    def add_context(self, name=None):
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

    def add_scene(self):
        return Scene()

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

    @classmethod
    def new(cls):
        application = cls()
        context = application.add_context()
        for _ in range(4):
            context.add_track()
        for _ in range(8):
            application.add_scene()
        return application

    def quit(self):
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