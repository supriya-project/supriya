import enum


class Node(object):

    ### CLASS VARIABLES ###

    class AddAction(enum.IntEnum):
        ADD_TO_HEAD = 0
        ADD_TO_TAIL = 1
        ADD_BEFORE = 2
        ADD_AFTER = 3
        ADD_REPLACE = 4

    __slots__ = (
        )
