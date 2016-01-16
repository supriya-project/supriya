# -*- encoding: utf-8 -*-
from supriya.tools import servertools
from supriya.tools.nonrealtimetools.NRTNode import NRTNode


class NRTGroup(NRTNode):

    ### CLASS VARIABLES ###

    _valid_add_actions = (
        servertools.AddAction.ADD_TO_HEAD,
        servertools.AddAction.ADD_TO_TAIL,
        servertools.AddAction.ADD_AFTER,
        servertools.AddAction.ADD_BEFORE,
        )

    ### SPECIAL METHODS ###

    def __str__(self):
        return 'group-{}'.format(self.session_id)
