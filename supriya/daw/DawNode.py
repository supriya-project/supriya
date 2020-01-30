import logging
from typing import Optional

from uqbar.containers import UniqueTreeNode

import supriya.daw  # noqa
from supriya.realtime import Server

from .DawMeta import DawMeta
from .DawMixin import DawMixin

logger = logging.getLogger("supriya.daw")


class DawNode(UniqueTreeNode, DawMixin, metaclass=DawMeta):

    ### INITIALIZER ###

    def __init__(self, *, channel_count=None, name=None):
        UniqueTreeNode.__init__(self, name=name)
        self._channel_count = channel_count
        self._server = None
        self._ready = None

    ### PRIVATE METHODS ###

    def _allocate_synthdefs(self, server):
        return

    def _create_bus_groups(self, server):
        for bus_group in self._list_bus_groups():
            bus_group.allocate(server)

    def _create_bus_routings(self, server):
        pass

    def _create_osc_callbacks(self, server):
        pass

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
        self._ready = False
        if self._server is None:
            return False
        self._unregister_with_transport()
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
        self._allocate_synthdefs(server)
        self._create_bus_groups(server)
        self._create_bus_routings(server)
        self._register_with_transport()
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
        self._ready = True

    def _reallocate(self):
        """
        Re-allocate nodes previously allocated on the server, and perform any necessary setup/teardown.
        """
        self._debug_tree("Re-alloc")
        self._ready = False
        for node in self._iter_children():
            node._reallocate()
        self._ready = True

    def _register_with_transport(self):
        pass

    def _unregister_with_transport(self):
        pass

    ### PUBLIC PROPERTIES ###

    @property
    def channel_count(self):
        return self._channel_count

    @property
    def ready(self):
        return self._ready

    @property
    def server(self) -> Optional[Server]:
        return self._server
