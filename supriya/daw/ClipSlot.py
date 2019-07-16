from typing import Optional

from uqbar.containers import UniqueTreeNode

import supriya.daw  # noqa

from .Clip import Clip


class ClipSlot(UniqueTreeNode):

    ### INITIALIZER ###

    def __init__(self):
        UniqueTreeNode.__init__(self)
        self._clip: Optional[Clip] = None

    ### PUBLIC METHODS ###

    def fire(self):
        application = self.application
        if application is None:
            raise ValueError

    ### PUBLIC PROPERTIES ###

    @property
    def application(self) -> Optional["supriya.daw.Application"]:
        from .Application import Application

        for parent in self.parentage[1:]:
            if isinstance(parent, Application):
                return parent
        return None
