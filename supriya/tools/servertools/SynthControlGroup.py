# -*- encoding: utf-8 -*-
import collections
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class SynthControlGroup(SupriyaObject, collections.Mapping):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_synth_controls',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        synth_controls=None,
        ):
        from supriya.tools import servertools
        synth_controls = synth_controls or ()
        prototype = servertools.SynthControl
        assert all(isinstance(x, prototype) for x in synth_controls)
        synth_controls = dict(
            (synth_control.name, synth_control)
            for synth_control in synth_controls
            )
        self._synth_controls = synth_controls

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self._synth_controls[item]

    def __len__(self):
        return len(self._synth_controls)

    def __setitem__(self, item, value):
        synth_control = self._synth_controls[item]
        synth_control.value = value

    ### PUBLIC METHODS ###

    @staticmethod
    def from_synthdef(synthdef):
        from supriya.tools import synthdeftools
        assert isinstance(synthdef, synthdeftools.SynthDef)

    ### PUBLIC PROPERTIES ###

    @property
    def synth_controls(self):
        return self._synth_controls.copy()
