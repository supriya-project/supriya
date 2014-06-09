# -*- encoding: utf-8 -*-
from supriya.tools.serverresponsetools.ServerResponse import ServerResponse


class QueryTreeSynthItem(ServerResponse):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_controls',
        '_node_id',
        '_synth_definition_name',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        node_id=None,
        synth_definition_name=None,
        controls=None,
        ):
        self._controls = controls
        self._node_id = node_id
        self._synth_definition_name = synth_definition_name

    ### PUBLIC PROPERTIES ###

    @property
    def controls(self):
        return self._controls

    @property
    def node_id(self):
        return self._node_id

    @property
    def synth_definition_name(self):
        return self._synth_definition_name
