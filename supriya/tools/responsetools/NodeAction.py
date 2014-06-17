# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.Enumeration import Enumeration


class NodeAction(Enumeration):

    ### CLASS VARIABLES ###

    NODE_CREATED = 0
    NODE_REMOVED = 1
    NODE_ACTIVATED = 2
    NODE_DEACTIVATED = 3
    NODE_MOVED = 4
    NODE_QUERIED = 5

    ### PUBLIC METHODS ###

    @staticmethod
    def from_address(address):
        addresses = {
            '/n_end': NodeAction.NODE_REMOVED,
            '/n_go': NodeAction.NODE_CREATED,
            '/n_info': NodeAction.NODE_QUERIED,
            '/n_move': NodeAction.NODE_MOVED,
            '/n_off': NodeAction.NODE_DEACTIVATED,
            '/n_on': NodeAction.NODE_ACTIVATED,
            }
        action = addresses[address]
        return action