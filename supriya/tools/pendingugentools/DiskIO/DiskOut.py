# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class DiskOut(UGen):

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
        bufnum=None,
        channels_array=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            bufnum=bufnum,
            channels_array=channels_array,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        bufnum=None,
        channels_array=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bufnum=bufnum,
            channels_array=channels_array,
            )
        return ugen
