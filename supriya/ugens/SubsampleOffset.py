from supriya.ugens.InfoUGenBase import InfoUGenBase


class SubsampleOffset(InfoUGenBase):
    """
    A subsample-offset info unit generator.

    ::

        >>> supriya.ugens.SubsampleOffset.ir()
        SubsampleOffset.ir()

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
