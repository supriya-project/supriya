# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class SynthDefGrapher(SupriyaObject):

    ### PRIVATE METHODS ###

    @staticmethod
    def _connect_nodes(synthdef, ugen_node_mapping):
        from abjad.tools import documentationtools
        from supriya.tools import synthdeftools
        for ugen in synthdef.ugens:
            tail_node = ugen_node_mapping[ugen]
            for i, input_ in enumerate(ugen.inputs):
                if not isinstance(input_, synthdeftools.OutputProxy):
                    continue
                tail_field = tail_node['inputs'][i]
                head_node = ugen_node_mapping[input_.source]
                head_field = head_node['outputs'][input_.output_index]
                edge = documentationtools.GraphvizEdge()
                edge(head_field, tail_field)
                edge.head_port_position = 'n'
                edge.tail_port_position = 's'

    @staticmethod
    def _create_ugen_input_group(ugen, ugen_index):
        from abjad.tools import documentationtools
        if not ugen.inputs:
            return None
        input_group = documentationtools.GraphvizGroup(
            name='inputs'.format(ugen_index),
            )
        for i, input_ in enumerate(ugen.inputs):
            label = ''
            input_name = None
            if i < len(ugen._ordered_input_names):
                input_name = ugen._ordered_input_names[i]
            if input_name:
                if '_' in input_name:
                    input_name = r'\n'.join(input_name.split('_'))
                if isinstance(input_, float):
                    label = r'{}:\n{}'.format(input_name, input_)
                else:
                    label = input_name
            elif isinstance(input_, float):
                label = str(input_)
            label = label or None
            field = documentationtools.GraphvizField(
                label=label,
                name='ugen_{}_input_{}'.format(ugen_index, i),
                )
            input_group.append(field)
        return input_group

    @staticmethod
    def _create_ugen_node_mapping(synthdef):
        from abjad.tools import documentationtools
        ugen_node_mapping = {}
        for ugen in synthdef.ugens:
            ugen_index = synthdef.ugens.index(ugen)
            node = documentationtools.GraphvizNode(
                name='ugen_{}'.format(ugen_index),
                )
            group = documentationtools.GraphvizGroup()
            input_group = SynthDefGrapher._create_ugen_input_group(
                ugen, ugen_index)
            if input_group is not None:
                group.append(input_group)
            title_field = SynthDefGrapher._create_ugen_title_field(ugen)
            group.append(title_field)
            output_group = SynthDefGrapher._create_ugen_output_group(
                synthdef, ugen, ugen_index)
            if output_group is not None:
                group.append(output_group)
            node.append(group)
            ugen_node_mapping[ugen] = node
        return ugen_node_mapping

    @staticmethod
    def _create_ugen_output_group(synthdef, ugen, ugen_index):
        from abjad.tools import documentationtools
        from supriya.tools import ugentools
        if not ugen.outputs:
            return None
        output_group = documentationtools.GraphvizGroup(
            name='outputs'.format(ugen_index),
            )
        for i, output in enumerate(ugen.outputs):
            label = str(i)
            if isinstance(ugen, ugentools.Control):
                parameter_index = ugen.special_index + i
                parameter = synthdef.parameters[parameter_index]
                label = r'{}:\n{}'.format(
                    r'\n'.join(parameter.name.split('_')),
                    parameter.value,
                    )
            field = documentationtools.GraphvizField(
                label=label,
                name='ugen_{}_output_{}'.format(ugen_index, i),
                )
            output_group.append(field)
        return output_group

    @staticmethod
    def _create_ugen_title_field(ugen):
        from abjad.tools import documentationtools
        title_field = documentationtools.GraphvizField(
            label='{}.{}'.format(
                type(ugen).__name__,
                ugen.rate.name.lower(),
                ),
            )
        return title_field

    @staticmethod
    def _style_graph(graph):
        graph.node_attributes['shape'] = 'Mrecord'

    ### PUBLIC METHODS ###

    @staticmethod
    def graph(synthdef):
        from abjad.tools import documentationtools
        from supriya.tools import synthdeftools
        assert isinstance(synthdef, synthdeftools.SynthDef)
        graph = documentationtools.GraphvizGraph(
            name='synthdef_{}'.format(synthdef.actual_name),
            )
        ugen_node_mapping = SynthDefGrapher._create_ugen_node_mapping(synthdef)
        for node in ugen_node_mapping.values():
            graph.append(node)
        SynthDefGrapher._connect_nodes(synthdef, ugen_node_mapping)
        SynthDefGrapher._style_graph(graph)
        return graph
