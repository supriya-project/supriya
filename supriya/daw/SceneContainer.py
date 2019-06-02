from typing import Optional

from uqbar.containers import UniqueTreeList

from .Scene import Scene


class SceneContainer(UniqueTreeList):

    ### PUBLIC METHODS ###

    def add_scene(self):
        scene = Scene()
        self.append(scene)
        return scene

    ### PRIVATE PROPERTIES ###

    @property
    def _node_class(self):
        return Scene

    ### PUBLIC PROPERTIES ###

    @property
    def application(self) -> Optional["supriya.daw.Application"]:
        from .Application import Application

        for parent in self.parentage[1:]:
            if isinstance(parent, Application):
                return parent
        return None
