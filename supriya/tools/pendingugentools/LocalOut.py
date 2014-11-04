# -*- encoding: utf-8 -*-
from supriya.tools.pendingugentools.AbstractOut import AbstractOut


class LocalOut(AbstractOut):

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
        channels_array=None,
        ):
        AbstractOut.__init__(
            self,
            calculation_rate=calculation_rate,
            channels_array=channels_array,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        channels_array=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            channels_array=channels_array,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        channels_array=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            channels_array=channels_array,
            )
        return ugen

    # def numFixedArgs(): ...
