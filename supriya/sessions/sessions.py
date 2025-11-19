import asyncio
import itertools
import logging
import re
from typing import TYPE_CHECKING, Iterable, Literal, Sequence

from ..contexts import AsyncServer
from ..enums import BootStatus
from ..osc import find_free_port
from ..scsynth import Options
from .components import Component
from .constants import Address, ChannelCount
from .specs import Artifacts, Spec

if TYPE_CHECKING:
    from .mixers import Mixer
    from .tracks import Track


logger = logging.getLogger(__name__)


# TODO: Session shouldn't be a Component because that assumes something
#       allocatable within a single context. We need a lower-level component
#       instead.
class Session(Component):
    """
    The top-level session component.

    Contains one or more contexts.

    Contains one or more mixers.

    Each mixer references one context.

    This supports running scsynth and supernova simultaneously via two mixers.
    """

    _PATH_REGEX = re.compile(r"^[a-z_]+\[\d+\](\.[a-z_]+\[\d+\])*$")
    _PATH_PART_REGEX = re.compile(r"^([a-z_]+)\[(\d+)\]$")

    def __init__(self) -> None:
        from .mixers import Mixer

        Component.__init__(self, id_=0)
        self._boot_future: asyncio.Future | None = None
        self._boot_status = BootStatus.OFFLINE
        self._channel_count: ChannelCount = 2
        self._global_artifacts_by_context: dict[AsyncServer, Artifacts] = {}
        self._global_specs_by_context: dict[AsyncServer, dict[Address, Spec]] = {}
        self._contexts: dict[AsyncServer, list[Mixer]] = {}
        self._lock = asyncio.Lock()
        self._mixers: dict[Mixer, AsyncServer] = {}
        self._next_id = 1
        self._quit_future: asyncio.Future | None = None
        self._soloed_tracks: set["Track"] = set()

    def __getitem__(self, key: str) -> "Component":
        if not isinstance(key, str):
            raise ValueError(key)
        elif not self._PATH_REGEX.match(key):
            raise ValueError(key)
        item: Component | Sequence[Component] = self
        for part in key.split("."):
            if not (match := self._PATH_PART_REGEX.match(part)):
                raise ValueError(key, part)
            name, index = match.groups()
            item = getattr(item, name)
            if index is not None:
                if not isinstance(item, Sequence):
                    raise ValueError(item, index)
                item = item[int(index)]
        if isinstance(item, Sequence):
            raise ValueError(item)
        return item

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.id} {self.boot_status.name}>"

    def _add_context(self, options: Options | None = None) -> AsyncServer:
        context = AsyncServer(options)
        self._contexts[context] = []
        self._global_artifacts_by_context[context] = Artifacts()
        self._global_specs_by_context[context] = {}
        return context

    def _add_mixer(self, context: AsyncServer, name: str | None) -> "Mixer":
        from .mixers import Mixer

        self._contexts.setdefault(context, []).append(
            mixer := Mixer(id_=self._get_next_id(), name=name, parent=self)
        )
        self._mixers[mixer] = context
        return mixer

    def _gather_annotations_by_context(
        self,
        annotation_style: Literal["nested", "numeric"] | None = "nested",
    ) -> dict[AsyncServer, dict[int, str]]:
        annotations: dict[AsyncServer, dict[int, str]] = {}
        for context, mixers in self._contexts.items():
            for mixer in mixers:
                annotations.setdefault(context, {}).update(
                    mixer._gather_annotations(annotation_style)
                )
        return annotations

    def _get_nested_address(self) -> Address:
        return "session"

    def _get_next_id(self) -> int:
        self._next_id = (next_id := self._next_id) + 1
        return next_id

    def _get_numeric_address(self) -> Address:
        return "session"

    async def _get_or_create_context(
        self, context: AsyncServer | None = None
    ) -> AsyncServer:
        if not self._contexts:
            context = self._add_context()
            if self._boot_status == BootStatus.ONLINE:
                await context.boot(port=find_free_port())
        if context is None:
            context = list(self._contexts)[0]
        if context not in self.contexts:
            raise ValueError(context)
        return context

    def _solo_track(
        self,
        *,
        exclusive: bool,
        track: "Track",
    ) -> None:
        # TODO: Can these be consolidated into a TrackSoloContext?
        self._soloed_tracks.add(track)
        if exclusive:
            for track_ in tuple(self._soloed_tracks):
                if track_ is track:
                    continue
                track_._set_soloed(soloed=False)

    def _solo_tracks(self, *, tracks: Iterable["Track"]) -> None:
        # TODO: Can these be consolidated into a TrackSoloContext?
        self._soloed_tracks.update(tracks)

    def _unsolo_tracks(self, *, tracks: Iterable["Track"]) -> None:
        # TODO: Can these be consolidated into a TrackSoloContext?
        self._soloed_tracks -= set(tracks)

    def _update_track_activation(self) -> None:
        from .tracks import Track

        tracks_to_update: list[Track] = []
        for track in self.walk(Track):
            assert isinstance(track, Track)
            if track._reconcile_activation():
                tracks_to_update.append(track)
        for context, tracks in itertools.groupby(
            tracks_to_update, lambda x: x._context
        ):
            if context is None:
                continue
            with context.at():
                for track in tracks:
                    track._apply_activation()

    async def add_context(self, options: Options | None = None) -> AsyncServer:
        """
        Add a synthesis context to the session.
        """
        async with self._lock:
            context = self._add_context(options)
            if self._boot_status == BootStatus.ONLINE:
                await context.boot(port=find_free_port())
            return context

    async def add_mixer(
        self, context: AsyncServer | None = None, name: str | None = None
    ) -> "Mixer":
        """
        Add a mixer to the session.
        """
        async with self._lock:
            context = await self._get_or_create_context(context)
            mixer = self._add_mixer(context=context, name=name)
            await mixer._reconcile(
                context=context,
                reconciling_components=[mixer],
                session=self,
            )
            return mixer

    async def boot(self) -> "Session":
        """
        Boot the session.

        Boots all contexts, and reconciles all mixers against them.
        """
        async with self._lock:
            # reset state
            # guard against concurrent boot / quits
            if self._boot_status == BootStatus.OFFLINE:
                self._quit_future = None
                self._boot_future = asyncio.get_running_loop().create_future()
                self._boot_status = BootStatus.BOOTING
                await asyncio.gather(
                    *[context.boot(port=find_free_port()) for context in self._contexts]
                )
                self._boot_status = BootStatus.ONLINE
                self._boot_future.set_result(True)
                for context, mixers in self._contexts.items():
                    for mixer in mixers:
                        await Component._reconcile(
                            context=context,
                            reconciling_components=[mixer],
                            session=self,
                        )
            elif self._boot_future is not None:  # BOOTING / ONLINE
                await self._boot_future
            else:  # NONREALTIME
                raise Exception(self._boot_status)
        return self

    async def delete_context(self, context: AsyncServer) -> None:
        """
        Delete a synthesis context from the session.

        Delete any mixers associated with that context.
        """
        async with self._lock:
            for mixer in self._contexts.pop(context):
                # Don't re-use Mixer.delete() because of re-entrancy
                await Component._reconcile(
                    context=None,
                    deleting_components=[mixer],
                    reconciling_components=[mixer],
                    session=self,
                )
            await context.quit()
            self._global_artifacts_by_context.pop(context)
            self._global_specs_by_context.pop(context)

    def dump_components(self) -> str:
        """
        Dump the sessions's component tree as a string representation.
        """
        indent = "    "
        parts = [repr(self)]
        for context, mixers in self._contexts.items():
            parts.append(indent + repr(context))
            for mixer in mixers:
                parts.extend((indent * 2) + line for line in mixer._dump_components())
        return "\n".join(parts)

    async def dump_tree(
        self,
        annotation_style: Literal["nested", "numeric"] | None = "nested",
        fallback_annotations: dict[AsyncServer, dict[int, str]] | None = None,
    ) -> str:
        """
        Dump the sessions's node tree, optionally annotated, as a string representation.
        """
        if self.boot_status != BootStatus.ONLINE:
            raise RuntimeError
        parts: list[str] = []
        for context, mixers in self._contexts.items():
            parts.append(repr(context))
            for mixer in mixers:
                for line in (
                    await mixer._dump_tree(
                        annotation_style=annotation_style,
                        fallback_annotations=(fallback_annotations or {}).get(context),
                    )
                ).splitlines():
                    parts.append(f"    {line}")
        return "\n".join(parts)

    async def quit(self) -> "Session":
        """
        Quit the session.

        Quit all running synthesis contexts.
        """
        async with self._lock:
            # guard against concurrent boot / quits
            if self._boot_status == BootStatus.ONLINE:
                self._boot_future = None
                self._quit_future = asyncio.get_running_loop().create_future()
                self._boot_status = BootStatus.QUITTING
                for context, mixers in self._contexts.items():
                    for mixer in mixers:
                        with context.at():
                            await Component._reconcile(
                                context=None,
                                reconciling_components=[mixer],
                                session=self,
                            )
                    self._global_artifacts_by_context[context].clear()
                    self._global_specs_by_context[context].clear()
                await asyncio.gather(*[context.quit() for context in self._contexts])
                self._boot_status = BootStatus.OFFLINE
                self._quit_future.set_result(True)
            elif self._quit_future is not None:  # QUITTING / OFFLINE
                await self._quit_future
            elif self._boot_status == BootStatus.OFFLINE:  # Never booted
                return self
            else:  # NONREALTIME
                raise Exception(self._boot_status)
        return self

    async def set_mixer_context(self, mixer: "Mixer", context: AsyncServer) -> None:
        """
        Set a mixer's associated synthesis context.
        """
        async with self._lock:
            if mixer not in self._mixers:
                raise ValueError(mixer)
            elif context not in self._contexts:
                raise ValueError(context)
            if mixer in self._contexts[context]:
                return
            self._contexts[self._mixers[mixer]].remove(mixer)
            if self._boot_status == BootStatus.ONLINE:
                await Component._reconcile(
                    context=context, reconciling_components=[mixer], session=self
                )
            self._contexts[context].append(mixer)
            self._mixers[mixer] = context

    async def sync(self) -> None:
        """
        Sync all synthesis contexts.
        """
        if self._boot_status != BootStatus.ONLINE:
            raise RuntimeError
        await asyncio.gather(*[context.sync() for context in self.contexts])

    @property
    def boot_status(self) -> BootStatus:
        """
        Get the boot boot_status of the session.
        """
        return self._boot_status

    @property
    def children(self) -> list[Component]:
        """
        Get the session's children.
        """
        return list(self._mixers)

    @property
    def contexts(self) -> list[AsyncServer]:
        """
        Get the session's contexts.
        """
        return list(self._contexts)

    @property
    def mixers(self) -> list["Mixer"]:
        """
        Get the session's mixers.
        """
        return list(self._mixers)
