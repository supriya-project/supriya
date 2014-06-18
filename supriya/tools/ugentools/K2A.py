# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class K2A(PureUGen):
    r'''Control rate to audio rate convert unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> source = ugentools.SinOsc.kr()
        >>> ugentools.K2A.ar(
        ...     source=source,
        ...     )
        K2A.ar()

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_argument_names = (
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
    def ar(
        cls,
        source=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen
