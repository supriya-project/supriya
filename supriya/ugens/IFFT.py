import collections
from supriya import CalculationRate
from supriya.ugens.WidthFirstUGen import WidthFirstUGen


class IFFT(WidthFirstUGen):
    """
    An inverse fast Fourier transform.

    ::

        >>> pv_chain = supriya.ugens.LocalBuf(2048)
        >>> ifft = supriya.ugens.IFFT.ar(
        ...     pv_chain=pv_chain,
        ...     window_size=0,
        ...     window_type=0,
        ...     )
        >>> ifft
        IFFT.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    _ordered_input_names = collections.OrderedDict([
        ('pv_chain', None),
        ('window_type', 0),
        ('window_size', 0),
    ])

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
    )
