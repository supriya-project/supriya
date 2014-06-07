# -*- encoding: utf-8 -*-
from supriya.library.systemlib.Enumeration import Enumeration


class AddAction(Enumeration):
    r'''An enumeration of scsynth node add actions.

    ::

        >>> from supriya.library import controllib
        >>> controllib.AddAction.ADD_TO_HEAD
        <AddAction.ADD_TO_HEAD: 0>

    ::

        >>> controllib.AddAction.from_expr('add before')
        <AddAction.ADD_BEFORE: 2>

    '''

    ### CLASS VARIABLES ###

    ADD_TO_HEAD = 0
    ADD_TO_TAIL = 1
    ADD_BEFORE = 2
    ADD_AFTER = 3
    REPLACE = 4
