# -*- encoding: utf-8 -*-
import collections
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class SynthControlGroup(SupriyaObject, collections.Mapping):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_synthdef',
        '_synth_controls',
        '_synth_control_map',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        synthdef,
        ):
        from supriya.tools import servertools
        synth_controls = []
        synth_control_map = collections.OrderedDict()
        for parameter in synthdef.parameters:
            synth_control = servertools.SynthControl.from_parameter(parameter)
            synth_controls.append(synth_control)
            synth_control_map[synth_control.name] = synth_control
        self._synth_controls = tuple(synth_controls)
        self._synth_control_map = synth_control_map

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        if isinstance(item, (int, slice)):
            return self._synth_controls[item]
        elif isinstance(item, str):
            return self._synth_control_map[item]
        elif isinstance(item, tuple):
            result = []
            for x in item:
                result.append(self.__getitem__(x))
            return tuple(result)
        return ValueError(item)

    ### PUBLIC PROPERTIES ###

    @property
    def synthdef(self):
        return self._synthdef
