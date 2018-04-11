from supriya.ugens.InfoUGenBase import InfoUGenBase


class NumBuffers(InfoUGenBase):
    """
    A number of buffers info unit generator.

    ::

        >>> supriya.ugens.NumBuffers.ir()
        NumBuffers.ir()

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
