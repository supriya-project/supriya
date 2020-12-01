import uqbar.graphs

from supriya import BinaryOperator, UnaryOperator


class SynthDefGrapher:
    r"""
    Graphs SynthDefs.

    ..  container:: example

        ::

            >>> ugen_graph = supriya.ugens.LFNoise2.ar()
            >>> result = ugen_graph.transpose([0, 3, 7])

        ::

            >>> supriya.graph(result)  # doctest: +SKIP

        ::

            >>> print(format(result.__graph__(), "graphviz"))
            digraph synthdef_c481c3d42e3cfcee0267250247dab51f {
                graph [bgcolor=transparent,
                    color=lightslategrey,
                    dpi=72,
                    fontname=Arial,
                    outputorder=edgesfirst,
                    overlap=prism,
                    penwidth=2,
                    rankdir=LR,
                    ranksep=1,
                    splines=spline,
                    style="dotted, rounded"];
                node [fontname=Arial,
                    fontsize=12,
                    penwidth=2,
                    shape=Mrecord,
                    style="filled, rounded"];
                edge [penwidth=2];
                ugen_0 [fillcolor=lightsteelblue2,
                    label="<f_0> LFNoise2\n(audio) | { { <f_1_0_0> frequency:\n500.0 } | { <f_1_1_0> 0 } }"];
                ugen_1 [fillcolor=lightsteelblue2,
                    label="<f_0> UnaryOpUGen\n[HZ_TO_MIDI]\n(audio) | { { <f_1_0_0> source } | { <f_1_1_0> 0 } }"];
                ugen_2 [fillcolor=lightsteelblue2,
                    label="<f_0> UnaryOpUGen\n[MIDI_TO_HZ]\n(audio) | { { <f_1_0_0> source } | { <f_1_1_0> 0 } }"];
                ugen_3 [fillcolor=lightsteelblue2,
                    label="<f_0> BinaryOpUGen\n[ADDITION]\n(audio) | { { <f_1_0_0> left | <f_1_0_1> right:\n3.0 } | { <f_1_1_0> 0 } }"];
                ugen_4 [fillcolor=lightsteelblue2,
                    label="<f_0> UnaryOpUGen\n[MIDI_TO_HZ]\n(audio) | { { <f_1_0_0> source } | { <f_1_1_0> 0 } }"];
                ugen_5 [fillcolor=lightsteelblue2,
                    label="<f_0> BinaryOpUGen\n[ADDITION]\n(audio) | { { <f_1_0_0> left | <f_1_0_1> right:\n7.0 } | { <f_1_1_0> 0 } }"];
                ugen_6 [fillcolor=lightsteelblue2,
                    label="<f_0> UnaryOpUGen\n[MIDI_TO_HZ]\n(audio) | { { <f_1_0_0> source } | { <f_1_1_0> 0 } }"];
                ugen_0:f_1_1_0:e -> ugen_1:f_1_0_0:w [color=steelblue];
                ugen_1:f_1_1_0:e -> ugen_2:f_1_0_0:w [color=steelblue];
                ugen_1:f_1_1_0:e -> ugen_3:f_1_0_0:w [color=steelblue];
                ugen_1:f_1_1_0:e -> ugen_5:f_1_0_0:w [color=steelblue];
                ugen_3:f_1_1_0:e -> ugen_4:f_1_0_0:w [color=steelblue];
                ugen_5:f_1_1_0:e -> ugen_6:f_1_0_0:w [color=steelblue];
            }

    """

    ### PRIVATE METHODS ###

    @staticmethod
    def _connect_nodes(synthdef, ugen_node_mapping):
        import supriya.synthdefs

        for ugen in synthdef.ugens:
            tail_node = ugen_node_mapping[ugen]
            for i, input_ in enumerate(ugen.inputs):
                if not isinstance(input_, supriya.synthdefs.OutputProxy):
                    continue
                tail_field = tail_node["inputs"][i]
                source = input_.source
                head_node = ugen_node_mapping[source]
                head_field = head_node["outputs"][input_.output_index]
                edge = uqbar.graphs.Edge(head_port_position="w", tail_port_position="e")
                edge.attach(head_field, tail_field)
                if source.calculation_rate == supriya.CalculationRate.CONTROL:
                    edge.attributes["color"] = "goldenrod"
                elif source.calculation_rate == supriya.CalculationRate.AUDIO:
                    edge.attributes["color"] = "steelblue"
                else:
                    edge.attributes["color"] = "salmon"

    @staticmethod
    def _create_ugen_input_group(ugen, ugen_index):
        if not ugen.inputs:
            return None
        input_group = uqbar.graphs.RecordGroup(name="inputs")
        for i, input_ in enumerate(ugen.inputs):
            label = ""
            input_name = None
            if i < len(ugen._ordered_input_names):
                input_name = tuple(ugen._ordered_input_names)[i]
            if input_name:
                # input_name = r'\n'.join(input_name.split('_'))
                if isinstance(input_, float):
                    label = r"{}:\n{}".format(input_name, input_)
                else:
                    label = input_name
            elif isinstance(input_, float):
                label = str(input_)
            label = label or None
            field = uqbar.graphs.RecordField(
                label=label, name="ugen_{}_input_{}".format(ugen_index, i)
            )
            input_group.append(field)
        return input_group

    @staticmethod
    def _create_ugen_node_mapping(synthdef):
        import supriya.synthdefs

        ugen_node_mapping = {}
        for ugen in synthdef.ugens:
            ugen_index = synthdef.ugens.index(ugen)
            node = uqbar.graphs.Node(name="ugen_{}".format(ugen_index))
            if ugen.calculation_rate == supriya.CalculationRate.CONTROL:
                node.attributes["fillcolor"] = "lightgoldenrod2"
            elif ugen.calculation_rate == supriya.CalculationRate.AUDIO:
                node.attributes["fillcolor"] = "lightsteelblue2"
            else:
                node.attributes["fillcolor"] = "lightsalmon2"
            title_field = SynthDefGrapher._create_ugen_title_field(ugen)
            node.append(title_field)
            group = uqbar.graphs.RecordGroup()
            input_group = SynthDefGrapher._create_ugen_input_group(ugen, ugen_index)
            if input_group is not None:
                group.append(input_group)
            output_group = SynthDefGrapher._create_ugen_output_group(
                synthdef, ugen, ugen_index
            )
            if output_group is not None:
                group.append(output_group)
            node.append(group)
            ugen_node_mapping[ugen] = node
        return ugen_node_mapping

    @staticmethod
    def _create_ugen_output_group(synthdef, ugen, ugen_index):
        import supriya.ugens

        if not ugen.outputs:
            return None
        output_group = uqbar.graphs.RecordGroup(name="outputs")
        for i, output in enumerate(ugen.outputs):
            label = str(i)
            if isinstance(ugen, supriya.synthdefs.Control):
                parameter_index = ugen.special_index + i
                parameter = dict(synthdef.indexed_parameters)[parameter_index]
                parameter_name = parameter.name
                # parameter_name = r'\n'.join(parameter.name.split('_'))
                label = r"{}:\n{}".format(parameter_name, parameter.value)
            field = uqbar.graphs.RecordField(
                label=label, name="ugen_{}_output_{}".format(ugen_index, i)
            )
            output_group.append(field)
        return output_group

    @staticmethod
    def _create_ugen_title_field(ugen):
        import supriya.synthdefs
        import supriya.ugens

        name = type(ugen).__name__
        calculation_rate = ugen.calculation_rate.name.lower()
        label_template = r"{name}\n({calculation_rate})"
        operator = None
        if isinstance(ugen, supriya.synthdefs.BinaryOpUGen):
            operator = BinaryOperator(ugen.special_index).name
            label_template = r"{name}\n[{operator}]\n({calculation_rate})"
        elif isinstance(ugen, supriya.synthdefs.UnaryOpUGen):
            operator = UnaryOperator(ugen.special_index).name
            label_template = r"{name}\n[{operator}]\n({calculation_rate})"
        title_field = uqbar.graphs.RecordField(
            label=label_template.format(
                name=name, operator=operator, calculation_rate=calculation_rate
            )
        )
        return title_field

    @staticmethod
    def _style_graph(graph):
        graph.attributes.update(
            {
                "bgcolor": "transparent",
                "color": "lightslategrey",
                "dpi": 72,
                "fontname": "Arial",
                "outputorder": "edgesfirst",
                "overlap": "prism",
                "penwidth": 2,
                "rankdir": "LR",
                "ranksep": 1,
                "splines": "spline",
                "style": ("dotted", "rounded"),
            }
        )
        graph.edge_attributes.update({"penwidth": 2})
        graph.node_attributes.update(
            {
                "fontname": "Arial",
                "fontsize": 12,
                "penwidth": 2,
                "shape": "Mrecord",
                "style": ("filled", "rounded"),
            }
        )

    ### PUBLIC METHODS ###

    @staticmethod
    def graph(synthdef):
        import supriya.synthdefs

        assert isinstance(synthdef, supriya.synthdefs.SynthDef)
        graph = uqbar.graphs.Graph(name="synthdef_{}".format(synthdef.actual_name))
        ugen_node_mapping = SynthDefGrapher._create_ugen_node_mapping(synthdef)
        for node in sorted(ugen_node_mapping.values(), key=lambda x: x.name):
            graph.append(node)
        SynthDefGrapher._connect_nodes(synthdef, ugen_node_mapping)
        SynthDefGrapher._style_graph(graph)
        return graph
