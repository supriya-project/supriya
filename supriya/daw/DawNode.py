from typing import Optional

from uqbar.containers import UniqueTreeNode

import supriya.daw  # noqa
from supriya.realtime import Group, Server

from .DawMeta import DawMeta
from .MixerContext import MixerContext


class DawNode(UniqueTreeNode, metaclass=DawMeta):

    ### CLASS VARIABLES ###

    _node = None

    ### INITIALIZER ###

    def __init__(self, *, channel_count=None, name=None):
        UniqueTreeNode.__init__(self, name=name)
        self._channel_count = channel_count
        self._server = None

    ### PRIVATE METHODS ###

    def _create_bus_groups(self, server):
        for bus_group in self._list_bus_groups():
            bus_group.allocate(server)

    def _create_bus_routings(self, server):
        pass

    def _create_osc_callbacks(self, server):
        pass

    def _debug_tree(self, prefix):
        print(
            f"{(prefix + ':').ljust(15)} {'..' * self.depth} {type(self).__name__}"
            f"{' (' + self.node.name + ')' if self.node else ''}"
        )

    def _destroy_bus_groups(self, server):
        for bus_group in self._list_bus_groups():
            bus_group.free()

    def _destroy_osc_callbacks(self, server):
        pass

    def _free(self) -> bool:
        """
        Free nodes and other resources allocated on the server.
        """
        self._debug_tree("Freeing")
        if self._server is None:
            return False
        for node in self._iter_children():
            node._free()
        self._destroy_osc_callbacks(self.server)
        self._destroy_bus_groups(self.server)
        self._server = None
        return True

    def _iter_children(self, prototype=None):
        try:
            for node in self:
                if not prototype or isinstance(node, prototype):
                    yield node
        except TypeError:
            for node in []:
                yield node

    def _list_bus_groups(self):
        return []

    def _pre_allocate(self, server) -> bool:
        """
        Perform actions necessary before allocating nodes in the server.
        """
        if self._server is server:
            self._debug_tree("Pre-alloc (F)")
            return False
        elif self._server:
            self._free()
        self._debug_tree("Pre-alloc (T)")
        self._server = server
        self._create_bus_groups(server)
        self._create_bus_routings(server)
        for node in self._iter_children():
            node._pre_allocate(server)
        return True

    def _post_allocate(self):
        """
        Perform actions only possible after allocating nodes in the server.
        """
        self._debug_tree("Post-alloc")
        if not self.server:
            raise ValueError(self.server)
        self._create_osc_callbacks(self.server)
        for node in self._iter_children():
            node._post_allocate()

    def _reallocate(self):
        """
        Re-allocate nodes previously allocated on the server, and perform any necessary setup/teardown.
        """
        self._debug_tree("Re-alloc")
        for node in self._iter_children():
            node._reallocate()

    ### PUBLIC PROPERTIES ###

    @property
    def application(self) -> Optional["supriya.daw.Application"]:
        from .Application import Application

        for parent in self.parentage[1:]:
            if isinstance(parent, Application):
                return parent
        return None

    @property
    def channel_count(self):
        return self._channel_count

    @property
    def node(self) -> Optional[Group]:
        return self._node

    @property
    def mixer_context(self) -> Optional[MixerContext]:
        for parent in self.parentage[1:]:
            if isinstance(parent, MixerContext):
                return parent
        return None

    @property
    def server(self) -> Optional[Server]:
        return self._server
