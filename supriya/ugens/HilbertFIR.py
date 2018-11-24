import collections
from supriya.enums import CalculationRate
from supriya.ugens.UGen import UGen


class HilbertFIR(UGen):
    """
    Applies the Hilbert transform.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> hilbert_fir = supriya.ugens.HilbertFIR.ar(
        ...     buffer_id=23,
        ...     source=source,
        ...     )
        >>> hilbert_fir
        HilbertFIR.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [('source', None), ('buffer_id', None)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO,)
