from abjad.tools import documentationtools


class ConcreteReSTDirective(documentationtools.ReSTDirective):

    ### INITIALIZER ###

    def __init__(
        self,
        argument=None,
        children=None,
        directive=None,
        name=None,
        options=None,
        ):
        documentationtools.ReSTDirective.__init__(
            self,
            argument=argument,
            children=children,
            name=name,
            options=options,
            )
        self._directive = directive

    ### PUBLIC PROPERTIES ###

    @property
    def directive(self):
        return self._directive