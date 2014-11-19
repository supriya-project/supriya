# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class AbstractIn(MultiOutUGen):
    r'''

    ::

        >>> abstract_in = ugentools.AbstractIn.(
        ...     )
        >>> abstract_in

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = ()

    _valid_calculation_rates = None

    ### INITIALIZER ###

    ### PUBLIC METHODS ###

    # def isInputUGen(): ...

    # def newFromDesc(): ...
