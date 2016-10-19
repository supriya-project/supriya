# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class PureMultiOutUGen(MultiOutUGen):
    r"""
    Abstract base class for multi-output ugens with no side-effects.

    These ugens may be optimized out of ugen graphs during SynthDef
    compilation.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    ### PRIVATE METHODS ###

    def _optimize_graph(self, sort_bundles):
        self._perform_dead_code_elimination(sort_bundles)
