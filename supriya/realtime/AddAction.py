from supriya.system.Enumeration import Enumeration


class AddAction(Enumeration):
    """
    An enumeration of scsynth node add actions.

    ::

        >>> import supriya.realtime
        >>> supriya.realtime.AddAction.ADD_TO_HEAD
        AddAction.ADD_TO_HEAD

    ::

        >>> supriya.realtime.AddAction.from_expr('add before')
        AddAction.ADD_BEFORE

    """

    ### CLASS VARIABLES ###

    ADD_TO_HEAD = 0
    ADD_TO_TAIL = 1
    ADD_BEFORE = 2
    ADD_AFTER = 3
    REPLACE = 4
