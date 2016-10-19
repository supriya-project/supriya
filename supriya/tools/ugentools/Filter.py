# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class Filter(PureUGen):
    r"""
    Abstract base class for filter ugens.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    __slots__ = ()

    ### PRIVATE METHODS ###

    def _validate_inputs(self):
        self._check_rate_same_as_first_input_rate()
