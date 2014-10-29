# -*- encoding: utf-8 -*-
from abjad.tools import documentationtools


class GraphvizDirective(documentationtools.ReSTDirective):

    ### INITIALIZER ###

    def __init__(self, graph, name=None):
        assert isinstance(graph, documentationtools.GraphvizGraph)
        self._graph = graph
        documentationtools.ReSTDirective.__init__(
            self,
            name=name,
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
        return 'graphviz'

    @property
    def graph(self):
        return self._graph