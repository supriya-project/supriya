import collections
from supriya import CalculationRate
from supriya.ugens.PureUGen import PureUGen


class VOsc3(PureUGen):
    """
    A wavetable lookup oscillator which can be swept smoothly across wavetables.

    ::

        >>> vosc_3 = supriya.ugens.VOsc3.ar(
        ...     buffer_id=supriya.ugens.MouseX.kr(0,7),
        ...     freq_1=110,
        ...     freq_2=220,
        ...     freq_3=440,
        ...     )
        >>> vosc_3
        VOsc3.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    _ordered_input_names = collections.OrderedDict([
        ('buffer_id', None),
        ('freq_1', 110),
        ('freq_2', 220),
        ('freq_3', 440),
    ])

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
    )
