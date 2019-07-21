import contextlib
from typing import Optional

from uqbar.containers import UniqueTreeNode

import supriya.daw  # noqa

from .Clip import Clip
from .DawMixin import DawMixin


class ClipSlot(UniqueTreeNode, DawMixin):

    ### INITIALIZER ###

    def __init__(self):
        UniqueTreeNode.__init__(self)
        self._children = []
        self._named_children = {}

    ### SPECIAL METHODS ###

    def __contains__(self, item):
        return item in self._children

    ### PUBLIC METHODS ###

    def fire(self):
        application = self.application
        if application is None:
            raise ValueError
        self.parent.parent.fire_clip_slot(self.parent.index(self))

    def set_clip(self, clip: Clip):
        if not isinstance(clip, Clip):
            raise ValueError
        with contextlib.ExitStack() as exit_stack:
            applications = set()
            for item in [self] + self._children:
                if item is None:
                    continue
                application = item.application
                if application is not None:
                    applications.add(application)
            for application in applications:
                self._debug_tree("Locking")
                exit_stack.enter_context(application._lock)
            if self.clip is not None:
                self.clip._set_parent(None)
            if clip is not None:
                clip._set_parent(self)
            self._children.append(clip)

    ### PUBLIC PROPERTIES ###

    @property
    def application(self) -> Optional["supriya.daw.Application"]:
        from .Application import Application

        for parent in self.parentage[1:]:
            if isinstance(parent, Application):
                return parent
        return None

    @property
    def clip(self):
        if self._children:
            return self._children[0]
