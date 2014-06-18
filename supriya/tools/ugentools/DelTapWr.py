# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.Argument import Argument
from supriya.tools.synthdeftools.UGen import UGen


class DelTapWr(UGen):
    r'''Delay tap writer unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> buffer_id = 0
        >>> source = ugentools.SoundIn.ar(0)
        >>> tapin = ugentools.DelTapWr.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ...     )

    ::

        >>> tapin
        DelTapWr.ar()

    ::

        >>> tapout = ugentools.DelTapRd.ar(
        ...     buffer_id=buffer_id,
        ...     phase=tapin,
        ...     delay_time=0.1,
        ...     interpolation=True,
        ...     )

    ::

        >>> tapout
        DelTapRd.ar()

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_argument_names = (
        Argument('buffer_id'),
        Argument('source'),
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        calculation_rate=None,
        source=None,
        ):
        buffer_id = int(buffer_id)
        UGen.__init__(
            self,
            buffer_id=buffer_id,
            calculation_rate=calculation_rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=None,
        source=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        source = cls.as_audio_rate_input(source)
        ugen = cls._new(
            buffer_id=buffer_id,
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        buffer_id=None,
        source=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        source = cls.as_audio_rate_input(source)
        ugen = cls._new(
            buffer_id=buffer_id,
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen
