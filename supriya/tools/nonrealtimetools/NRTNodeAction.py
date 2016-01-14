# -*- encoding: utf-8 -*-
from supriya.tools import servertools


class NRTNodeAction(object):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_source',
        '_target',
        '_action',
        )

    ### INITIALIZER ###

    def __init__(self, source, action, target):
        from supriya.tools import nonrealtimetools
        assert isinstance(source, nonrealtimetools.NRTNode)
        assert isinstance(target, nonrealtimetools.NRTNode)
        action = servertools.AddAction.from_expr(action)
        assert isinstance(action, servertools.AddAction)
        self._source = source
        self._target = target
        self._action = action

    ### PUBLIC METHODS ###

    def apply_transform(self, nodes_to_children, nodes_to_parent):
        pass

    @staticmethod
    def free_node(node, nodes_to_children, nodes_to_parent):
        pass

    ### PUBLIC PROPERTIES ###

    @property
    def action(self):
        return self._action

    @property
    def source(self):
        return self._source

    @property
    def target(self):
        return self._target
