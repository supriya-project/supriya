# -*- encoding: utf-8 -*-
import collections
from supriya.tools.responsetools.Response import Response


class QueryTreeSynth(Response, collections.Sequence):

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

    def __getitem__(self, item):
        return self._controls[item]

    def __len__(self):
        return len(self._controls)

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
        if self.controls:
            control_string = ', '.join(
                str(control) for control in self.controls
                )
            control_string = '\t' + control_string
            result.append(control_string)
        return result

    ### PUBLIC METHODS ###

    @classmethod
    def from_synth(cls, synth, include_controls=False):
        from supriya.tools import responsetools
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        assert isinstance(synth, servertools.Synth)
        node_id = synth.node_id
        synthdef_name = synth.synthdef
        if isinstance(synthdef_name, synthdeftools.StaticSynthDef):
            synthdef_name = synthdef_name.actual_name
        controls = []
        if include_controls:
            for control in synth.controls:
                control = responsetools.QueryTreeControl.from_control(control)
                controls.append(control)
        controls = tuple(controls)
        query_tree_synth = QueryTreeSynth(
            node_id=node_id,
            synthdef_name=synthdef_name,
            controls=controls,
            )
        return query_tree_synth

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
