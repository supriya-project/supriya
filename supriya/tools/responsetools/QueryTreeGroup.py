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

    ### PUBLIC PROPERTIES ###

    @property
    def children(self):
        return self._children

    @property
    def node_id(self):
        return self._node_id
