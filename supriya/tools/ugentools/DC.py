# -*- encoding: utf-8 -*-
import collections
from supriya.tools.synthdeftools.Argument import Argument
from supriya.tools.ugentools.PureMultiOutUGen import PureMultiOutUGen


class DC(PureMultiOutUGen):
    r'''DC unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> ugentools.DC.ar(source=0)
        UGenArray(
            (
                OutputProxy(
                    source=DC(
                        calculation_rate=<CalculationRate.AUDIO: 2>,
                        channel_count=1,
                        source=0.0
                        ),
                    output_index=0
                    ),
                )
            )

    ::

        >>> ugentools.DC.ar(source=(1, 2, 3))
        UGenArray(
            (
                OutputProxy(
                    source=DC(
                        calculation_rate=<CalculationRate.AUDIO: 2>,
                        channel_count=3,
                        source=1.0
                        ),
                    output_index=0
                    ),
                OutputProxy(
                    source=DC(
                        calculation_rate=<CalculationRate.AUDIO: 2>,
                        channel_count=3,
                        source=1.0
                        ),
                    output_index=1
                    ),
                OutputProxy(
                    source=DC(
                        calculation_rate=<CalculationRate.AUDIO: 2>,
                        channel_count=3,
                        source=1.0
                        ),
                    output_index=2
                    ),
                )
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_argument_names = (
        Argument('source'),
        )

    _unexpanded_argument_names = (
        'source',
        'channel_count',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        channel_count=None,
        source=None,
        ):
        PureMultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            source=source,
            )

    ### PRIVATE METHODS ###

    @classmethod
    def _new(
        cls,
        calculation_rate=None,
        source=None,
        ):
        if not isinstance(source, collections.Sequence):
            source = (source,)
        channel_count = len(source)
        return super(DC, cls)._new(
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            source=source,
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

    @classmethod
    def kr(
        cls,
        source=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen
