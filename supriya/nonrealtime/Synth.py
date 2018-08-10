import supriya.realtime
from supriya.commands import SynthNewRequest
from supriya.nonrealtime.Node import Node
from supriya.nonrealtime.SessionObject import SessionObject
from supriya.nonrealtime.NodeAction import NodeAction
from typing import Dict, Optional


class Synth(Node):
    """
    A non-realtime synth.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Session Objects'

    __slots__ = (
        '_synthdef',
        '_synth_kwargs',
        )

    _valid_add_actions = (
        supriya.AddAction.ADD_BEFORE,
        supriya.AddAction.ADD_AFTER,
        )

    ### INITIALIZER ###

    def __init__(
        self,
        session,
        session_id: int,
        duration: float=None,
        synthdef=None,
        start_offset: float=None,
        **synth_kwargs
    ) -> None:
        if synthdef is None:
            synthdef = supriya.assets.synthdefs.default
        Node.__init__(
            self,
            session,
            session_id,
            duration=duration,
            start_offset=start_offset,
            )
        self._synthdef = synthdef
        self._synth_kwargs = synth_kwargs

    ### SPECIAL METHODS ###

    def __str__(self) -> str:
        return 'synth-{}'.format(self.session_id)

    ### PRIVATE METHODS ###

    def _get_at_offset(
        self,
        offset: float,
        item: str,
    ) -> Optional[float]:
        default = self.synthdef.parameters[item].value
        default = self._synth_kwargs.get(item, default)
        return super()._get_at_offset(offset=offset, item=item) or default

    def _to_request(
        self,
        action: NodeAction,
        id_mapping: Dict[SessionObject, int],
        **synth_kwargs,
    ) -> SynthNewRequest:
        import supriya.nonrealtime
        source_id = id_mapping[action.source]
        target_id = id_mapping[action.target]
        add_action = action.action
        bus_prototype = (
            supriya.nonrealtime.Bus,
            supriya.nonrealtime.BusGroup,
            )
        buffer_prototype = (
            supriya.nonrealtime.Buffer,
            supriya.nonrealtime.BufferGroup,
            )
        #nonmapping_keys = ['out']
        for key, value in synth_kwargs.items():
            if isinstance(value, bus_prototype):
                bus_id = id_mapping[value]
                #if key not in nonmapping_keys:
                #    value = value.get_map_symbol(bus_id)
                #else:
                #    value = bus_id
                value = bus_id
                synth_kwargs[key] = value
            elif isinstance(value, buffer_prototype):
                synth_kwargs[key] = id_mapping[value]
        request = SynthNewRequest(
            add_action=add_action,
            node_id=source_id,
            synthdef=self.synthdef.anonymous_name,
            target_node_id=target_id,
            **synth_kwargs
            )
        return request

    ### PUBLIC PROPERTIES ###

    @property
    def synthdef(self):
        return self._synthdef

    @property
    def synth_kwargs(self):
        return self._synth_kwargs.copy()
