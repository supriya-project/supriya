# -*- encoding: utf-8 -*-
from supriya.tools.responsetools.Response import Response


class QueryTreeGroup(Response):

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

    def __str__(self):
        result = self._get_str_format_pieces()
        result = '\n'.join(result)
        result = 'NODE TREE {}'.format(result)
        return result

    ### PRIVATE METHODS ###

    def _get_str_format_pieces(self):
        result = []
        string = '{} group'.format(self.node_id)
        result.append(string)
        for child in self.children:
            for line in child._get_str_format_pieces():
                result.append('\t{}'.format(line))
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def children(self):
        return self._children

    @property
    def node_id(self):
        return self._node_id
