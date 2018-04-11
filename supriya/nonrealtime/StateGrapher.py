import uqbar.graphs
from supriya.system.Grapher import Grapher


class StateGrapher(Grapher):
    """
    Graphs non-realtime sessions via .
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Session Internals'

    ### PRIVATE METHODS ###

    @staticmethod
    def _create_graphviz_table_cell(label, with_rule=False, **kwargs):
        attributes = {'border': 0}
        attributes.update(**kwargs)
        cell = uqbar.graphs.TableCell(
            label,
            attributes=attributes
            )
        row = uqbar.graphs.TableRow(children=[cell])
        if with_rule:
            rule = uqbar.graphs.HRule()
            return [rule, row]
        return [row]

    @staticmethod
    def _create_graphviz_node(label, **kwargs):
        node = uqbar.graphs.Node(attributes={'margin': 0.05})
        table_attributes = {
            'border': 2,
            'cellborder': 0,
            'cellpadding': 5,
            'cellspacing': 0,
            }
        table_attributes.update(**kwargs)
        table = uqbar.graphs.Table(
            attributes=table_attributes,
            )
        table.extend(StateGrapher._create_graphviz_table_cell(label))
        node.append(table)
        return node

    @staticmethod
    def _create_root_node_node(state, nrt_node):
        label = r'Root:0'
        graphviz_node = StateGrapher._create_graphviz_node(
            label,
            bgcolor='lightsalmon2',
            )
        return graphviz_node

    @staticmethod
    def _create_group_node(state, nrt_node, include_controls=False):
        label = r'G:{}'.format(nrt_node.session_id)
        graphviz_node = StateGrapher._create_graphviz_node(
            label,
            bgcolor='lightgoldenrod2',
            )
        if include_controls:
            all_settings = nrt_node._collect_settings(state.offset, persistent=True)
            new_settings = nrt_node._collect_settings(state.offset, persistent=False)
            for name, value in all_settings.items():
                kwargs = {'cellpadding': 2}
                if name in new_settings:
                    kwargs['bgcolor'] = 'goldenrod2'
                try:
                    value = float(value)
                except Exception:
                    pass
                label = '<FONT POINT-SIZE="8">{}: {}</FONT>'.format(name, value)
                graphviz_node[0].extend(
                    StateGrapher._create_graphviz_table_cell(
                        label, with_rule=True, **kwargs),
                    )
        label = '{}:{}'.format(
            nrt_node.start_offset,
            nrt_node.stop_offset,
            )
        graphviz_node[0].extend(
            StateGrapher._create_graphviz_table_cell(label, with_rule=True),
            )
        return graphviz_node

    @staticmethod
    def _create_synth_node(state, nrt_node, include_controls=False):
        label = r'S:{}<BR/>({})'.format(
            nrt_node.session_id,
            nrt_node.synthdef.anonymous_name[:7],
            )
        graphviz_node = StateGrapher._create_graphviz_node(
            label,
            bgcolor='lightsteelblue2',
            )
        if include_controls:
            all_settings = nrt_node._collect_settings(state.offset, persistent=True)
            new_settings = nrt_node._collect_settings(state.offset, persistent=False)
            synthdef, synth_kwargs = nrt_node.synthdef, nrt_node.synth_kwargs
            for name, parameter in sorted(synthdef.parameters.items()):
                kwargs = {'cellpadding': 2}
                value = parameter.value
                if nrt_node.start_offset == state.offset:
                    if name in synth_kwargs:
                        value = synth_kwargs[name]
                        kwargs['bgcolor'] = 'steelblue2'
                if name in all_settings:
                    value = all_settings[name]
                if name in new_settings:
                    kwargs['bgcolor'] = 'steelblue2'
                try:
                    value = float(value)
                except Exception:
                    pass
                label = '<FONT POINT-SIZE="8">{}: {}</FONT>'.format(name, value)
                graphviz_node[0].extend(
                    StateGrapher._create_graphviz_table_cell(
                        label, with_rule=True, **kwargs),
                    )
        label = '{}:{}'.format(
            nrt_node.start_offset,
            nrt_node.stop_offset,
            )
        graphviz_node[0].extend(
            StateGrapher._create_graphviz_table_cell(label, with_rule=True)
            )
        return graphviz_node

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
            'rankdir': 'TB',
            'ranksep': 0.5,
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
            'shape': 'none',
            'style': 'rounded',
            })

    @staticmethod
    def graph(state, include_controls=False):
        import supriya.nonrealtime
        subgraph = uqbar.graphs.Graph(is_cluster=True)
        graph = uqbar.graphs.Graph(children=[subgraph])
        node_mapping = {}
        root_node = state.session.root_node
        graphviz_root_node = StateGrapher._create_root_node_node(
            state, root_node)
        node_mapping[root_node] = graphviz_root_node
        graph.append(graphviz_root_node)
        for parent, child in state._iterate_node_pairs(
            root_node, state.nodes_to_children):
            if isinstance(child, supriya.nonrealtime.Group):
                graphviz_child = StateGrapher._create_group_node(
                    state,
                    child,
                    include_controls=include_controls,
                    )
                graph.append(graphviz_child)
            else:
                graphviz_child = StateGrapher._create_synth_node(
                    state,
                    child,
                    include_controls=include_controls,
                    )
                subgraph.append(graphviz_child)
            node_mapping[child] = graphviz_child
            node_mapping[parent].attach(graphviz_child)
        StateGrapher._style_graph(graph)
        return graph
