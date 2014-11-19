# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class AbstractOut(UGen):
    r'''

    ::

        >>> abstract_out = ugentools.AbstractOut.(
        ...     )
        >>> abstract_out

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = ()

    _valid_calculation_rates = None

    ### INITIALIZER ###

    ### PUBLIC METHODS ###

    # def isOutputUGen(): ...

    # def numFixedArgs(): ...
