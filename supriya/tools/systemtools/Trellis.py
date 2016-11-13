# -*- encoding: utf-8 -*-
import collections
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class Trellis(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_parents_to_children',
        '_children_to_parents',
        )

    ### INITIALIZER ###

    def __init__(self):
        self._parents_to_children = collections.OrderedDict()
        self._children_to_parents = collections.OrderedDict()

    ### SPECIAL METHODS ###

    def __contains__(self, expr):
        return expr in self._parents_to_children

    def __eq__(self, expr):
        if type(self) != type(expr):
            return False
        return self._parents_to_children == expr._parents_to_children

    def __getitem__(self, expr):
        if expr not in self:
            raise ValueError('{!r} not in {}'.format(expr, type(self)))
        parents = frozenset(self._children_to_parents[expr])
        children = frozenset(self._parents_to_children[expr])
        return parents, children

    def __iter__(self):
        trellis = self.copy()
        while len(trellis):
            yield trellis.pop()

    def __len__(self):
        return len(self._parents_to_children)

    ### PUBLIC METHODS ###

    def add(self, child, parent=None):
        if parent is not None and parent not in self:
            self.add(parent)
        self._parents_to_children.setdefault(child, [])
        parents = self._children_to_parents.setdefault(child, [])
        if parent is not None:
            if parent not in parents:
                parents.append(parent)
            children = self._parents_to_children[parent]
            if child not in children:
                children.append(child)

    def children(self, expr):
        if expr not in self:
            raise ValueError('{!r} not in {}'.format(expr, type(self)))
        return frozenset(self._parents_to_children[expr])

    def copy(self):
        copied = type(self)()
        copied._parents_to_children = self._parents_to_children.copy()
        for parent, children in copied._parents_to_children.items():
            copied._parents_to_children[parent] = list(children)
        copied._children_to_parents = self._children_to_parents.copy()
        for child, parents in copied._children_to_parents.items():
            copied._children_to_parents[child] = list(parents)
        return copied

    def is_acyclic(self):
        trellis = self.copy()
        while len(trellis):
            try:
                trellis.pop()
            except ValueError:
                return False
        return True

    def parents(self, expr):
        if expr not in self:
            raise ValueError('{!r} not in {}'.format(expr, type(self)))
        return frozenset(self._children_to_parents[expr])

    def pop(self):
        popped = None
        for parent, children in self._parents_to_children.items():
            if children:
                continue
            popped = parent
            break
        if popped is None:
            raise ValueError('Trellis contains cycles.')
        self.remove(popped)
        return popped

    def remove(self, expr):
        if expr not in self:
            raise ValueError('{!r} not in {}'.format(expr, type(self)))
        for child in self._parents_to_children.pop(expr):
            self._children_to_parents[child].remove(expr)
        for parent in self._children_to_parents.pop(expr):
            self._parents_to_children[parent].remove(expr)
