from supriya.ugens.MultiOutUGen import MultiOutUGen


class PureMultiOutUGen(MultiOutUGen):
    """
    Abstract base class for multi-output ugens with no side-effects.

    These ugens may be optimized out of ugen graphs during SynthDef
    compilation.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    ### PRIVATE METHODS ###

    def _optimize_graph(self, sort_bundles):
        self._perform_dead_code_elimination(sort_bundles)
