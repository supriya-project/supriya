# -*- encoding: utf-8 -*-
import collections
from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class QueryTreeSynth(SupriyaValueObject, collections.Sequence):

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

    @classmethod
    def _from_nrt_synth(cls, state, node, include_controls=False):
        from supriya.tools import nonrealtimetools
        from supriya.tools import responsetools
        from supriya.tools import synthdeftools
        assert isinstance(node, nonrealtimetools.Synth)
        node_id = node.session_id
        synthdef_name = node.synthdef
        if isinstance(synthdef_name, synthdeftools.SynthDef):
            synthdef_name = synthdef_name.actual_name
        controls = []
        if include_controls:
            settings = node._collect_settings(state.offset, persistent=True)
            synthdef, synth_kwargs = node.synthdef, node.synth_kwargs
            for name, parameter in sorted(synthdef.parameters.items()):
                value = parameter.value
                if node.start_offset == state.offset:
                    if name in synth_kwargs:
                        value = synth_kwargs[name]
                if name in settings:
                    value = settings[name]
                try:
                    value = float(value)
                except:
                    pass
                control = responsetools.QueryTreeControl(
                    control_name_or_index=name,
                    control_value=value,
                    )
                controls.append(control)
        query_tree_synth = QueryTreeSynth(
            node_id=node_id,
            synthdef_name=synthdef_name,
            controls=controls,
            )
        return query_tree_synth

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
            control_string = '    ' + control_string
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
        if isinstance(synthdef_name, synthdeftools.SynthDef):
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

    def to_dict(self):
        """
        Convert QueryTreeSynth to JSON-serializable dictionary.

        ::

            >>> query_tree_synth = responsetools.QueryTreeSynth(
            ...     node_id=1001,
            ...     synthdef_name='c1aa521afab5b0c0ce3d744690951649',
            ...     controls=(
            ...         responsetools.QueryTreeControl(
            ...             control_name_or_index='level',
            ...             control_value=1.0,
            ...             ),
            ...         responsetools.QueryTreeControl(
            ...             control_name_or_index='out',
            ...             control_value=0.0,
            ...             ),
            ...         ),
            ...     )

        ::

            >>> import json
            >>> result = query_tree_synth.to_dict()
            >>> result = json.dumps(
            ...     result,
            ...     indent=4,
            ...     separators=(',', ': '),
            ...     sort_keys=True,
            ...     )
            >>> print(result)
            {
                "controls": {
                    "level": 1.0,
                    "out": 0.0
                },
                "node_id": 1001,
                "synthdef": "c1aa521afab5b0c0ce3d744690951649"
            }

        """
        result = {
            'node_id': self.node_id,
            'synthdef': self.synthdef_name,
            'controls': {}
            }
        for control in self.controls:
            name = control.control_name_or_index
            result['controls'][name] = control.control_value
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
