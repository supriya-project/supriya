import logging
from contextlib import ExitStack, contextmanager
from types import MappingProxyType
from typing import Any, Dict, Mapping, Optional, Set, Union

from uqbar.containers import UniqueTreeTuple

import supriya.xdaw  # noqa
from supriya.commands import NodeQueryRequest
from supriya.enums import AddAction
from supriya.provider import (
    BusGroupProxy,
    BusProxy,
    NodeProxy,
    OscCallbackProxy,
    Provider,
    SynthProxy,
)
from supriya.querytree import QueryTreeGroup, QueryTreeSynth
from supriya.typing import Missing

logger = logging.getLogger("supriya.xdaw")


class ApplicationObject(UniqueTreeTuple):

    ### INITIALIZER ###

    def __init__(self, *, name=None):
        self._application: Optional["supriya.xdaw.Application"] = None
        UniqueTreeTuple.__init__(self, name=name)
        self._cached_state = self._get_state()

    ### SPECIAL METHODS ###

    def __str__(self):
        return "\n".join(
            [
                f"<{type(self).__name__}>",
                *(f"    {line}" for child in self for line in str(child).splitlines()),
            ]
        )

    ### PRIVATE METHODS ###

    def _append(self, node):
        self._mutate(slice(len(self), len(self)), [node])

    def _applicate(self, new_application):
        self._debug_tree(self, "Applicating", suffix=hex(id(new_application)))

    def _deapplicate(self, old_application):
        self._debug_tree(self, "Deapplicating", suffix=repr(None))

    @classmethod
    def _debug_tree(cls, node, prefix, suffix=None):
        parts = [
            (prefix + ":").ljust(15),
            ".." * node.depth,
            " " if node.depth else "",
            type(node).__name__,
            f"({node.name})" if node.name else "",
            f" ({suffix})" if suffix else "",
        ]
        logger.debug("".join(parts))

    def _get_state(self):
        index = None
        if self.parent:
            index = self.parent.index(self)
        return dict(application=self.application, parent=self.parent, index=index)

    def _get_state_difference(self, **kwargs):
        # self._debug_tree(self, "Reconciling")
        old_state = self._cached_state
        self._cached_state = new_state = self._get_state()
        difference = {}
        for key in old_state:
            if old_state[key] == new_state[key]:
                continue
            difference[key] = old_state[key], new_state[key]
        return difference

    def _reconcile(self, **kwargs):
        difference = self._get_state_difference()
        if "application" in difference:
            old_application, new_application = difference.pop("application")
            if old_application:
                self._deapplicate(old_application)
            if new_application:
                self._applicate(new_application)
            for child in self:
                child._set(application=new_application)

    def _remove(self, node):
        index = self.index(node)
        self._mutate(slice(index, index + 1), [])

    def _set(
        self,
        application: Optional[Union[Missing, "supriya.xdaw.Application"]] = Missing(),
        **kwargs,
    ):
        if not isinstance(application, Missing):
            self._application = application
        self._reconcile()

    def _set_items(self, new_items, old_items, start_index, stop_index):
        UniqueTreeTuple._set_items(self, new_items, old_items, start_index, stop_index)
        for item in new_items:
            item._set(application=self.application)
        for item in old_items:
            item._set(application=None)

    def _cleanup(self):
        pass

    ### PUBLIC METHODS ###

    @classmethod
    @contextmanager
    def lock(cls, objects, seconds=None):
        exit_stack = ExitStack()
        with exit_stack:
            for object_ in objects:
                if object_.application is not None:
                    exit_stack.enter_context(object_.application.lock)
            yield

    def rename(self, name):
        pass

    ### PUBLIC PROPERTIES ###

    @property
    def application(self) -> Optional["supriya.xdaw.Application"]:
        return self._application

    @property
    def cached_state(self) -> Mapping[str, Any]:
        return MappingProxyType(self._cached_state)

    @property
    def context(self) -> Optional["supriya.xdaw.Context"]:
        from supriya.xdaw import Context

        for parent in self.parentage:
            if isinstance(parent, Context):
                return parent
        return None

    @property
    def label(self):
        return self.name or type(self).__name__

    @property
    def provider(self):
        return None

    @property
    def transport(self):
        application = self.application
        if application is None:
            return None
        return application.transport


class Allocatable(ApplicationObject):

    ### INITIALIZER ###

    def __init__(self, *, channel_count=None, name=None):
        self._audio_bus_proxies: Dict[str, Union[BusProxy, BusGroupProxy]] = {}
        self._buffer_proxies = {}
        self._channel_count: Optional[int] = channel_count
        self._control_bus_proxies: Dict[str, Union[BusProxy, BusGroupProxy]] = {}
        self._is_active = True
        self._node_proxies: Dict[str, NodeProxy] = {}
        self._osc_callback_proxies: Dict[str, OscCallbackProxy] = {}
        self._provider: Optional[Provider] = None
        ApplicationObject.__init__(self, name=name)

    ### SPECIAL METHODS ###

    def __str__(self):
        node_proxy_id = int(self.node_proxy) if self.node_proxy is not None else "..."
        obj_name = self.name or type(self).__name__
        return "\n".join(
            [
                f"<{obj_name} [{node_proxy_id}]>",
                *(f"    {line}" for child in self for line in str(child).splitlines()),
            ]
        )

    ### PRIVATE METHODS ###

    def _activate(self):
        self._debug_tree(self, "Activating")
        self._is_active = True

    def _allocate(self, provider, target_node, add_action):
        self._debug_tree(
            self,
            "Allocating",
            suffix=f"{hex(id(provider))} {target_node!r} {add_action}",
        )

    def _deallocate(self, old_provider, *, dispose_only=False):
        self._debug_tree(self, "Deallocating", suffix=repr(None))
        node = self._node_proxies.pop("node", None)
        if node is not None and not dispose_only:
            node["gate"] = 0
        self._node_proxies.clear()
        for key, value in sorted(self._node_proxies.items()):
            if isinstance(value, SynthProxy):
                self._node_proxies.pop(key)["gate"] = 0
        while self._audio_bus_proxies:
            _, bus_proxy = self._audio_bus_proxies.popitem()
            bus_proxy.free()
        while self._buffer_proxies:
            _, buffer_proxy = self._buffer_proxies.popitem()
            buffer_proxy.free()
        while self._control_bus_proxies:
            _, bus_proxy = self._control_bus_proxies.popitem()
            bus_proxy.free()
        while self._osc_callback_proxies:
            _, osc_callback_proxy = self._osc_callback_proxies.popitem()
            osc_callback_proxy.unregister()

    def _deactivate(self):
        self._debug_tree(self, "Deactivating")
        self._is_active = False

    def _get_state(self):
        state = ApplicationObject._get_state(self)
        state.update(channel_count=self.effective_channel_count, provider=self.provider)
        return state

    def _move(self, target_node, add_action):
        self._debug_tree(
            self, "Moving", suffix=f"{target_node.identifier} {add_action}"
        )
        self.node_proxy.move(add_action=add_action, target_node=target_node)

    def _reallocate(self, difference):
        self._debug_tree(self, "Reallocating")

    def _reconcile(
        self,
        target_node: Optional[NodeProxy] = None,
        add_action: Optional[int] = None,
        dispose_only: bool = False,
        **kwargs,
    ):
        difference = self._get_state_difference()
        if "provider" in difference:
            old_provider, new_provider = difference.pop("provider")
            if old_provider:
                self._deallocate(old_provider, dispose_only=dispose_only)
                for child in self:
                    child._set(provider=None, dispose_only=True)
            if new_provider:
                for parameter in getattr(self, "parameters", {}).values():
                    parameter._preallocate(new_provider, self)
                self._allocate(new_provider, target_node, add_action)
                target_node, add_action = self.node_proxy, AddAction.ADD_TO_HEAD
                for child in self:
                    child._set(
                        provider=new_provider,
                        target_node=target_node,
                        add_action=add_action,
                    )
                    if isinstance(child, Allocatable) and child.node_proxy is not None:
                        target_node, add_action = child.node_proxy, AddAction.ADD_AFTER
            self._reconcile_dependents()
        elif self.provider:
            if "index" in difference or "parent" in difference:
                self._move(target_node, add_action)
            if "channel_count" in difference:
                self._reallocate(difference)
            for child in self:
                child._reconcile()
            self._reconcile_dependents()
        if "application" in difference:
            old_application, new_application = difference.pop("application")
            if old_application:
                self._deapplicate(old_application)
            if new_application:
                self._applicate(new_application)
            for child in self:
                child._set(application=new_application)

    def _reconcile_dependents(self):
        pass

    def _set(
        self,
        application: Optional[Union[Missing, "supriya.xdaw.Application"]] = Missing(),
        channel_count: Optional[Union[Missing, int]] = Missing(),
        provider: Optional[Union[Missing, Provider]] = Missing(),
        target_node: Optional[NodeProxy] = None,
        add_action: Optional[AddAction] = None,
        **kwargs,
    ):
        if not isinstance(application, Missing):
            self._application = application
            if application is None:
                provider = None
        if not isinstance(provider, Missing):
            self._provider = provider
        if not isinstance(channel_count, Missing):
            self._channel_count = channel_count
        self._reconcile(target_node=target_node, add_action=add_action, **kwargs)

    def _collect_for_cleanup(self, new_items, old_items):
        return []

    def _set_items(self, new_items, old_items, start_index, stop_index):
        target_node, add_action = self, AddAction.ADD_TO_HEAD
        if new_items:
            if start_index == len(self):
                target_node, add_action = self, AddAction.ADD_TO_TAIL
            elif start_index:
                while start_index and not isinstance(self[start_index], Allocatable):
                    start_index -= 1
                if start_index:
                    target_node, add_action = self[start_index], AddAction.ADD_AFTER
        to_cleanup = self._collect_for_cleanup(new_items, old_items)
        UniqueTreeTuple._set_items(self, new_items, old_items, start_index, stop_index)
        for item in new_items:
            item._set(
                application=self.application,
                provider=self.provider,
                target_node=target_node.node_proxy,
                add_action=add_action,
            )
            if isinstance(item, Allocatable) and item.node_proxy is not None:
                target_node, add_action = item, AddAction.ADD_AFTER
        for item in old_items:
            item._set(application=None, provider=None)
        for item in to_cleanup:
            item._cleanup()

    ### PUBLIC METHODS ###

    @classmethod
    @contextmanager
    def lock(cls, objects, seconds=None):
        exit_stack = ExitStack()
        with exit_stack:
            providers = set()
            for object_ in objects:
                if object_.application is not None:
                    exit_stack.enter_context(object_.application.lock)
                provider = getattr(object_, "provider", None)
                if provider is not None and provider not in providers:
                    exit_stack.enter_context(provider.at(seconds))
                    providers.add(provider)
            yield

    def query(self):
        if self.provider.server is None:
            raise ValueError
        query_tree = {}
        stack = [self.node_proxy.identifier]
        while stack:
            node_id = stack.pop()
            if node_id in query_tree:
                continue
            request = NodeQueryRequest(node_id)
            response = request.communicate(server=self.provider.server)
            if (response.next_node_id or -1) > 0:
                stack.append(response.next_node_id)
            if (response.head_node_id or -1) > 0:
                stack.append(response.head_node_id)
            if response.is_group:
                query_tree[node_id] = QueryTreeGroup.from_response(response)
            else:
                query_tree[node_id] = QueryTreeSynth.from_response(response)
            if response.parent_id in query_tree:
                query_tree[response.parent_id]._children += (query_tree[node_id],)
        query_tree_group = query_tree[self.node_proxy.identifier]
        return query_tree_group.annotate(self.provider.annotation_map)

    ### PUBLIC PROPERTIES ###

    @property
    def audio_bus_proxies(self) -> Mapping[str, Union[BusProxy, BusGroupProxy]]:
        return MappingProxyType(self._audio_bus_proxies)

    @property
    def buffer_proxies(self) -> Mapping[str, Any]:
        return MappingProxyType(self._buffer_proxies)

    @property
    def channel_count(self) -> Optional[int]:
        return self._channel_count

    @property
    def control_bus_proxies(self) -> Mapping[str, Union[BusProxy, BusGroupProxy]]:
        return MappingProxyType(self._control_bus_proxies)

    @property
    def effective_channel_count(self) -> int:
        for object_ in self.parentage:
            channel_count = getattr(object_, "channel_count", None)
            if channel_count:
                return channel_count
        return 2

    @property
    def is_active(self) -> bool:
        return self._is_active

    @property
    def node_proxies(self) -> Mapping[str, NodeProxy]:
        return MappingProxyType(self._node_proxies)

    @property
    def node_proxy(self) -> Optional[NodeProxy]:
        return self._node_proxies.get("node")

    @property
    def osc_callback_proxies(self) -> Mapping[str, OscCallbackProxy]:
        return MappingProxyType(self._osc_callback_proxies)

    @property
    def provider(self) -> Optional[Provider]:
        return self._provider


class Container(ApplicationObject):

    ### INITIALIZER ###

    def __init__(self, *, label=None):
        ApplicationObject.__init__(self)
        self._label = label

    ### SPECIAL METHODS ###

    def __str__(self):
        return "\n".join(
            [
                f"<{self.label}>",
                *(f"    {line}" for child in self for line in str(child).splitlines()),
            ]
        )

    @property
    def label(self):
        return self._label or type(self).__name__


class AllocatableContainer(Allocatable):

    ### INITIALIZER ###

    def __init__(
        self,
        target_node_name: str,
        add_action: int,
        *,
        label=None,
        target_node_parent: Optional[Allocatable] = None,
    ):
        Allocatable.__init__(self)
        self._target_node_name = str(target_node_name)
        self._add_action = AddAction.from_expr(add_action)
        self._label = label
        self._target_node_parent = target_node_parent

    ### SPECIAL METHODS ###

    def __str__(self):
        node_proxy_id = int(self.node_proxy) if self.node_proxy is not None else "..."
        return "\n".join(
            [
                f"<{self.label} [{node_proxy_id}]>",
                *(f"    {line}" for child in self for line in str(child).splitlines()),
            ]
        )

    ### PRIVATE METHODS ###

    def _allocate(self, provider, target_node, add_action):
        Allocatable._allocate(self, provider, target_node, add_action)
        parent = self.target_node_parent or self.parent
        target_node = parent.node_proxies[self.target_node_name]
        self._node_proxies["node"] = provider.add_group(
            target_node=target_node, add_action=self.add_action, name=self.label
        )

    ### PUBLIC PROPERTIES ###

    @property
    def add_action(self):
        return self._add_action

    @property
    def label(self):
        return self._label or type(self).__name__

    @property
    def target_node_name(self):
        return self._target_node_name

    @property
    def target_node_parent(self):
        return self._target_node_parent


class Mixer:
    def __init__(self):
        from .tracks import TrackObject

        self._soloed_tracks: Set[TrackObject] = set()
