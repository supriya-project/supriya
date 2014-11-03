# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class SyncSaw(PureUGen):

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
        saw_frequency=440,
        sync_frequency=440,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            saw_frequency=saw_frequency,
            sync_frequency=sync_frequency,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        saw_frequency=440,
        sync_frequency=440,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            saw_frequency=saw_frequency,
            sync_frequency=sync_frequency,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        saw_frequency=440,
        sync_frequency=440,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            saw_frequency=saw_frequency,
            sync_frequency=sync_frequency,
            )
        return ugen
