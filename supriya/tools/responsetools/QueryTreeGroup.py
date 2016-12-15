# -*- encoding: utf-8 -*-
import collections
from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class QueryTreeGroup(SupriyaValueObject, collections.Sequence):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_children',
        '_node_id',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        node_id=None,
        children=None,
        ):
        self._children = children
        self._node_id = node_id

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self._children[item]

    def __len__(self):
        return len(self._children)

    def __str__(self):
        result = self._get_str_format_pieces()
        result = '\n'.join(result)
        result = 'NODE TREE {}'.format(result)
        return result

    ### PRIVATE METHODS ###

    @classmethod
    def _from_nrt_group(cls, state, node, include_controls=False):
        from supriya.tools import nonrealtimetools
        from supriya.tools import responsetools
        assert isinstance(node, nonrealtimetools.Group)
        node_id = node.session_id
        children = []
        for child in (state.nodes_to_children.get(node) or ()):
            if isinstance(child, nonrealtimetools.Group):
                child = QueryTreeGroup._from_nrt_group(
                    state, child, include_controls=include_controls)
            elif isinstance(child, nonrealtimetools.Synth):
                child = responsetools.QueryTreeSynth._from_nrt_synth(
                    state, child, include_controls=include_controls)
            else:
                raise ValueError(child)
            children.append(child)
        children = tuple(children)
        query_tree_group = QueryTreeGroup(
            node_id=node_id,
            children=children,
            )
        return query_tree_group

    def _get_str_format_pieces(self):
        result = []
        string = '{} group'.format(self.node_id)
        result.append(string)
        for child in self.children:
            for line in child._get_str_format_pieces():
                result.append('    {}'.format(line))
        return result

    ### PUBLIC METHODS ###

    @classmethod
    def from_group(cls, group, include_controls=False):
        from supriya.tools import responsetools
        from supriya.tools import servertools
        assert isinstance(group, servertools.Group)
        node_id = group.node_id
        children = []
        for child in group.children:
            if isinstance(child, servertools.Group):
                child = QueryTreeGroup.from_group(
                    child,
                    include_controls=include_controls,
                    )
            elif isinstance(child, servertools.Synth):
                child = responsetools.QueryTreeSynth.from_synth(
                    child,
                    include_controls=include_controls,
                    )
            else:
                raise ValueError(child)
            children.append(child)
        children = tuple(children)
        query_tree_group = QueryTreeGroup(
            node_id=node_id,
            children=children,
            )
        return query_tree_group

    @classmethod
    def from_state(cls, state, include_controls=False):
        root_node = state.session.root_node
        query_tree_group = cls._from_nrt_group(
            state, root_node, include_controls=include_controls)
        return query_tree_group

    def to_dict(self):
        """
        Convert QueryTreeGroup to JSON-serializable dictionary.

        ::

            >>> query_tree_group = responsetools.QueryTreeGroup(
            ...     node_id=1002,
            ...     children=(
            ...         responsetools.QueryTreeSynth(
            ...             node_id=1105,
            ...             synthdef_name='dca557070c6b57164557041ac746fb3f',
            ...             controls=(
            ...                 responsetools.QueryTreeControl(
            ...                     control_name_or_index='damping',
            ...                     control_value=0.06623425334692,
            ...                     ),
            ...                 responsetools.QueryTreeControl(
            ...                     control_name_or_index='duration',
            ...                     control_value=3.652155876159668,
            ...                     ),
            ...                 responsetools.QueryTreeControl(
            ...                     control_name_or_index='level',
            ...                     control_value=0.894767701625824,
            ...                     ),
            ...                 responsetools.QueryTreeControl(
            ...                     control_name_or_index='out',
            ...                     control_value=16.0,
            ...                     ),
            ...                 responsetools.QueryTreeControl(
            ...                     control_name_or_index='room_size',
            ...                     control_value=0.918643176555634,
            ...                     ),
            ...                 ),
            ...             ),
            ...         responsetools.QueryTreeSynth(
            ...             node_id=1098,
            ...             synthdef_name='cc754c63533fdcf412a44ef6adb1a8f0',
            ...             controls=(
            ...                 responsetools.QueryTreeControl(
            ...                     control_name_or_index='duration',
            ...                     control_value=5.701356887817383,
            ...                     ),
            ...                 responsetools.QueryTreeControl(
            ...                     control_name_or_index='level',
            ...                     control_value=0.959683060646057,
            ...                     ),
            ...                 responsetools.QueryTreeControl(
            ...                     control_name_or_index='out',
            ...                     control_value=16.0,
            ...                     ),
            ...                 responsetools.QueryTreeControl(
            ...                     control_name_or_index='pitch_dispersion',
            ...                     control_value=0.040342573076487,
            ...                     ),
            ...                 responsetools.QueryTreeControl(
            ...                     control_name_or_index='pitch_shift',
            ...                     control_value=10.517594337463379,
            ...                     ),
            ...                 responsetools.QueryTreeControl(
            ...                     control_name_or_index='time_dispersion',
            ...                     control_value=0.666014134883881,
            ...                     ),
            ...                 responsetools.QueryTreeControl(
            ...                     control_name_or_index='window_size',
            ...                     control_value=1.014111995697021,
            ...                     ),
            ...                 ),
            ...             ),
            ...         ),
            ...     )

        ::

            >>> import json
            >>> result = query_tree_group.to_dict()
            >>> result = json.dumps(
            ...     result,
            ...     indent=4,
            ...     separators=(',', ': '),
            ...     sort_keys=True,
            ...     )
            >>> print(result)
            {
                "children": [
                    {
                        "controls": {
                            "damping": 0.06623425334692,
                            "duration": 3.652155876159668,
                            "level": 0.894767701625824,
                            "out": 16.0,
                            "room_size": 0.918643176555634
                        },
                        "node_id": 1105,
                        "synthdef": "dca557070c6b57164557041ac746fb3f"
                    },
                    {
                        "controls": {
                            "duration": 5.701356887817383,
                            "level": 0.959683060646057,
                            "out": 16.0,
                            "pitch_dispersion": 0.040342573076487,
                            "pitch_shift": 10.517594337463379,
                            "time_dispersion": 0.666014134883881,
                            "window_size": 1.014111995697021
                        },
                        "node_id": 1098,
                        "synthdef": "cc754c63533fdcf412a44ef6adb1a8f0"
                    }
                ],
                "node_id": 1002
            }

        """
        result = {
            'node_id': self.node_id,
            'children': [x.to_dict() for x in self.children]
            }
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def children(self):
        return self._children

    @property
    def node_id(self):
        return self._node_id
