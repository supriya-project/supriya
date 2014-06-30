# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class Filter(PureUGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PRIVATE METHODS ###

    def _validate_inputs(self):
        self._check_rate_same_as_first_input_rate()
