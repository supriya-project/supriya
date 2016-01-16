# -*- encoding: utf-8 -*-
from supriya.tools import servertools
from supriya.tools.nonrealtimetools.NRTGroup import NRTGroup


class NRTRootNode(NRTGroup):

    ### CLASS VARIABLES ###
    
    _valid_add_actions = (
        servertools.AddAction.ADD_TO_HEAD,
        servertools.AddAction.ADD_TO_TAIL,
        )

    ### INITIALIZER ###

    def __init__(self, session):
        NRTGroup.__init__(self, session, 0)

    ### SPECIAL METHODS ###

    def __str__(self):
        return 'root'
