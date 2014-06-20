# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class A2K(PureUGen):
    r'''Audio rate to control rate convert unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> source = ugentools.SinOsc.ar()
        >>> ugentools.A2K.kr(
        ...     source=source,
        ...     )
        A2K.kr()

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'source',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        source=None,
        calculation_rate=None,
        ):
        PureUGen.__init__(
            self,
            source=source,
            calculation_rate=calculation_rate,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        source=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen
