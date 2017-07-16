from supriya.tools.ugentools.BufInfoUGenBase import BufInfoUGenBase


class BufSamples(BufInfoUGenBase):
    """
    A buffer sample count info unit generator.

    ::

        >>> ugentools.BufSamples.kr(buffer_id=0)
        BufSamples.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Buffer UGens'

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        calculation_rate=None,
        ):
        BufInfoUGenBase.__init__(
            self,
            buffer_id=buffer_id,
            calculation_rate=calculation_rate,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        """
        Gets `buffer_id` input of BufSamples.

        ::

            >>> buffer_id = 23
            >>> buf_samples = ugentools.BufSamples.kr(
            ...     buffer_id=buffer_id,
            ...     )
            >>> buf_samples.buffer_id
            23.0

        Returns input.
        """
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]
