from .bases import Response
from supriya.enums import NodeAction


class NodeInfoResponse(Response):

    ### INITIALIZER ###

    def __init__(
        self,
        action=None,
        node_id=None,
        parent_id=None,
        previous_node_id=None,
        next_node_id=None,
        is_group=None,
        head_node_id=None,
        tail_node_id=None,
        synthdef_name=None,
        synthdef_controls=None,
    ):
        self._action = NodeAction.from_address(action)
        self._is_group = bool(is_group)
        self._head_node_id = self._coerce_node_id(head_node_id)
        self._next_node_id = self._coerce_node_id(next_node_id)
        self._node_id = self._coerce_node_id(node_id)
        self._parent_id = self._coerce_node_id(parent_id)
        self._previous_node_id = self._coerce_node_id(previous_node_id)
        self._tail_node_id = self._coerce_node_id(tail_node_id)
        self._synthdef_name = synthdef_name
        self._synthdef_controls = synthdef_controls

    ### PRIVATE METHODS ###

    def _coerce_node_id(self, node_id):
        if node_id is not None and -1 < node_id:
            return node_id
        return None

    ### PUBLIC METHODS ###

    @classmethod
    def from_osc_message(cls, osc_message):
        arguments = (osc_message.address,) + osc_message.contents
        kwargs = dict(
            action=arguments[0],
            node_id=arguments[1],
            parent_id=arguments[2],
            previous_node_id=arguments[3],
            next_node_id=arguments[4],
            is_group=arguments[5],
        )
        if arguments[5]:
            kwargs.update(head_node_id=arguments[6], tail_node_id=arguments[7])
        elif len(arguments) > 6:
            controls = []
            for i in range(arguments[7]):
                controls.append((arguments[8 + (i * 2)], arguments[9 + (i * 2)]))
            kwargs.update(synthdef_name=arguments[6], synthdef_controls=tuple(controls))
        response = cls(**kwargs)
        return response

    ### PUBLIC PROPERTIES ###

    @property
    def action(self):
        return self._action

    @property
    def head_node_id(self):
        return self._head_node_id

    @property
    def is_group(self):
        return self._is_group

    @property
    def next_node_id(self):
        return self._next_node_id

    @property
    def node_id(self):
        return self._node_id

    @property
    def parent_id(self):
        return self._parent_id

    @property
    def previous_node_id(self):
        return self._previous_node_id

    @property
    def tail_node_id(self):
        return self._tail_node_id

    @property
    def synthdef_controls(self):
        return self._synthdef_controls

    @property
    def synthdef_name(self):
        return self._synthdef_name
