# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.Enumeration import Enumeration


class AddAction(Enumeration):
    """
    An enumeration of scsynth node add actions.

    ::

        >>> from supriya.tools import servertools
        >>> servertools.AddAction.ADD_TO_HEAD
        AddAction.ADD_TO_HEAD

    ::

        >>> servertools.AddAction.from_expr('add before')
        AddAction.ADD_BEFORE

    """

    ### CLASS VARIABLES ###

    ADD_TO_HEAD = 0
    ADD_TO_TAIL = 1
    ADD_BEFORE = 2
    ADD_AFTER = 3
    REPLACE = 4
