# -*- encoding: utf-8 -*-
from supriya.tools.pendingugentools.AbstractOut import AbstractOut


class XOut(AbstractOut):

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
        bus=None,
        channels_array=None,
        xfade=None,
        ):
        AbstractOut.__init__(
            self,
            calculation_rate=calculation_rate,
            bus=bus,
            channels_array=channels_array,
            xfade=xfade,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        bus=None,
        channels_array=None,
        xfade=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bus=bus,
            channels_array=channels_array,
            xfade=xfade,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        bus=None,
        channels_array=None,
        xfade=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bus=bus,
            channels_array=channels_array,
            xfade=xfade,
            )
        return ugen

    # def numFixedArgs(): ...
