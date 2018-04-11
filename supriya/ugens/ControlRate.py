from supriya.ugens.InfoUGenBase import InfoUGenBase


class ControlRate(InfoUGenBase):
    """
    A control-rate info unit generator.

    ::

        >>> supriya.ugens.ControlRate.ir()
        ControlRate.ir()

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
