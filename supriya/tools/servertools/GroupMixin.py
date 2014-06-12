# -*- encoding: utf-8 -*-
import abc
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class GroupMixin(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        self._children = []

    ### PRIVATE METHODS ###

    @staticmethod
    def _iterate_children(group):
        from supriya.tools import servertools
        for child in group.children:
            if isinstance(child, servertools.GroupMixin):
                for subchild in GroupMixin._iterate_children(child):
                    yield subchild
            yield child

    ### PUBLIC PROPERTIES ###

    @property
    def children(self):
        return tuple(self._children)
