# -*- encoding: utf-8 -*-
from supriya.tools import requesttools
from supriya.tools import servertools
from supriya.tools.nonrealtimetools.Node import Node


class Synth(Node):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_synthdef',
        '_synth_kwargs',
        )

    _valid_add_actions = (
        servertools.AddAction.ADD_AFTER,
        servertools.AddAction.ADD_BEFORE,
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

    ### PUBLIC METHODS ###

    def to_request(self, action, id_mapping, **synth_kwargs):
        from supriya.tools import nonrealtimetools
        source_id = id_mapping[action.source]
        target_id = id_mapping[action.target]
        add_action = action.action
        prototype = (nonrealtimetools.Bus, nonrealtimetools.BusGroup)
        for key, value in synth_kwargs.items():
            if isinstance(value, prototype):
                bus_id = id_mapping[value]
                synth_kwargs[key] = value.get_map_symbol(bus_id)
        request = requesttools.SynthNewRequest(
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
