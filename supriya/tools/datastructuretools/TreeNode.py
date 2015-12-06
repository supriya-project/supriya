# -*- encoding: utf-8 -*-
import collections
import copy


class TreeNode(object):

    ### CLASS VARIABLES ###

    __slots__ = (
        # '_name',
        # '_parent',
        )

    ### INITIALIZER ###

    def __init__(self, name=None):
        self._name = name
        self._parent = None

    ### PRIVATE METHODS ###

    def _cache_named_children(self):
        name_dictionary = {}
        if hasattr(self, '_named_children'):
            for name, children in self._named_children.items():
                name_dictionary[name] = copy.copy(children)
        if hasattr(self, 'name') and self.name is not None:
            if self.name not in name_dictionary:
                name_dictionary[self.name] = set()
            name_dictionary[self.name].add(self)
        return name_dictionary

    @classmethod
    def _iterate_nodes(cls, nodes):
        for x in nodes:
            yield x
            if hasattr(x, '_children'):
                for y in cls._iterate_nodes(x):
                    yield y

    def _remove_from_parent(self):
        if self._parent is not None:
            if self in self._parent:
                self._parent._children.remove(self)
        self._parent = None

    def _remove_named_children_from_parentage(self, name_dictionary):
        if self._parent is not None and name_dictionary:
            for parent in self.parentage[1:]:
                named_children = parent._named_children
                for name in name_dictionary:
                    for node in name_dictionary[name]:
                        named_children[name].remove(node)
                    if not named_children[name]:
                        del(named_children[name])

    def _restore_named_children_to_parentage(self, name_dictionary):
        if self._parent is not None and name_dictionary:
            for parent in self.parentage[1:]:
                named_children = parent._named_children
                for name in name_dictionary:
                    if name in named_children:
                        named_children[name].update(name_dictionary[name])
                    else:
                        named_children[name] = copy.copy(name_dictionary[name])

    def _set_parent(self, new_parent):
        named_children = self._cache_named_children()
        self._remove_named_children_from_parentage(named_children)
        self._remove_from_parent()
        self._parent = new_parent
        self._restore_named_children_to_parentage(named_children)

    ### PUBLIC METHODS ###

    def precede_by(self, expr):
        if not isinstance(expr, collections.Sequence):
            expr = [expr]
        index = self.parent.index(self)
        self.parent[index:index] = expr

    def replace_with(self, expr):
        if not isinstance(expr, collections.Sequence):
            expr = [expr]
        index = self.parent.index(self)
        self.parent[index:index + 1] = expr

    def succeed_by(self, expr):
        if not isinstance(expr, collections.Sequence):
            expr = [expr]
        index = self.parent.index(self)
        self.parent[index + 1:index + 1] = expr

    ### PUBLIC PROPERTIES ###

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, expr):
        assert isinstance(expr, (str, type(None)))
        old_name = self._name
        for parent in self.parentage[1:]:
            named_children = parent._named_children
            if old_name is not None:
                named_children[old_name].remove(self)
                if not named_children[old_name]:
                    del named_children[old_name]
            if expr is not None:
                if expr not in named_children:
                    named_children[expr] = set([self])
                else:
                    named_children[expr].add(self)
        self._name = expr

    @property
    def parent(self):
        return self._parent

    @property
    def parentage(self):
        parentage = []
        node = self
        while node is not None:
            parentage.append(node)
            node = node.parent
        return tuple(parentage)
