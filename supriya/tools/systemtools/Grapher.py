# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class Grapher(SupriyaObject):

    @staticmethod
    def _style_graph(graph):
        graph.attributes.update({
            'bgcolor': 'transparent',
            'color': 'lightslategrey',
            'dpi': 72,
            'fontname': 'Arial',
            'outputorder': 'edgesfirst',
            'overlap': 'prism',
            'penwidth': 2,
            'rankdir': 'LR',
            'ranksep': 1,
            'splines': 'spline',
            'style': ('dotted', 'rounded'),
            })
        graph.edge_attributes.update({
            'penwidth': 2,
            })
        graph.node_attributes.update({
            'fontname': 'Arial',
            'fontsize': 12,
            'penwidth': 2,
            'shape': 'Mrecord',
            'style': ('filled', 'rounded'),
            })
