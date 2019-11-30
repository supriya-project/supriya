from uqbar.objects import new
import abc
import contextlib
import dataclasses
import pathlib
import re
import tempfile
from types import MappingProxyType
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
)

import supriya.nonrealtime  # noqa
import supriya.realtime  # noqa
from supriya import nonrealtime, realtime
from supriya.assets.synthdefs.default import default
from supriya.commands.ControlBusSetRequest import ControlBusSetRequest
from supriya.commands.GroupHeadRequest import GroupHeadRequest
from supriya.commands.GroupNewRequest import GroupNewRequest
from supriya.commands.GroupTailRequest import GroupTailRequest
from supriya.commands.MoveRequest import MoveRequest
from supriya.commands.NodeAfterRequest import NodeAfterRequest
from supriya.commands.NodeBeforeRequest import NodeBeforeRequest
from supriya.commands.NodeFreeRequest import NodeFreeRequest
from supriya.commands.NodeSetRequest import NodeSetRequest
from supriya.commands.RequestBundle import RequestBundle
from supriya.commands.SynthDefReceiveRequest import SynthDefReceiveRequest
from supriya.commands.SynthNewRequest import SynthNewRequest
from supriya.enums import AddAction, CalculationRate
from supriya.nonrealtime.Session import Session
from supriya.realtime.Server import Server
from supriya.synthdefs.SynthDef import SynthDef

# TODO: Implement BusProxy, integrate with BusGroupProxy


# @dataclasses.dataclass(frozen=True)
# class BufferProxy:
#    provider: "Provider"
#    channel_count: int = 1
#    frame_count: Optional[int] = None
#    file_path: Optional[str] = None
#    channel_indices: Optional[List[int]] = None
#    starting_frame: Optional[int] = None
#
#    def close(self):
#        pass
#
#    def free(self):
#        self.provider.free_buffer(self)
#
#    def normalize(self, new_maximum=1.0):
#        pass
#
#    def read(self, file_path, leave_open=False):
#        pass
#
#    def write(
#        self,
#        file_path,
#        frame_count=None,
#        header_format="aiff",
#        leave_open=False,
#        sample_format="int24",
#        starting_frame=None,
#    ):
#        pass


@dataclasses.dataclass(frozen=True)
class Proxy:
    provider: "Provider"


@dataclasses.dataclass(frozen=True)
class OscCallbackProxy(Proxy):
    provider: "Provider"
    identifier: Any

    def unregister(self):
        self.provider.unregister_osc_callback(self)


@dataclasses.dataclass(frozen=True)
class BusProxy(Proxy):
    calculation_rate: CalculationRate
    provider: "Provider"
    identifier: Union["supriya.nonrealtime.Bus.Bus", int]

    def __float__(self):
        return float(int(self))

    def __int__(self):
        if self.provider.server:
            return self.identifier
        elif self.provider.session:
            return self.provider.identifier.session_id

    def set_(self, value):
        self.provider.set_bus(self, value)

    def free(self):
        self.provider.free_bus(self)


@dataclasses.dataclass(frozen=True)
class BusGroupProxy(Proxy):
    calculation_rate: CalculationRate
    channel_count: int
    identifier: Union["supriya.nonrealtime.BusGroup.BusGroup", int]
    provider: "Provider"
    buses: Sequence["BusProxy"] = dataclasses.field(init=False)

    def __post_init__(self):
        if isinstance(self.identifier, int):
            bus_identifiers = range(
                self.identifier, self.identifier + self.channel_count
            )
        else:
            bus_identifiers = self.identifier[:]
        object.__setattr__(
            self,
            "buses",
            tuple(
                BusProxy(
                    calculation_rate=self.calculation_rate,
                    provider=self.provider,
                    identifier=bus_identifier,
                )
                for bus_identifier in bus_identifiers
            ),
        )

    def __float__(self):
        return float(int(self))

    def __getitem__(self, item):
        return self.buses[item]

    def __int__(self):
        if self.provider.server:
            return self.identifier
        elif self.provider.session:
            return self.provider.identifier.session_id

    def __len__(self):
        return self.channel_count

    def free(self):
        self.provider.free_bus_group(self)


@dataclasses.dataclass(frozen=True)
class NodeProxy(Proxy):
    identifier: Union["supriya.nonrealtime.Node.Node", int]
    provider: "Provider"

    def __float__(self):
        return float(int(self))

    def __int__(self):
        if self.provider.server:
            return self.identifier
        elif self.provider.session:
            return self.provider.identifier.session_id

    def __setitem__(self, key, value):
        self.provider.set_node(self, **{key: value})

    def add_group(
        self, *, add_action: int = AddAction.ADD_TO_HEAD, name: Optional[str] = None
    ) -> "GroupProxy":
        return self.provider.add_group(add_action=add_action, target_node=self)

    def add_synth(
        self,
        *,
        synthdef: SynthDef = None,
        add_action: int = AddAction.ADD_TO_HEAD,
        name: Optional[str] = None,
        **settings,
    ) -> "SynthProxy":
        return self.provider.add_synth(
            add_action=add_action, synthdef=synthdef, target_node=self, **settings
        )

    def as_move_request(
        self, add_action: AddAction, target_node: "NodeProxy"
    ) -> MoveRequest:
        request_classes: Dict[int, Type[MoveRequest]] = {
            AddAction.ADD_TO_HEAD: GroupHeadRequest,
            AddAction.ADD_TO_TAIL: GroupTailRequest,
            AddAction.ADD_BEFORE: NodeBeforeRequest,
            AddAction.ADD_AFTER: NodeAfterRequest,
        }
        request_class: Type[MoveRequest] = request_classes[add_action]
        return request_class(
            node_id_pairs=[request_class.NodeIdPair(int(self), int(target_node))]
        )

    def as_set_request(self, **settings):
        coerced_settings = {}
        for key, value in settings.items():
            if isinstance(value, (BusProxy, BusGroupProxy)):
                if value.calculation_rate == CalculationRate.AUDIO:
                    value = f"a{value.identifier}"
                else:
                    value = f"c{value.identifier}"
            coerced_settings[key] = value
        return NodeSetRequest(node_id=int(self), **coerced_settings)

    def dispose(self):
        self.provider.dispose(self)

    def free(self):
        self.provider.free_node(self)

    def move(self, add_action: AddAction, target_node: "NodeProxy"):
        self.provider.move_node(self, add_action, target_node)


@dataclasses.dataclass(frozen=True)
class GroupProxy(NodeProxy):
    identifier: Union["supriya.nonrealtime.Node.Node", int]
    provider: "Provider"

    def as_add_request(self, add_action, target_node):
        return GroupNewRequest(
            items=[
                GroupNewRequest.Item(
                    node_id=int(self.identifier),
                    add_action=add_action,
                    target_node_id=int(target_node),
                )
            ]
        )

    def as_free_request(self, force=False):
        return NodeFreeRequest(node_ids=[int(self)])


@dataclasses.dataclass(frozen=True)
class SynthProxy(NodeProxy):
    identifier: Union["supriya.nonrealtime.Node.Node", int]
    provider: "Provider"
    synthdef: SynthDef
    settings: Dict[str, Union[float, BusGroupProxy]]

    def as_add_request(self, add_action, target_node):
        synthdef = self.synthdef or default
        synthdef_kwargs = {key: float(value) for key, value in self.settings.items()}
        for _, parameter in synthdef.indexed_parameters:
            value = synthdef_kwargs.get(parameter.name)
            if value == parameter.value:
                synthdef_kwargs.pop(parameter.name)
        return SynthNewRequest(
            node_id=int(self.identifier),
            add_action=add_action,
            target_node_id=int(target_node),
            synthdef=synthdef,
            **synthdef_kwargs,
        )

    def as_free_request(self, force=False):
        if force or "gate" not in self.synthdef.parameters:
            return NodeFreeRequest(node_ids=[int(self)])
        return NodeSetRequest(node_id=int(self), gate=0)


@dataclasses.dataclass(frozen=True)
class ProviderMoment:
    provider: "Provider"
    seconds: float
    bus_settings: List[Tuple[BusProxy, float]]
    node_reorderings: List[Tuple[NodeProxy, AddAction, NodeProxy]]
    node_additions: List[Tuple[NodeProxy, AddAction, NodeProxy]]
    node_removals: List[NodeProxy]
    node_settings: List[Tuple[NodeProxy, Dict[str, Union[float, BusGroupProxy]]]]

    def __enter__(self):
        self.provider._moments.append(self)
        return self

    def __exit__(self, *args):
        self.provider._moments.pop()
        if not self.provider.server:
            return
        requests = []
        synthdefs = set()
        new_nodes = set()
        for node_proxy, add_action, target_node in self.node_additions:
            request = node_proxy.as_add_request(add_action, target_node)
            if isinstance(request, SynthNewRequest):
                if request.synthdef not in self.provider.server:
                    synthdefs.add(request.synthdef)
            requests.append(request)
            new_nodes.add(node_proxy.identifier)
        for node_proxy, add_action, target_node in self.node_reorderings:
            requests.append(node_proxy.as_move_request(add_action, target_node))
        for node_proxy, settings in self.node_settings:
            requests.append(node_proxy.as_set_request(**settings))
        for node_proxy in self.node_removals:
            requests.append(
                node_proxy.as_free_request(force=node_proxy.identifier in new_nodes)
            )
        if self.bus_settings:
            sorted_pairs = sorted(
                dict(
                    (int(bus_proxy.identifier), value)
                    for bus_proxy, value in self.bus_settings
                ).items()
            )
            request = ControlBusSetRequest(index_value_pairs=sorted_pairs)
            requests.append(request)
        if not requests:
            return
        if synthdefs:
            request_bundle = RequestBundle(
                timestamp=self.seconds,
                contents=[
                    SynthDefReceiveRequest(
                        synthdefs=sorted(synthdefs, key=lambda x: x.actual_name),
                        callback=RequestBundle(contents=requests),
                    )
                ],
            )
            # check bundle size, write synthdefs to disk and do /d_load
            if len(request_bundle.to_datagram(with_placeholders=True)) > 8192:
                directory_path = pathlib.Path(tempfile.mkdtemp())
                for synthdef in synthdefs:
                    name = synthdef.anonymous_name
                    if synthdef.name:
                        name += "-" + re.sub(r"[^\w]", "-", synthdef.name)
                    file_name = "{}.scsyndef".format(name)
                    synthdef_path = directory_path / file_name
                    synthdef_path.write_bytes(synthdef.compile())
                request_bundle = RequestBundle(
                    timestamp=self.seconds,
                    contents=[
                        supriya.commands.SynthDefLoadDirectoryRequest(
                            directory_path=directory_path,
                            callback=RequestBundle(contents=requests),
                        )
                    ],
                )
        else:
            request_bundle = RequestBundle(timestamp=self.seconds, contents=requests)
        try:
            self.provider.server.send_message(request_bundle)
        except OSError:
            messages = request_bundle.contents
            if synthdefs:
                synthdef_message = messages[0]
                messages = synthdef_message.callback.contents or []
                synthdef_message = new(synthdef_message, callback=None)
                synthdef_message.communicate(sync=True, server=self.provider.server)
            for message in messages:
                self.provider.server.send_message(message)
        for synthdef in synthdefs:
            synthdef._register_with_local_server(server=self.provider.server)


class Provider(metaclass=abc.ABCMeta):
    """
    Provides limited realtime/non-realtime compatibility layer.
    """

    ### INITIALIZER ###

    def __init__(self):
        self._moments: List[ProviderMoment] = []
        self._server = None
        self._session = None
        self._annotation_map: Dict[
            Union["supriya.nonrealtime.Node.Node", int], str
        ] = {}

    ### PUBLIC METHODS ###

    #    @abc.abstractmethod
    #    def add_buffer(self):
    #        raise NotImplementedError

    @abc.abstractmethod
    def add_bus(self, calculation_rate=CalculationRate.CONTROL) -> BusProxy:
        raise NotImplementedError

    @abc.abstractmethod
    def add_bus_group(
        self, channel_count=1, calculation_rate=CalculationRate.CONTROL
    ) -> BusGroupProxy:
        raise NotImplementedError

    @abc.abstractmethod
    def add_group(
        self,
        *,
        target_node=None,
        add_action=AddAction.ADD_TO_HEAD,
        name: Optional[str] = None,
    ) -> GroupProxy:
        raise NotImplementedError

    @abc.abstractmethod
    def add_synth(
        self,
        *,
        synthdef: SynthDef = None,
        target_node=None,
        add_action=AddAction.ADD_TO_HEAD,
        name: Optional[str] = None,
        **settings,
    ) -> SynthProxy:
        raise NotImplementedError

    @abc.abstractmethod
    def boot(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def dispose(self, node_proxy: NodeProxy):
        raise NotImplementedError

    #    @abc.abstractmethod
    #    def free_buffer(self, buffer_proxy):
    #        raise NotImplementedError

    @abc.abstractmethod
    def free_bus(self, bus_proxy: BusProxy):
        raise NotImplementedError

    @abc.abstractmethod
    def free_bus_group(self, bus_group_proxy: BusGroupProxy):
        raise NotImplementedError

    @abc.abstractmethod
    def free_node(self, node_proxy: NodeProxy):
        raise NotImplementedError

    @abc.abstractmethod
    def move_node(
        self, node_proxy: NodeProxy, add_action: AddAction, target_node: NodeProxy
    ):
        raise NotImplementedError

    @abc.abstractmethod
    def set_bus(self, bus_proxy: BusProxy, value: float):
        raise NotImplementedError

    @abc.abstractmethod
    def set_node(self, node_proxy: NodeProxy, **settings):
        raise NotImplementedError

    @contextlib.contextmanager
    def at(self, seconds=None):
        provider_moment = ProviderMoment(
            provider=self,
            seconds=seconds,
            bus_settings=[],
            node_additions=[],
            node_removals=[],
            node_reorderings=[],
            node_settings=[],
        )
        exit_stack = contextlib.ExitStack()
        with exit_stack:
            exit_stack.enter_context(provider_moment)
            if self.session:
                exit_stack.enter_context(self.session.at(seconds or 0))
            yield provider_moment

    @classmethod
    def from_context(cls, context) -> "Provider":
        if isinstance(context, Session):
            return NonrealtimeProvider(context)
        elif isinstance(context, Server):
            return RealtimeProvider(context)
        raise ValueError("Unknown context")

    @classmethod
    def nonrealtime(cls) -> "NonrealtimeProvider":
        session = Session()
        return cast("NonrealtimeProvider", cls.from_context(session))

    @abc.abstractmethod
    def quit(self):
        raise NotImplementedError

    @classmethod
    def realtime(
        cls, scsynth_path=None, options=None, port=None, **kwargs
    ) -> "RealtimeProvider":
        server = Server(port=port)
        server.boot(scsynth_path=scsynth_path, options=options, **kwargs)
        return cast("RealtimeProvider", cls.from_context(server))

    @abc.abstractmethod
    def register_osc_callback(
        self, pattern: Tuple[Union[str, float], ...], procedure: Callable
    ) -> OscCallbackProxy:
        raise NotImplementedError

    @abc.abstractmethod
    def unregister_osc_callback(self, proxy: OscCallbackProxy):
        raise NotImplementedError

    ### PUBLIC PROPERTIES ###

    @property
    def annotation_map(self) -> Mapping[int, str]:
        return MappingProxyType(self._annotation_map)

    @property
    def moment(self) -> Optional[ProviderMoment]:
        if self._moments:
            return self._moments[0]
        return None

    @property
    def server(self) -> Server:
        return self._server

    @property
    def session(self) -> Session:
        return self._session


class NonrealtimeProvider(Provider):

    ### INITIALIZER ###

    def __init__(self, session):
        if not isinstance(session, Session):
            raise ValueError(f"Expected session, got {session}")
        Provider.__init__(self)
        self._session = session

    ### PRIVATE METHODS ###

    def _resolve_target_node(self, target_node) -> nonrealtime.Node:
        if target_node is None:
            target_node = self.session.root_node
        elif isinstance(target_node, NodeProxy):
            target_node = target_node.identifier
        return target_node

    ### PUBLIC METHODS ###

    #    def add_buffer(self) -> BufferProxy:
    #        if not self.moment:
    #            raise ValueError("No current moment")
    #        return BufferProxy(provider=self)

    def add_bus(self, calculation_rate=CalculationRate.CONTROL) -> BusProxy:
        if not self.moment:
            raise ValueError("No current moment")
        calculation_rate = CalculationRate.from_expr(calculation_rate)
        if calculation_rate not in (CalculationRate.AUDIO, CalculationRate.CONTROL):
            raise ValueError(f"Invalid calculation rate: {calculation_rate!r}")
        identifier = self.session.add_bus(calculation_rate=calculation_rate)
        return BusProxy(
            calculation_rate=calculation_rate, identifier=identifier, provider=self
        )

    def add_bus_group(
        self, channel_count=1, calculation_rate=CalculationRate.CONTROL
    ) -> BusGroupProxy:
        if not self.moment:
            raise ValueError("No current moment")
        calculation_rate = CalculationRate.from_expr(calculation_rate)
        if calculation_rate not in (CalculationRate.AUDIO, CalculationRate.CONTROL):
            raise ValueError(f"Invalid calculation rate: {calculation_rate!r}")
        if channel_count < 1:
            raise ValueError(f"Channel-count must be positive, non-zero integer")
        identifier = self.session.add_bus_group(
            bus_count=channel_count, calculation_rate=calculation_rate
        )
        return BusGroupProxy(
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            identifier=identifier,
            provider=self,
        )

    def add_group(
        self,
        *,
        target_node=None,
        add_action=AddAction.ADD_TO_HEAD,
        name: Optional[str] = None,
    ) -> GroupProxy:
        if not self.moment:
            raise ValueError("No current moment")
        identifier = self._resolve_target_node(target_node).add_group(
            add_action=add_action
        )
        proxy = GroupProxy(identifier=identifier, provider=self)
        return proxy

    def add_synth(
        self,
        *,
        synthdef: SynthDef = None,
        target_node=None,
        add_action=AddAction.ADD_TO_HEAD,
        name: Optional[str] = None,
        **settings,
    ) -> SynthProxy:
        if not self.moment:
            raise ValueError("No current moment")
        sanitized_settings = {}
        for key, value in settings.items():
            if isinstance(value, (BusProxy, BusGroupProxy)):
                value = value.identifier
            sanitized_settings[key] = value
        identifier = self._resolve_target_node(target_node).add_synth(
            add_action=add_action, synthdef=synthdef, **sanitized_settings
        )
        proxy = SynthProxy(
            identifier=identifier,
            provider=self,
            synthdef=synthdef or default,
            settings=settings,
        )
        return proxy

    #    def free_buffer(self, buffer_: BufferProxy):
    #        if not self.moment:
    #            raise ValueError("No current moment")

    def boot(self, **kwargs):
        pass  # no-op

    def dispose(self, node_proxy: NodeProxy):
        if not self.moment:
            raise ValueError("No current moment")
        return  # This is currently a no-op

    def free_bus(self, bus: BusProxy):
        if not self.moment:
            raise ValueError("No current moment")
        return  # This is currently a no-op

    def free_bus_group(self, bus_group: BusGroupProxy):
        if not self.moment:
            raise ValueError("No current moment")
        return  # This is currently a no-op

    def free_node(self, node_proxy: NodeProxy):
        if not self.moment:
            raise ValueError("No current moment")
        cast(nonrealtime.Node, node_proxy.identifier).free()

    def move_node(
        self,
        node_proxy: NodeProxy,
        add_action: AddAction,
        target_node: Union[NodeProxy, nonrealtime.Node],
    ):
        if not self.moment:
            raise ValueError("No current moment")
        self._resolve_target_node(target_node).move_node(
            node_proxy.identifier, add_action=add_action
        )

    def set_bus(self, bus_proxy: BusProxy, value: float):
        if not self.moment:
            raise ValueError("No current moment")
        elif bus_proxy.calculation_rate != CalculationRate.CONTROL:
            raise ValueError("Can only set control-rate buses")
        cast(nonrealtime.Bus, bus_proxy.identifier).set_(value)

    def set_node(self, node_proxy: NodeProxy, **settings):
        if not self.moment:
            raise ValueError("No current moment")
        for key, value in settings.items():
            if isinstance(value, (BusProxy, BusGroupProxy)):
                value = value.identifier
            cast(nonrealtime.Node, node_proxy.identifier)[key] = value

    def quit(self):
        pass  # no-op

    def register_osc_callback(
        self, pattern: Tuple[Union[str, float], ...], procedure: Callable
    ) -> OscCallbackProxy:
        return OscCallbackProxy(provider=self, identifier=None)

    def unregister_osc_callback(self, proxy: OscCallbackProxy):
        pass  # no-op


class RealtimeProvider(Provider):

    ### INITIALIZER ###

    def __init__(self, server):
        if not isinstance(server, Server):
            raise ValueError(f"Expected Server, got {server}")
        Provider.__init__(self)
        self._server = server

    ### PRIVATE METHODS ###

    def _resolve_target_node(self, target_node):
        if target_node is None:
            target_node = self.server.default_group
        return target_node

    ### PUBLIC METHODS ###

    #    def add_buffer(self) -> BufferProxy:
    #        if not self.moment:
    #            raise ValueError("No current moment")
    #        return BufferProxy(provider=self)

    def add_bus(self, calculation_rate=CalculationRate.CONTROL) -> BusProxy:
        if not self.moment:
            raise ValueError("No current moment")
        calculation_rate = CalculationRate.from_expr(calculation_rate)
        if calculation_rate not in (CalculationRate.AUDIO, CalculationRate.CONTROL):
            raise ValueError(f"Invalid calculation rate: {calculation_rate!r}")
        allocator = realtime.Bus._get_allocator(calculation_rate, server=self.server)
        identifier = allocator.allocate(1)
        return BusProxy(
            calculation_rate=calculation_rate, identifier=identifier, provider=self
        )

    def add_bus_group(
        self, channel_count=1, calculation_rate=CalculationRate.CONTROL
    ) -> BusGroupProxy:
        if not self.moment:
            raise ValueError("No current moment")
        calculation_rate = CalculationRate.from_expr(calculation_rate)
        if calculation_rate not in (CalculationRate.AUDIO, CalculationRate.CONTROL):
            raise ValueError(f"Invalid calculation rate: {calculation_rate!r}")
        if channel_count < 1:
            raise ValueError(f"Channel-count must be positive, non-zero integer")
        allocator = realtime.Bus._get_allocator(calculation_rate, server=self.server)
        identifier = allocator.allocate(channel_count)
        if identifier is None:
            raise RuntimeError
        return BusGroupProxy(
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            identifier=identifier,
            provider=self,
        )

    def add_group(
        self,
        *,
        target_node=None,
        add_action=AddAction.ADD_TO_HEAD,
        name: Optional[str] = None,
    ) -> GroupProxy:
        if not self.moment:
            raise ValueError("No current moment")
        target_node = self._resolve_target_node(target_node)
        identifier = self.server.node_id_allocator.allocate_node_id(1)
        proxy = GroupProxy(identifier=identifier, provider=self)
        self.moment.node_additions.append((proxy, add_action, target_node))
        if name:
            self._annotation_map[identifier] = name
        return proxy

    def add_synth(
        self,
        *,
        synthdef: SynthDef = None,
        target_node=None,
        add_action=AddAction.ADD_TO_HEAD,
        name: Optional[str] = None,
        **settings,
    ) -> SynthProxy:
        if not self.moment:
            raise ValueError("No current moment")
        target_node = self._resolve_target_node(target_node)
        identifier = self.server.node_id_allocator.allocate_node_id(1)
        proxy = SynthProxy(
            identifier=identifier,
            provider=self,
            synthdef=synthdef or default,
            settings=settings,
        )
        self.moment.node_additions.append((proxy, add_action, target_node))
        if name:
            self._annotation_map[identifier] = name
        return proxy

    def boot(self, **kwargs):
        self.server.boot(**kwargs)

    #    def free_buffer(self, buffer_: BufferProxy):
    #        if not self.moment:
    #            raise ValueError("No current moment")

    def dispose(self, node_proxy: NodeProxy):
        if not self.moment:
            raise ValueError("No current moment")
        return  # This is currently a no-op

    def free_bus(self, bus_proxy: BusProxy):
        if not self.moment:
            raise ValueError("No current moment")
        allocator = realtime.Bus._get_allocator(
            bus_proxy.calculation_rate, server=self.server
        )
        allocator.free(cast(int, bus_proxy.identifier))

    def free_bus_group(self, bus_group_proxy: BusGroupProxy):
        if not self.moment:
            raise ValueError("No current moment")
        allocator = realtime.Bus._get_allocator(
            bus_group_proxy.calculation_rate, server=self.server
        )
        allocator.free(cast(int, bus_group_proxy.identifier))

    def free_node(self, node_proxy: NodeProxy):
        if not self.moment:
            raise ValueError("No current moment")
        self.moment.node_removals.append(node_proxy)
        self._annotation_map.pop(node_proxy.identifier, None)

    def move_node(
        self, node_proxy: NodeProxy, add_action: AddAction, target_node: NodeProxy
    ):
        if not self.moment:
            raise ValueError("No current moment")
        target_node = self._resolve_target_node(target_node)
        self.moment.node_reorderings.append((node_proxy, add_action, target_node))

    def quit(self):
        self.server.quit()

    def set_bus(self, bus_proxy: BusProxy, value: float):
        if not self.moment:
            raise ValueError("No current moment")
        elif bus_proxy.calculation_rate != CalculationRate.CONTROL:
            raise ValueError("Can only set control-rate buses")
        self.moment.bus_settings.append((bus_proxy, value))

    def set_node(self, node_proxy: NodeProxy, **settings):
        if not self.moment:
            raise ValueError("No current moment")
        self.moment.node_settings.append((node_proxy, settings))

    def register_osc_callback(
        self, pattern: Tuple[Union[str, float], ...], procedure: Callable
    ) -> OscCallbackProxy:
        identifier = self.server.osc_io.register(pattern=pattern, procedure=procedure)
        return OscCallbackProxy(provider=self, identifier=identifier)

    def unregister_osc_callback(self, proxy: OscCallbackProxy):
        self.server.osc_io.unregister(proxy.identifier)
