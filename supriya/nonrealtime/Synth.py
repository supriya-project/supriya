import supriya.commands
import supriya.realtime
from supriya.nonrealtime.Node import Node


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
        supriya.realtime.AddAction.ADD_BEFORE,
        supriya.realtime.AddAction.ADD_AFTER,
        )

    ### INITIALIZER ###

    def __init__(
        self,
        session,
        session_id,
        duration=None,
        synthdef=None,
        start_offset=None,
        **synth_kwargs
    ):
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

    def __str__(self):
        return 'synth-{}'.format(self.session_id)

    ### PRIVATE METHODS ###

    def _to_request(self, action, id_mapping, **synth_kwargs):
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
        request = supriya.commands.SynthNewRequest(
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
