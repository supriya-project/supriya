# -*- encoding: utf-8 -*-
import copy
from supriya.tools.servertools.ControlInterface import ControlInterface


class GroupInterface(ControlInterface):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        client=None,
        ):
        self._synth_controls = {}
        self._client = client

    ### SPECIAL METHODS ###

    def __setitem__(self, items, values):
        pass

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