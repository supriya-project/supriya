# -*- encoding: utf-8 -*-
from supriya.tools.responsetools.Response import Response


class QueryTreeSynthItem(Response):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_controls',
        '_node_id',
        '_synthdef_name',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        node_id=None,
        synthdef_name=None,
        controls=None,
        ):
        self._controls = controls
        self._node_id = node_id
        self._synthdef_name = synthdef_name

    ### PUBLIC PROPERTIES ###

    @property
    def controls(self):
        return self._controls

    @property
    def node_id(self):
        return self._node_id

    @property
    def synthdef_name(self):
        return self._synthdef_name
