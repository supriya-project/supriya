# -*- encoding: utf-8 -*-
import collections
from supriya.tools.datastructuretools.TreeNode import TreeNode


class TreeContainer(TreeNode):

    ### CLASS VARIABLES ###

    __slots__ = (
        # '_children',
        # '_name',
        # '_named_children',
        # '_parent',
        )

    ### INITIALIZER ###

    def __init__(self, children=None, name=None):
        TreeNode.__init__(self, name=name)
        self._children = []
        self._named_children = {}
        if children is not None:
            self[:] = children

    ### SPECIAL METHODS ###

    def __contains__(self, expr):
        for x in self._children:
            if x is expr:
                return True
        return False

    def __delitem__(self, i):
        if isinstance(i, str):
            i = self.index(self._named_children[i])
        if isinstance(i, int):
            if i < 0:
                i = len(self) + i
            i = slice(i, i + 1)
        self.__setitem__(i, [])

    def __getitem__(self, expr):
        if isinstance(expr, (int, slice)):
            return self._children[expr]
        elif isinstance(expr, str):
            return self._named_children[expr]
        raise ValueError(expr)

    def __iter__(self):
        for child in self._children:
            yield child

    def __len__(self):
        return len(self._children)

    def __setitem__(self, i, expr):
        self._validate_setitem_expr(expr)
        if isinstance(i, slice):
            assert isinstance(expr, collections.Sequence)
        if isinstance(i, str):
            i = self.index(self._named_children[i])
        if isinstance(i, int):
            if i < 0:
                i = len(self) + i
            i = slice(i, i + 1)
        if i.start == i.stop and i.start is not None \
            and i.stop is not None and i.start <= -len(self):
            start, stop = 0, 0
        else:
            start, stop, stride = i.indices(len(self))
        if not isinstance(expr, collections.Sequence):
            expr = [expr]
        for old_child in tuple(self[start:stop]):
            old_child._set_parent(None)
        self._children[start:stop] = expr
        for new_child in expr:
            new_child._set_parent(self)

    ### PRIVATE METHODS ###

    def _validate_setitem_expr(self, expr):
        from supriya.tools import servertools
        assert all(isinstance(_, TreeNode) for _ in expr)
        parentage = self.parentage
        for x in expr:
            if isinstance(x, TreeContainer):
                assert x not in parentage

    ### PUBLIC METHODS ###

    def append(self, expr):
        self.__setitem__(
            slice(len(self), len(self)),
            [expr]
            )

    def extend(self, expr):
        self.__setitem__(
            slice(len(self), len(self)),
            expr
            )

    def index(self, expr):
        for i, child in enumerate(self._children):
            if child is expr:
                return i
        else:
            message = '{!r} not in {!r}.'
            message = message.format(expr, self)
            raise ValueError(message)

    def insert(self, i, expr):
        self.__setitem__(
            slice(i, i),
            [expr]
            )

    def pop(self, i=-1):
        node = self[i]
        del(self[i])
        return node

    def remove(self, node):
        i = self.index(node)
        del(self[i])

    ### PUBLIC PROPERTIES ###

    @property
    def children(self):
        return tuple(self._children)
