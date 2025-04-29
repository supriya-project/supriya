import asyncio
import logging
import re
from typing import TYPE_CHECKING, Sequence

from ..clocks import AsyncClock
from ..contexts import AsyncServer
from ..enums import BootStatus
from ..osc import find_free_port
from ..scsynth import Options
from ..ugens import SynthDef
from .components import Address, ChannelCount, Component

if TYPE_CHECKING:
    from .mixers import Mixer


logger = logging.getLogger(__name__)


class Session(Component):
    """
    Top-level object.

    Contains one transport.

    Contains one or more contexts.

    Contains one or more mixers.

    Each mixer references one context.

    This supports running scsynth and supernova simultaneously via two mixers.
    """

    _PATH_REGEX = re.compile(r"^[a-z_]+(\[\d+\])?(\.[a-z_]+(\[\d+\])?)*$")
    _PATH_PART_REGEX = re.compile(r"^([a-z_]+)(\[(\d+)\])?$")

    def __init__(self) -> None:
        from .mixers import Mixer

        super().__init__(session=self)
        self._boot_future: asyncio.Future | None = None
        self._channel_count: ChannelCount = 2
        self._clock = AsyncClock()
        self._contexts: dict[AsyncServer, list[Mixer]] = {}
        self._lock = asyncio.Lock()
        self._mixers: dict[Mixer, AsyncServer] = {}
        self._quit_future: asyncio.Future | None = None
        self._status = BootStatus.OFFLINE
        self._synthdefs: dict[AsyncServer, set[SynthDef]] = {}
        # add initial context and mixer

    def __getitem__(self, key: str) -> "Component":
        if not isinstance(key, str):
            raise ValueError(key)
        elif not self._PATH_REGEX.match(key):
            raise ValueError(key)
        item: Component | Sequence[Component] = self
        for part in key.split("."):
            if not (match := self._PATH_PART_REGEX.match(part)):
                raise ValueError(key, part)
            name, _, index = match.groups()
            item = getattr(item, name)
            if index is not None:
                if not isinstance(item, Sequence):
                    raise ValueError(item, index)
                item = item[int(index)]
        if isinstance(item, Sequence):
            raise ValueError(item)
        return item

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self._id}>"

    def __str__(self) -> str:
        parts: list[str] = [f"<{type(self).__name__} status={self.status.name}>"]
        for context, mixers in self._contexts.items():
            parts.append(
                f"    <{type(context).__name__} address={context.options.ip_address}:{context.options.port}>"
            )
            for mixer in mixers:
                parts.extend("        " + line for line in str(mixer).splitlines())
        return "\n".join(parts)

    def _add_context(self, options: Options | None = None) -> AsyncServer:
        context = AsyncServer(options)
        self._contexts[context] = []
        self._synthdefs[context] = set()
        return context

    def _get_next_id(self) -> int:
        self._next_id = (next_id := getattr(self, "_next_id", 0)) + 1
        return next_id

    async def add_context(self, options: Options | None = None) -> AsyncServer:
        async with self._lock:
            context = self._add_context(options)
            if self._status == BootStatus.ONLINE:
                await context.boot(port=find_free_port())
            return context

    async def add_mixer(
        self, context: AsyncServer | None = None, name: str | None = None
    ) -> "Mixer":
        from .mixers import Mixer

        async with self._lock:
            if not self._contexts:
                context = self._add_context()
                if self._status == BootStatus.ONLINE:
                    await context.boot(port=find_free_port())
            if context is None:
                context = list(self._contexts)[0]
            if context not in self.contexts:
                raise ValueError(context)
            self._contexts.setdefault(context, []).append(
                mixer := Mixer(name=name, parent=self, session=self._session)
            )
            self._mixers[mixer] = context
            if self._status == BootStatus.ONLINE:
                await mixer._allocate_deep(context=context)
            return mixer

    async def boot(self) -> None:
        async with self._lock:
            # reset state
            for set_ in self._synthdefs.values():
                set_.clear()
            # guard against concurrent boot / quits
            if self._status == BootStatus.OFFLINE:
                self._quit_future = None
                self._boot_future = asyncio.get_running_loop().create_future()
                self._status = BootStatus.BOOTING
                await asyncio.gather(
                    *[context.boot(port=find_free_port()) for context in self._contexts]
                )
                self._status = BootStatus.ONLINE
                self._boot_future.set_result(True)
                for context, mixers in self._contexts.items():
                    for mixer in mixers:
                        await mixer._allocate_deep(context=context)
            elif self._boot_future is not None:  # BOOTING / ONLINE
                await self._boot_future
            else:  # NONREALTIME
                raise Exception(self._status)

    async def delete_context(self, context: AsyncServer) -> None:
        async with self._lock:
            for mixer in self._contexts.pop(context):
                await mixer.delete()
            await context.quit()

    def dump_components(self) -> str:
        indent = "    "
        parts = [repr(self)]
        for context, mixers in self._contexts.items():
            parts.append(indent + repr(context))
            for mixer in mixers:
                parts.extend((indent * 2) + line for line in mixer._dump_components())
        return "\n".join(parts)

    async def dump_tree(self, annotated: bool = True) -> str:
        if self.status != BootStatus.ONLINE:
            raise RuntimeError
        parts: list[str] = []
        for context, mixers in self._contexts.items():
            parts.append(repr(context))
            for mixer in mixers:
                for line in (await mixer.dump_tree(annotated)).splitlines():
                    parts.append(f"    {line}")
        return "\n".join(parts)

    async def quit(self) -> None:
        async with self._lock:
            # guard against concurrent boot / quits
            if self._status == BootStatus.ONLINE:
                self._boot_future = None
                self._quit_future = asyncio.get_running_loop().create_future()
                self._status = BootStatus.QUITTING
                for context, mixers in self._contexts.items():
                    for mixer in mixers:
                        with context.at():
                            mixer._deallocate_deep()
                await asyncio.gather(*[context.quit() for context in self._contexts])
                self._status = BootStatus.OFFLINE
                self._quit_future.set_result(True)
            elif self._quit_future is not None:  # QUITTING / OFFLINE
                await self._quit_future
            elif self._status == BootStatus.OFFLINE:  # Never booted
                return
            else:  # NONREALTIME
                raise Exception(self._status)

    async def set_mixer_context(self, mixer: "Mixer", context: AsyncServer) -> None:
        async with self._lock:
            if mixer not in self._mixers:
                raise ValueError(mixer)
            elif context not in self._contexts:
                raise ValueError(context)
            if mixer in self._contexts[context]:
                return
            self._contexts[self._mixers[mixer]].remove(mixer)
            async with mixer._lock:
                mixer._deallocate_deep()
                if self._status == BootStatus.ONLINE:
                    await mixer._allocate_deep(context=context)
                self._contexts[context].append(mixer)
                self._mixers[mixer] = context

    async def sync(self) -> None:
        if self._status != BootStatus.ONLINE:
            raise RuntimeError
        await asyncio.gather(*[context.sync() for context in self.contexts])

    @property
    def address(self) -> Address:
        return "session"

    @property
    def children(self) -> list[Component]:
        return list(self._mixers)

    @property
    def contexts(self) -> list[AsyncServer]:
        return list(self._contexts)

    @property
    def mixers(self) -> list["Mixer"]:
        return list(self._mixers)

    @property
    def status(self) -> BootStatus:
        return self._status
