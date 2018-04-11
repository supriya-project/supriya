from supriya.ugens.InfoUGenBase import InfoUGenBase


class NumAudioBuses(InfoUGenBase):
    """
    A number of audio buses info unit generator.

    ::

        >>> supriya.ugens.NumAudioBuses.ir()
        NumAudioBuses.ir()

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
