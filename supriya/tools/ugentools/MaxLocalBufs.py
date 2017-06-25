from supriya.tools.synthdeftools.CalculationRate import CalculationRate
from supriya.tools.ugentools.UGen import UGen


class MaxLocalBufs(UGen):
    """
    Sets the maximum number of local buffers in a synth.

    Used internally by LocalBuf.

    ::

        >>> max_local_bufs = ugentools.MaxLocalBufs(1)
        >>> max_local_bufs
        MaxLocalBufs.ir()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Buffer UGens'

    __slots__ = ()

    _ordered_input_names = (
        'maximum',
        )

    _valid_calculation_rates = (
        CalculationRate.SCALAR,
        )

    ### INITIALIZER ###

    def __init__(
        self,
        maximum=0,
        ):
        from supriya.tools import synthdeftools
        maximum = float(maximum)
        calculation_rate = synthdeftools.CalculationRate.SCALAR
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            maximum=maximum,
            )

    ### PUBLIC METHODS ###

    def increment(self):
        """
        Increments maximum local buffer count.

        ::

            >>> max_local_bufs = ugentools.MaxLocalBufs(1)
            >>> max_local_bufs.maximum
            1.0

        ::

            >>> max_local_bufs.increment()
            >>> max_local_bufs.maximum
            2.0

        Returns none.
        """
        self._inputs[0] += 1

    ### PUBLIC PROPERTIES ###

    @property
    def maximum(self):
        """
        Gets `maximum` input of MaxLocalBufs.

        ::

            >>> max_local_bufs = ugentools.MaxLocalBufs(1)
            >>> max_local_bufs.maximum
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('maximum')
        return self._inputs[index]
