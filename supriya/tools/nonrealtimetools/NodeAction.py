from supriya.tools import requesttools
from supriya.tools import servertools
from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class NodeAction(SupriyaValueObject):
    """
    A non-realtime state transition.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Session Internals'

    __slots__ = (
        '_source',
        '_target',
        '_action',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        source=None,
        action=None,
        target=None,
        ):
        if action is not None:
            action = servertools.AddAction.from_expr(action)
            assert isinstance(action, servertools.AddAction)
            assert source is not target
        if action is None:
            assert source is not None
            assert target is None
        self._action = action
        self._source = source
        self._target = target

    ### PRIVATE METHODS ###

    def _free_node(self, nodes_to_children, nodes_to_parents):
        node = self.source
        for child in nodes_to_children.get(node, ()) or ():
            NodeAction.free_node(child, nodes_to_children, nodes_to_parents)
        parent = nodes_to_parents.get(node, None)
        if node in nodes_to_children:
            del(nodes_to_children[node])
        if node in nodes_to_parents:
            del(nodes_to_parents[node])
        if not parent:
            return
        children = list(nodes_to_children[parent])
        children.remove(node)
        if children:
            children = tuple(children)
        else:
            children = None
        nodes_to_children[parent] = children

    def _move_node(self, nodes_to_children, nodes_to_parents):
        assert self.target in nodes_to_children
        if self.source not in nodes_to_children:
            nodes_to_children[self.source] = None
        old_parent = nodes_to_parents.get(self.source, None)
        if old_parent:
            children = list(nodes_to_children[old_parent])
            children.remove(self.source)
            if children:
                nodes_to_children[old_parent] = tuple(children)
            else:
                nodes_to_children[old_parent] = None
        if self.action in (
            servertools.AddAction.ADD_AFTER,
            servertools.AddAction.ADD_BEFORE,
            ):
            new_parent = nodes_to_parents[self.target]
        else:
            new_parent = self.target
        nodes_to_parents[self.source] = new_parent
        children = list(nodes_to_children.get(new_parent, None) or ())
        if self.action == servertools.AddAction.ADD_TO_HEAD:
            children.insert(0, self.source)
        elif self.action == servertools.AddAction.ADD_TO_TAIL:
            children.append(self.source)
        elif self.action == servertools.AddAction.ADD_BEFORE:
            index = children.index(self.target)
            children.insert(index, self.source)
        elif self.action == servertools.AddAction.ADD_AFTER:
            index = children.index(self.target) + 1
            children.insert(index, self.source)
        nodes_to_children[new_parent] = tuple(children)

    def _to_request(self, id_mapping):
        node_id_pair = requesttools.NodeIdPair(
            node_id=id_mapping[self.source],
            target_node_id=id_mapping[self.target],
            )
        if self.action == servertools.AddAction.ADD_TO_HEAD:
            request_class = requesttools.GroupHeadRequest
        elif self.action == servertools.AddAction.ADD_TO_TAIL:
            request_class = requesttools.GroupTailRequest
        elif self.action == servertools.AddAction.ADD_BEFORE:
            request_class = requesttools.NodeBeforeRequest
        elif self.action == servertools.AddAction.ADD_AFTER:
            request_class = requesttools.NodeAfterRequest
        request = request_class(node_id_pairs=[node_id_pair])
        return request

    ### PUBLIC METHODS ###

    def apply_transform(self, nodes_to_children, nodes_to_parents):
        if self.action is None:
            self._free_node(nodes_to_children, nodes_to_parents)
        else:
            self._move_node(nodes_to_children, nodes_to_parents)

    @staticmethod
    def free_node(node, nodes_to_children, nodes_to_parents):
        action = NodeAction(source=node)
        action.apply_transform(nodes_to_children, nodes_to_parents)

    ### PUBLIC PROPERTIES ###

    @property
    def action(self):
        return self._action

    @property
    def source(self):
        return self._source

    @property
    def target(self):
        return self._target
