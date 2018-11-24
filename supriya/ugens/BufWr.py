import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class BufWr(UGen):
    """
    A buffer-writing oscillator.

    ::

        >>> buffer_id = 23
        >>> phase = supriya.ugens.Phasor.ar(
        ...     rate=supriya.ugens.BufRateScale.kr(buffer_id),
        ...     start=0,
        ...     stop=supriya.ugens.BufFrames.kr(buffer_id),
        ...     )
        >>> source = supriya.ugens.SoundIn.ar(bus=(0, 1))
        >>> buf_wr = supriya.ugens.BufWr.ar(
        ...     buffer_id=buffer_id,
        ...     loop=1,
        ...     phase=phase,
        ...     source=source,
        ...     )
        >>> buf_wr
        BufWr.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Buffer UGens'

    _has_done_flag = True

    _ordered_input_names = collections.OrderedDict(
        [('buffer_id', None), ('phase', 0.0), ('loop', 1.0), ('source', None)]
    )

    _unexpanded_input_names = ('source',)

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)

    ### PUBLIC PROPERTIES ###

    @property
    def has_done_flag(self):
        """
        Is true if UGen has a done flag.

        Returns boolean.
        """
        return True
