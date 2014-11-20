# -*- encoding: utf-8 -*-
from abjad.tools import documentationtools


class GraphvizDirective(documentationtools.ReSTDirective):
    r'''A ReST Graphviz directive.
    '''

    ### INITIALIZER ###

    def __init__(
        self,
        graph,
        name=None,
        options=None,
        ):
        assert isinstance(graph, documentationtools.GraphvizGraph)
        self._graph = graph
        documentationtools.ReSTDirective.__init__(
            self,
            name=name,
            options=options,
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _children_rest_format_contributions(self):
        result = ['']
        graphviz_format = str(self.graph)
        for line in graphviz_format.splitlines():
            line = '   {}'.format(line)
            result.append(line)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def directive(self):
        r'''Gets directive of ReST Graphviz directive.

        Returns string.
        '''
        return 'graphviz'

    @property
    def graph(self):
        r'''Gets graph of ReST Graphviz directive.

        Returns Graphviz graph.
        '''
        return self._graph