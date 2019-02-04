import copy

from supriya.realtime.ControlInterface import ControlInterface


class GroupInterface(ControlInterface):
    """
    Interface to group controls.

    ::

        >>> server = supriya.Server().boot()
        >>> group = supriya.Group().allocate()
        >>> group.extend([
        ...     supriya.Synth(synthdef=supriya.assets.synthdefs.test),
        ...     supriya.Synth(synthdef=supriya.assets.synthdefs.default),
        ...     supriya.Synth(synthdef=supriya.assets.synthdefs.default),
        ...     ])

    ::

        >>> control = group.controls['amplitude']

    ::

        >>> group.controls['frequency'] = 777

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_group_controls",)

    ### INITIALIZER ###

    def __init__(self, client=None):
        self._synth_controls = {}
        self._group_controls = {}
        self._client = client

    ### SPECIAL METHODS ###

    def __contains__(self, item):
        return item in self._synth_controls

    def __getitem__(self, item):
        return self._group_controls[item]

    def __iter__(self):
        return iter(sorted(self._group_controls))

    def __len__(self):
        return len(self._group_controls)

    def __repr__(self):
        class_name = type(self).__name__
        return "<{}: {!r}>".format(class_name, self.client)

    def __setitem__(self, items, values):
        import supriya.realtime

        if not isinstance(items, tuple):
            items = (items,)
        assert all(_ in self._synth_controls for _ in items)
        if not isinstance(values, tuple):
            values = (values,)
        assert len(items) == len(values)
        settings = dict(zip(items, values))
        for key, value in settings.items():
            for synth in self._synth_controls.get(key, ()):
                control = synth.controls[key]
                if isinstance(value, supriya.realtime.Bus):
                    control._map_to_bus(value)
                elif value is None:
                    control._unmap()
                else:
                    control._set_to_number(value)
        requests = self._set(**settings)
        supriya.commands.RequestBundle(contents=requests).communicate(
            server=self.client.server, sync=True
        )

    ### PUBLIC METHODS ###

    def add_controls(self, control_interface_dict):
        import supriya.realtime

        for control_name in control_interface_dict:
            if control_name not in self._synth_controls:
                self._synth_controls[control_name] = copy.copy(
                    control_interface_dict[control_name]
                )
                proxy = supriya.realtime.GroupControl(client=self, name=control_name)
                self._group_controls[control_name] = proxy
            else:
                self._synth_controls[control_name].update(
                    control_interface_dict[control_name]
                )

    def as_dict(self):
        result = {}
        for control_name, node_set in self._synth_controls.items():
            result[control_name] = copy.copy(node_set)
        return result

    def remove_controls(self, control_interface_dict):
        for control_name in control_interface_dict:
            if control_name not in self._synth_controls:
                continue
            current_nodes = self._synth_controls[control_name]
            nodes_to_remove = control_interface_dict[control_name]
            current_nodes.difference_update(nodes_to_remove)
            if not current_nodes:
                del (self._synth_controls[control_name])
                del (self._group_controls[control_name])

    def reset(self):
        self._synth_controls.clear()
