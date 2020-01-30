import contextlib
import logging
from typing import Optional, cast

import supriya.daw  # noqa
from supriya.realtime.nodes import Node

from .MixerContext import MixerContext

logger = logging.getLogger("supriya.daw")


class DawMixin:
    def __init__(self):
        self._node = None

    ### PRIVATE METHODS ###

    def _debug_tree(self, prefix, suffix=None):
        message = (
            f"{(prefix + ':').ljust(15)} {'..' * self.depth} {type(self).__name__}"
            f"{' (' + self.node.name + ')' if getattr(self, 'node', None) else ''}"
        )
        if suffix:
            message += " " + suffix
        logger.debug(message)

    ### PUBLIC METHODS ###

    @classmethod
    @contextlib.contextmanager
    def lock_applications(cls, nodes=None):
        with contextlib.ExitStack() as exit_stack:
            applications = set()
            for node in nodes:
                if node is None:
                    continue
                application = node.application
                if application is not None:
                    applications.add(application)
            for application in applications:
                exit_stack.enter_context(application._lock)
            yield

    ### PUBLIC PROPERTIES ###

    @property
    def application(self) -> Optional["supriya.daw.Application"]:
        from .Application import Application

        for parent in cast("supriya.daw.DawNode", self).parentage[1:]:
            if isinstance(parent, Application):
                return parent
        return None

    @property
    def mixer_context(self) -> Optional[MixerContext]:
        for parent in cast("supriya.daw.DawNode", self).parentage[1:]:
            if isinstance(parent, MixerContext):
                return parent
        return None

    @property
    def node(self) -> Optional[Node]:
        return cast("supriya.daw.DawNode", self)._node

    @property
    def transport(self):
        application = self.application
        if application is None:
            return None
        return application.transport
