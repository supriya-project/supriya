from typing import Optional

from uqbar.containers import UniqueTreeList

from .ClipSlot import ClipSlot


class ClipSlotContainer(UniqueTreeList):

    ### PRIVATE PROPERTIES ###

    @property
    def _node_class(self):
        return ClipSlot

    ### PUBLIC PROPERTIES ###

    @property
    def application(self) -> Optional["supriya.daw.Application"]:
        from .Application import Application

        for parent in self.parentage[1:]:
            if isinstance(parent, Application):
                return parent
        return None
