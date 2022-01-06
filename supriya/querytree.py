from collections.abc import Sequence

from supriya import ParameterRate
from supriya.system import SupriyaValueObject


class QueryTreeControl(SupriyaValueObject):

    ### CLASS VARIABLES ###

    __slots__ = ("_control_value", "_control_name_or_index")

    ### INITIALIZER ###

    def __init__(self, control_name_or_index=None, control_value=None):
        self._control_value = control_value
        self._control_name_or_index = control_name_or_index

    ### SPECIAL METHODS ###

    def __str__(self):
        key = self._control_name_or_index
        value = self._control_value
        try:
            value = round(value, 6)
        except Exception:
            pass
        string = "{}: {!s}".format(key, value)
        return string

    ### PUBLIC METHODS ###

    @classmethod
    def from_control(cls, control):
        import supriya.realtime

        control_name = control.name
        if isinstance(control.value, supriya.realtime.Bus):
            control_value = str(control.value)
        else:
            control_value = float(control.value)
        return cls(control_value=control_value, control_name_or_index=control_name)

    ### PUBLIC PROPERTIES ###

    @property
    def control_name_or_index(self):
        return self._control_name_or_index

    @property
    def control_value(self):
        return self._control_value


class QueryTreeSynth(SupriyaValueObject, Sequence):

    ### CLASS VARIABLES ###

    __slots__ = ("_controls", "_extra", "_name", "_node_id", "_synthdef_name")

    ### INITIALIZER ###

    def __init__(
        self, node_id=None, synthdef_name=None, controls=None, name=None, **extra
    ):
        self._controls = controls
        self._extra = tuple(sorted(extra.items()))
        self._node_id = node_id
        self._synthdef_name = synthdef_name
        self._name = name

    ### SPECIAL METHODS ###

    def __format__(self, format_spec):
        result = self._get_str_format_pieces(unindexed=format_spec == "unindexed")
        result = "\n".join(result)
        return result

    def __getitem__(self, item):
        return self._controls[item]

    def __len__(self):
        return len(self._controls)

    def __str__(self):
        result = self._get_str_format_pieces()
        result = "\n".join(result)
        return result

    ### PRIVATE METHODS ###

    @classmethod
    def _from_nrt_synth(
        cls,
        state,
        node,
        include_controls=False,
        include_timespans=False,
        id_mapping=None,
    ):
        from supriya.nonrealtime import Bus, BusGroup, Synth
        from supriya.synthdefs import SynthDef

        assert isinstance(node, Synth)
        node_id = node.session_id
        synthdef_name = node.synthdef
        if isinstance(synthdef_name, SynthDef):
            synthdef_name = synthdef_name.actual_name
        controls = []
        if include_controls:
            settings = node._collect_settings(
                state.offset, persistent=True, id_mapping=id_mapping
            )
            synthdef, synth_kwargs = node.synthdef, node.synth_kwargs
            for name, parameter in sorted(synthdef.parameters.items()):
                value = parameter.value
                if name in synth_kwargs:
                    value = synth_kwargs[name]
                if name in settings:
                    value = settings[name]
                if (
                    parameter.parameter_rate == ParameterRate.SCALAR
                    or parameter.name in ("in_", "out")
                ):
                    if value in id_mapping:
                        value = id_mapping[value]
                    value = float(value)
                elif isinstance(value, (Bus, BusGroup)) and value in id_mapping:
                    value = value.get_map_symbol(id_mapping[value])
                else:
                    value = float(value)
                control = QueryTreeControl(
                    control_name_or_index=name, control_value=value
                )
                controls.append(control)
        extra = {}
        if include_timespans:
            extra.update(timespan=[node.start_offset, node.stop_offset])
        query_tree_synth = QueryTreeSynth(
            node_id=node_id, synthdef_name=synthdef_name, controls=controls, **extra
        )
        return query_tree_synth

    def _get_str_format_pieces(self, unindexed=False):
        result = []
        node_id = self.node_id
        if unindexed:
            node_id = "..."
        string = f"{node_id} {self.synthdef_name}"
        if self.name:
            string += f" ({self.name})"
        if self.extra:
            string += (
                " ("
                + ", ".join("{}: {}".format(key, value) for key, value in self.extra)
                + ")"
            )
        result.append(string)
        if self.controls:
            control_string = ", ".join(str(control) for control in self.controls)
            control_string = "    " + control_string
            result.append(control_string)
        return result

    ### PUBLIC METHODS ###

    def annotate(self, annotation_map):
        return type(self)(
            node_id=self.node_id,
            controls=self.controls,
            synthdef_name=self.synthdef_name,
            name=annotation_map.get(self.node_id),
            **dict(self.extra),
        )

    @classmethod
    def from_response(cls, response):
        return cls(
            node_id=response.node_id,
            controls=[
                QueryTreeControl(control_name_or_index=name, control_value=value)
                for name, value in (response.synthdef_controls.items() or {})
            ],
            synthdef_name=response.synthdef_name,
        )

    @classmethod
    def from_synth(cls, synth, include_controls=False):
        import supriya.commands
        import supriya.realtime
        import supriya.synthdefs

        assert isinstance(synth, supriya.realtime.Synth)
        node_id = synth.node_id
        synthdef_name = synth.synthdef
        if isinstance(synthdef_name, supriya.synthdefs.SynthDef):
            synthdef_name = synthdef_name.actual_name
        controls = []
        if include_controls:
            for control_name in synth:
                control = QueryTreeControl.from_control(synth.controls[control_name])
                controls.append(control)
        query_tree_synth = QueryTreeSynth(
            node_id=node_id, synthdef_name=synthdef_name, controls=tuple(controls)
        )
        return query_tree_synth

    def to_dict(self):
        """
        Convert QueryTreeSynth to JSON-serializable dictionary.

        ::

            >>> query_tree_synth = supriya.querytree.QueryTreeSynth(
            ...     node_id=1001,
            ...     synthdef_name="c1aa521afab5b0c0ce3d744690951649",
            ...     controls=(
            ...         supriya.querytree.QueryTreeControl(
            ...             control_name_or_index="level",
            ...             control_value=1.0,
            ...         ),
            ...         supriya.querytree.QueryTreeControl(
            ...             control_name_or_index="out",
            ...             control_value=0.0,
            ...         ),
            ...     ),
            ... )

        ::

            >>> import json
            >>> result = query_tree_synth.to_dict()
            >>> result = json.dumps(
            ...     result,
            ...     indent=4,
            ...     separators=(",", ": "),
            ...     sort_keys=True,
            ... )
            >>> print(result)
            {
                "controls": {
                    "level": 1.0,
                    "out": 0.0
                },
                "node_id": 1001,
                "synthdef": "c1aa521afab5b0c0ce3d744690951649"
            }

        """
        result = {
            "node_id": self.node_id,
            "synthdef": self.synthdef_name,
            "controls": {},
        }
        for control in self.controls:
            name = control.control_name_or_index
            result["controls"][name] = control.control_value
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def controls(self):
        return self._controls

    @property
    def extra(self):
        return self._extra

    @property
    def name(self):
        return self._name

    @property
    def node_id(self):
        return self._node_id

    @property
    def synthdef_name(self):
        return self._synthdef_name


class QueryTreeGroup(SupriyaValueObject, Sequence):

    ### CLASS VARIABLES ###

    __slots__ = ("_children", "_extra", "_name", "_node_id")

    ### INITIALIZER ###

    def __init__(self, node_id=None, children=None, name=None, **extra):
        self._children = tuple(children or ())
        self._extra = tuple(sorted(extra.items()))
        self._node_id = node_id
        self._name = name

    ### SPECIAL METHODS ###

    def __format__(self, format_spec):
        result = self._get_str_format_pieces(unindexed=format_spec == "unindexed")
        result = "\n".join(result)
        result = "NODE TREE {}".format(result)
        return result

    def __getitem__(self, item):
        return self._children[item]

    def __len__(self):
        return len(self._children)

    def __str__(self):
        result = self._get_str_format_pieces()
        result = "\n".join(result)
        result = "NODE TREE {}".format(result)
        return result

    ### PRIVATE METHODS ###

    @classmethod
    def _from_nrt_group(
        cls,
        state,
        node,
        include_controls=False,
        include_timespans=False,
        id_mapping=None,
    ):
        import supriya.commands
        import supriya.nonrealtime

        assert isinstance(node, supriya.nonrealtime.Group)
        node_id = node.session_id
        children = []
        for child in state.nodes_to_children.get(node) or ():
            if isinstance(child, supriya.nonrealtime.Group):
                child = QueryTreeGroup._from_nrt_group(
                    state,
                    child,
                    include_controls=include_controls,
                    include_timespans=include_timespans,
                    id_mapping=id_mapping,
                )
            elif isinstance(child, supriya.nonrealtime.Synth):
                child = QueryTreeSynth._from_nrt_synth(
                    state,
                    child,
                    include_controls=include_controls,
                    include_timespans=include_timespans,
                    id_mapping=id_mapping,
                )
            else:
                raise ValueError(child)
            children.append(child)
        children = tuple(children)
        extra = {}
        if include_timespans:
            extra.update(timespan=[node.start_offset, node.stop_offset])
        query_tree_group = QueryTreeGroup(node_id=node_id, children=children, **extra)
        return query_tree_group

    def _get_str_format_pieces(self, unindexed=False):
        result = []
        node_id = self.node_id
        if unindexed:
            node_id = "..."
        string = f"{node_id} group"
        if self.name:
            string += f" ({self.name})"
        if self.extra:
            string += (
                " ("
                + ", ".join("{}: {}".format(key, value) for key, value in self.extra)
                + ")"
            )
        result.append(string)
        for child in self.children:
            for line in child._get_str_format_pieces(unindexed=unindexed):
                result.append("    {}".format(line))
        return result

    ### PUBLIC METHODS ###

    def annotate(self, annotation_map):
        return type(self)(
            node_id=self.node_id,
            children=[child.annotate(annotation_map) for child in self.children],
            name=annotation_map.get(self.node_id),
            **dict(self.extra),
        )

    @classmethod
    def from_group(cls, group, include_controls=False):
        import supriya.commands
        import supriya.realtime

        assert isinstance(group, supriya.realtime.Group)
        node_id = group.node_id
        children = []
        for child in group.children:
            if isinstance(child, supriya.realtime.Group):
                child = QueryTreeGroup.from_group(
                    child, include_controls=include_controls
                )
            elif isinstance(child, supriya.realtime.Synth):
                child = QueryTreeSynth.from_synth(
                    child, include_controls=include_controls
                )
            else:
                raise ValueError(child)
            children.append(child)
        children = tuple(children)
        query_tree_group = QueryTreeGroup(node_id=node_id, children=children)
        return query_tree_group

    @classmethod
    def from_response(cls, response):
        return cls(node_id=response.node_id)

    @classmethod
    def from_state(cls, state, include_controls=False, include_timespans=False):
        id_mapping = state.session._build_id_mapping()
        root_node = state.session.root_node
        query_tree_group = cls._from_nrt_group(
            state,
            root_node,
            include_controls=include_controls,
            include_timespans=include_timespans,
            id_mapping=id_mapping,
        )
        return query_tree_group

    def to_dict(self):
        """
        Convert QueryTreeGroup to JSON-serializable dictionary.

        ::

            >>> query_tree_group = supriya.querytree.QueryTreeGroup(
            ...     node_id=1002,
            ...     children=(
            ...         supriya.querytree.QueryTreeSynth(
            ...             node_id=1105,
            ...             synthdef_name="dca557070c6b57164557041ac746fb3f",
            ...             controls=(
            ...                 supriya.querytree.QueryTreeControl(
            ...                     control_name_or_index="damping",
            ...                     control_value=0.06623425334692,
            ...                 ),
            ...                 supriya.querytree.QueryTreeControl(
            ...                     control_name_or_index="duration",
            ...                     control_value=3.652155876159668,
            ...                 ),
            ...                 supriya.querytree.QueryTreeControl(
            ...                     control_name_or_index="level",
            ...                     control_value=0.894767701625824,
            ...                 ),
            ...                 supriya.querytree.QueryTreeControl(
            ...                     control_name_or_index="out",
            ...                     control_value=16.0,
            ...                 ),
            ...                 supriya.querytree.QueryTreeControl(
            ...                     control_name_or_index="room_size",
            ...                     control_value=0.918643176555634,
            ...                 ),
            ...             ),
            ...         ),
            ...         supriya.querytree.QueryTreeSynth(
            ...             node_id=1098,
            ...             synthdef_name="cc754c63533fdcf412a44ef6adb1a8f0",
            ...             controls=(
            ...                 supriya.querytree.QueryTreeControl(
            ...                     control_name_or_index="duration",
            ...                     control_value=5.701356887817383,
            ...                 ),
            ...                 supriya.querytree.QueryTreeControl(
            ...                     control_name_or_index="level",
            ...                     control_value=0.959683060646057,
            ...                 ),
            ...                 supriya.querytree.QueryTreeControl(
            ...                     control_name_or_index="out",
            ...                     control_value=16.0,
            ...                 ),
            ...                 supriya.querytree.QueryTreeControl(
            ...                     control_name_or_index="pitch_dispersion",
            ...                     control_value=0.040342573076487,
            ...                 ),
            ...                 supriya.querytree.QueryTreeControl(
            ...                     control_name_or_index="pitch_shift",
            ...                     control_value=10.517594337463379,
            ...                 ),
            ...                 supriya.querytree.QueryTreeControl(
            ...                     control_name_or_index="time_dispersion",
            ...                     control_value=0.666014134883881,
            ...                 ),
            ...                 supriya.querytree.QueryTreeControl(
            ...                     control_name_or_index="window_size",
            ...                     control_value=1.014111995697021,
            ...                 ),
            ...             ),
            ...         ),
            ...     ),
            ... )

        ::

            >>> import json
            >>> result = query_tree_group.to_dict()
            >>> result = json.dumps(
            ...     result,
            ...     indent=4,
            ...     separators=(",", ": "),
            ...     sort_keys=True,
            ... )
            >>> print(result)
            {
                "children": [
                    {
                        "controls": {
                            "damping": 0.06623425334692,
                            "duration": 3.652155876159668,
                            "level": 0.894767701625824,
                            "out": 16.0,
                            "room_size": 0.918643176555634
                        },
                        "node_id": 1105,
                        "synthdef": "dca557070c6b57164557041ac746fb3f"
                    },
                    {
                        "controls": {
                            "duration": 5.701356887817383,
                            "level": 0.959683060646057,
                            "out": 16.0,
                            "pitch_dispersion": 0.040342573076487,
                            "pitch_shift": 10.517594337463379,
                            "time_dispersion": 0.666014134883881,
                            "window_size": 1.014111995697021
                        },
                        "node_id": 1098,
                        "synthdef": "cc754c63533fdcf412a44ef6adb1a8f0"
                    }
                ],
                "node_id": 1002
            }

        """
        result = {
            "node_id": self.node_id,
            "children": [x.to_dict() for x in self.children],
        }
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def children(self):
        return self._children

    @property
    def extra(self):
        return self._extra

    @property
    def name(self):
        return self._name

    @property
    def node_id(self):
        return self._node_id
