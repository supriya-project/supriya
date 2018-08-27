from supriya.ugens.PureUGen import PureUGen


class Filter(PureUGen):
    """
    Abstract base class for filter ugens.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    ### PRIVATE METHODS ###

    def _validate_inputs(self):
        self._check_rate_same_as_first_input_rate()
