# -*- encoding: utf-8 -*-
from supriya.tools.responsetools.Response import Response


class QueryTreeSynth(Response):

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

    ### SPECIAL METHODS ###

    def __str__(self):
        result = self._get_str_format_pieces()
        result = '\n'.join(result)
        return result

    ### PRIVATE METHODS ###

    def _get_str_format_pieces(self):
        result = []
        synth_string = '{} {}'.format(
            self.node_id,
            self.synthdef_name,
            )
        result.append(synth_string)
        control_string = ', '.join(
            str(control) for control in self.controls
            )
        control_string = '\t' + control_string
        result.append(control_string)
        return result

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
