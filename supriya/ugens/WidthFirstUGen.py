import abc
from supriya.ugens.UGen import UGen


class WidthFirstUGen(UGen):
    """
    Abstract base class for UGens with a width-first sort order.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    ### INITIALIZER ###
    @abc.abstractmethod
    def __init__(
        self,
        calculation_rate=None,
        special_index=0,
        **kwargs
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            special_index=special_index,
            **kwargs
            )
