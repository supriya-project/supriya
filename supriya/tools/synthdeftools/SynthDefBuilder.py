# -*- encoding: utf-8 -*-
from abjad.tools.topleveltools import new
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class SynthDefBuilder(SupriyaObject):
    r'''A SynthDef builder.

    ::

        >>> from supriya.tools import synthdeftools
        >>> builder = synthdeftools.SynthDefBuilder()
        >>> builder.add_control('frequency', 440)
        >>> builder.add_control('trigger', 0, synthdeftools.Rate.TRIGGER)

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_synthdef_controls',
        '_ugens',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        name=None,
        **kwargs
        ):
        self._synthdef_controls = {}
        for key, value in kwargs.items():
            self.add_control(key, value)
        self._ugens = []

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self._synthdef_controls[item]

    ### PUBLIC METHODS ###

    def add_control(self, *args):
        from supriya.tools import synthdeftools
        if 3 < len(args):
            raise ValueError(args)
        if len(args) == 1:
            assert isinstance(args[0], synthdeftools.SynthDefControl)
            name, value, rate = args[0].name, args[0], args[0].rate
        elif len(args) == 2:
            name, value = args
            if not isinstance(value, synthdeftools.SynthDefControl):
                rate = synthdeftools.Rate.CONTROL
        elif len(args) == 3:
            name, value, rate = args
            rate = synthdeftools.Rate.from_expr(rate)
        if not isinstance(value, synthdeftools.SynthDefControl):
            control = synthdeftools.SynthDefControl(
                name=name,
                rate=rate,
                value=value,
                )
        else:
            control = new(value, name=name, rate=rate)
        self._synthdef_controls[name] = control

    def add_ugen(self, ugen):
        pass

    def build_synthdef(self, name=None):
        pass
