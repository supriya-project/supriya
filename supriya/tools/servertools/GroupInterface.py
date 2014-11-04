# -*- encoding: utf-8 -*-
import copy
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class GroupInterface(SupriyaObject):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Server Internals'

    __slots__ = (
        '_synth_controls',
        '_client',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        client=None,
        ):
        self._synth_controls = {}
        self._client = client

    ### PUBLIC METHODS ###

    def add_controls(self, control_interface_dict):
        for control_name in control_interface_dict:
            if control_name not in self._synth_controls:
                self._synth_controls[control_name] = copy.copy(
                    control_interface_dict[control_name])
            else:
                self._synth_controls[control_name].update(
                    control_interface_dict[control_name])

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
                del(self._synth_controls[control_name])

    def reset(self):
        self._synth_controls.clear()

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        return self._client

    @property
    def node_id(self):
        return int(self.client)
