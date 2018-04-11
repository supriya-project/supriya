import supriya.realtime
from supriya.nonrealtime.Group import Group


class RootNode(Group):
    """
    A non-realtime root node.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Session Objects'

    __slots__ = ()

    _valid_add_actions = (
        supriya.realtime.AddAction.ADD_TO_HEAD,
        supriya.realtime.AddAction.ADD_TO_TAIL,
        )

    ### INITIALIZER ###

    def __init__(self, session):
        Group.__init__(
            self,
            session=session,
            session_id=0,
            duration=float('inf'),
            start_offset=float('-inf'),
            )

    ### SPECIAL METHODS ###

    def __str__(self):
        return 'root'

    ### PUBLIC PROPERTIES ###

    @property
    def start_offset(self):
        return float('-inf')

    @property
    def stop_offset(self):
        return float('inf')

    @property
    def duration(self):
        return float('inf')
