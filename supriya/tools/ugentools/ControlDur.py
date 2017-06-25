from supriya.tools.ugentools.InfoUGenBase import InfoUGenBase


class ControlDur(InfoUGenBase):
    """
    A control duration info unit generator.

    ::

        >>> ugentools.ControlDur.ir()
        ControlDur.ir()

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
