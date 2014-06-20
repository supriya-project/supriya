# -*- encoding: utf-8 -*-
import collections
from supriya.tools.synthdeftools.UGen import UGen


class Out(UGen):
    r'''Bus output unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> source = ugentools.SinOsc.ar()
        >>> ugentools.Out.ar(
        ...     bus=0,
        ...     source=source,
        ...     )
        Out.ar()

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    _unexpanded_input_names = ('source',)

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        bus=0,
        source=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            )
        self._configure_argument('bus', bus)
        if not isinstance(source, collections.Sequence):
            source = [source]
        for single_source in source:
            self._configure_argument('source', single_source)

    ### PRIVATE METHODS ###

    def _get_outputs(self):
        return []

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        bus=0,
        source=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        return cls._new(
            bus=bus,
            calculation_rate=calculation_rate,
            source=source,
            )

    @classmethod
    def kr(
        cls,
        bus=0,
        source=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        return cls._new(
            bus=bus,
            calculation_rate=calculation_rate,
            source=source,
            )
