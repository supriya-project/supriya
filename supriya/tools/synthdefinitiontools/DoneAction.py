# -*- encoding: utf-8 -*-
from supriya.tools.systemlib.Enumeration import Enumeration


class DoneAction(Enumeration):
    r'''An enumeration of scsynth UGen "done" actions.

    ::

        >>> from supriya.tools import synthdefinitiontools
        >>> synthdefinitiontools.DoneAction(2)
        <DoneAction.FREE_SYNTH: 2>

    ::

        >>> synthdefinitiontools.DoneAction.from_expr('pause synth')
        <DoneAction.PAUSE_SYNTH: 1>

    '''

    ### CLASS VARIABLES ###

    NOTHING = 0
    PAUSE_SYNTH = 1
    FREE_SYNTH = 2
    FREE_SYNTH_AND_PRECEDING_NODE = 3
    FREE_SYNTH_AND_FOLLOWING_NODE = 4
    FREE_SYNTH_AND_FREEALL_PRECEDING_NODE = 5
    FREE_SYNTH_AND_FREEALL_FOLLOWING_NODE = 6
    FREE_SYNTH_AND_ALL_PRECEDING_NODES_IN_GROUP = 7
    FREE_SYNTH_AND_ALL_FOLLOWING_NODES_IN_GROUP = 8
    FREE_SYNTH_AND_PAUSE_PRECEDING_NODE = 9
    FREE_SYNTH_AND_PAUSE_FOLLOWING_NODE = 10
    FREE_SYNTH_AND_DEEPFREE_PRECEDING_NODE = 11
    FREE_SYNTH_AND_DEEPFREE_FOLLOWING_NODE = 12
    FREE_SYNTH_AND_ALL_SIBLING_NODES = 13
    FREE_SYNTH_AND_ENCLOSING_GROUP = 14
