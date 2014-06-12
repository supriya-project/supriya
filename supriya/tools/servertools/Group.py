from supriya.tools.servertools.Node import Node


class Group(Node):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_children',
        )

    ### INITIALIZER ###

    def __init__(self):
        Node.__init__(self)
        self._children = []

    ### PUBLIC METHODS ###
