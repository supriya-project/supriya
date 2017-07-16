from supriya.tools.ugentools.InfoUGenBase import InfoUGenBase


class BlockSize(InfoUGenBase):
    """
    A block size info unit generator.

    ::

        >>> ugentools.BlockSize.ir()
        BlockSize.ir()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Info UGens'

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        ):
        InfoUGenBase.__init__(
            self,
            calculation_rate=calculation_rate,
            )
