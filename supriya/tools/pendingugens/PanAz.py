# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class PanAz(MultiOutUGen):

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        level=1,
        num_chans=None,
        orientation=0.5,
        pos=0,
        source=None,
        width=2,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            level=level,
            num_chans=num_chans,
            orientation=orientation,
            pos=pos,
            source=source,
            width=width,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        level=1,
        num_chans=None,
        orientation=0.5,
        pos=0,
        source=None,
        width=2,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            level=level,
            num_chans=num_chans,
            orientation=orientation,
            pos=pos,
            source=source,
            width=width,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        level=1,
        num_chans=None,
        orientation=0.5,
        pos=0,
        source=None,
        width=2,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            level=level,
            num_chans=num_chans,
            orientation=orientation,
            pos=pos,
            source=source,
            width=width,
            )
        return ugen
