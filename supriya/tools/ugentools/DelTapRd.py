# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class DelTapRd(UGen):
    r'''Delay tap reader unit generator.

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

    _ordered_input_names = (
        'buffer_id',
        'phase',
        'delay_time',
        'interpolation',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        phase=None,
        delay_time=None,
        interpolation=None,
        ):
        buffer_id = int(buffer_id)
        interpolation = int(bool(interpolation))
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            phase=phase,
            delay_time=delay_time,
            interpolation=interpolation,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=None,
        phase=None,
        delay_time=None,
        interpolation=True,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            buffer_id=buffer_id,
            calculation_rate=calculation_rate,
            phase=phase,
            delay_time=delay_time,
            interpolation=interpolation,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        buffer_id=None,
        phase=None,
        delay_time=None,
        interpolation=True,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.SCALAR
        ugen = cls._new_expanded(
            buffer_id=buffer_id,
            calculation_rate=calculation_rate,
            phase=phase,
            delay_time=delay_time,
            interpolation=interpolation,
            )
        return ugen
