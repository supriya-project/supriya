# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class DynKlank(UGen):

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
        decayscale=1,
        freqoffset=0,
        freqscale=1,
        input=None,
        specifications_array_ref=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            decayscale=decayscale,
            freqoffset=freqoffset,
            freqscale=freqscale,
            input=input,
            specifications_array_ref=specifications_array_ref,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        decayscale=1,
        freqoffset=0,
        freqscale=1,
        input=None,
        specifications_array_ref=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            decayscale=decayscale,
            freqoffset=freqoffset,
            freqscale=freqscale,
            input=input,
            specifications_array_ref=specifications_array_ref,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        decayscale=1,
        freqoffset=0,
        freqscale=1,
        input=None,
        specifications_array_ref=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            decayscale=decayscale,
            freqoffset=freqoffset,
            freqscale=freqscale,
            input=input,
            specifications_array_ref=specifications_array_ref,
            )
        return ugen

    # def new1(): ...
