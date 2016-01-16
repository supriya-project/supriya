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

    def apply_transform(self, nodes_to_children, nodes_to_parents):
        assert self.target in nodes_to_children
        if self.source not in nodes_to_children:
            nodes_to_children[self.source] = None
        old_parent = nodes_to_parents.get(self.source, None)
        if old_parent:
            children = list(nodes_to_children[old_parent])
            children.remove(self.source)
            if children:
                nodes_to_children[old_parent] = tuple(children)
            else:
                nodes_to_children[old_parent] = None
        if self.action in (
            servertools.AddAction.ADD_AFTER,
            servertools.AddAction.ADD_BEFORE,
            ):
            new_parent = nodes_to_parents[self.target]
        else:
            new_parent = self.target
        nodes_to_parents[self.source] = new_parent
        children = list(nodes_to_children.get(new_parent, None) or ())
        if self.action == servertools.AddAction.ADD_TO_HEAD:
            children.insert(0, self.source)
        elif self.action == servertools.AddAction.ADD_TO_TAIL:
            children.append(self.source)
        elif self.action == servertools.AddAction.ADD_BEFORE:
            index = children.index(self.target)
            children.insert(index, self.source)
        elif self.action == servertools.AddAction.ADD_AFTER:
            index = children.index(self.target) + 1
            children.insert(index, self.source)
        nodes_to_children[new_parent] = tuple(children)

    @staticmethod
    def free_node(node, nodes_to_children, nodes_to_parents):
        for child in nodes_to_children.get(node, ()) or ():
            NRTNodeAction.free_node(child, nodes_to_children, nodes_to_parents)
        parent = nodes_to_parents.get(node, None)
        if node in nodes_to_children:
            del(nodes_to_children[node])
        if node in nodes_to_parents:
            del(nodes_to_parents[node])
        if not parent:
            return
        children = list(nodes_to_children[parent])
        children.remove(node)
        if children:
            children = tuple(children)
        else:
            children = None
        nodes_to_children[parent] = children

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
