import collections

from supriya import CalculationRate, utils
from supriya.synthdefs import UGen


class Klank(UGen):
    """
    A bank of resonators.

    ::

        >>> frequencies = [200, 671, 1153, 1723]
        >>> amplitudes = None
        >>> decay_times = [1, 1, 1, 1]
        >>> specifications = [frequencies, amplitudes, decay_times]
        >>> source = supriya.ugens.BrownNoise.ar() * 0.001
        >>> klank = supriya.ugens.Klank.ar(
        ...     decay_scale=1,
        ...     frequency_offset=0,
        ...     frequency_scale=1,
        ...     source=source,
        ...     specifications=specifications,
        ...     )
        >>> klank
        Klank.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Filter UGens"

    _ordered_input_names = collections.OrderedDict(
        [
            ("source", None),
            ("frequency_scale", 1),
            ("frequency_offset", 0),
            ("decay_scale", 1),
            ("specifications", None),
        ]
    )

    _unexpanded_input_names = ("specifications",)

    _valid_calculation_rates = (CalculationRate.AUDIO,)

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        decay_scale=1,
        frequency_offset=0,
        frequency_scale=1,
        source=None,
        specifications=None,
    ):
        frequencies, amplitudes, decay_times = specifications
        assert len(frequencies)
        if not amplitudes:
            amplitudes = [1.0] * len(frequencies)
        elif not isinstance(amplitudes, collections.Sequence):
            amplitudes = [amplitudes] * len(frequencies)
        if not decay_times:
            decay_times = [1.0] * len(frequencies)
        elif not isinstance(decay_times, collections.Sequence):
            decay_times = [decay_times] * len(frequencies)
        specifications = utils.zip_sequences(frequencies, amplitudes, decay_times)
        specifications = utils.flatten_iterable(specifications)
        specifications = tuple(specifications)
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            decay_scale=decay_scale,
            frequency_offset=frequency_offset,
            frequency_scale=frequency_scale,
            source=source,
            specifications=specifications,
        )
