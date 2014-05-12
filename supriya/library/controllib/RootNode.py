from supriya.library.controllib.Group import Group


class RootNode(Group):

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    _instance = None

    ### CONSTRUCTOR ###

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RootNode, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    ### INITIALIZER ###

    def __init__(self):
        from supriya.library import controllib
        controllib.Node.__init__(
            self,
            node_id=0,
            server=controllib.Server(),
            )
