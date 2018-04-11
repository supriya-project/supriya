from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class NodeIdPair(SupriyaValueObject):
    """
    A node id pair.

    ::

        >>> import supriya.commands
        >>> node_id_pair = supriya.commands.NodeIdPair(
        ...     node_id=1001,
        ...     target_node_id=1000,
        ...     )
        >>> node_id_pair
        NodeIdPair(
            node_id=1001,
            target_node_id=1000,
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_node_id',
        '_target_node_id',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        node_id=None,
        target_node_id=None,
        ):
        self._node_id = int(node_id)
        self._target_node_id = int(target_node_id)

    ### PUBLIC PROPERTIES ###

    @property
    def node_id(self):
        return self._node_id

    @property
    def target_node_id(self):
        return self._target_node_id
