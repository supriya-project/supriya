from uqbar.containers import UniqueTreeDict

from supriya.realtime import Group

from .DawNode import DawNode
from .Send import Send


class SendManager(DawNode, UniqueTreeDict):

    ### INITIALIZER ###

    def __init__(self):
        DawNode.__init__(self)
        UniqueTreeDict.__init__(self)
        self._pre_fader_group = Group(name="pre-fader sends")
        self._post_fader_group = Group(name="post-fader sends")

    ### PRIVATE METHODS ###

    def _iter_children(self, prototype=None):
        for node in self.values():
            if not prototype or isinstance(node, prototype):
                yield node

    def _update_parentage(self, new_nodes, old_nodes):
        UniqueTreeDict._update_parentage(self, new_nodes, old_nodes)
        alloc_nodes = [node for node in new_nodes if node._pre_allocate(self._server)]
        # for node in new_nodes:
        #     node._reallocate()
        for node in alloc_nodes:
            node._post_allocate()
        for node in old_nodes:
            node._free()

    def _validate(self, new_items, old_items):
        UniqueTreeDict._validate(self, new_items, old_items)
        for key, value in new_items:
            if key is not value.target:
                raise ValueError(value.target)

    ### PRIVATE PROPERTIES ###

    @property
    def _node_class(self):
        return Send

    ### PUBLIC PROPERTIES ###

    @property
    def post_fader_group(self):
        return self._post_fader_group

    @property
    def pre_fader_group(self):
        return self._pre_fader_group
