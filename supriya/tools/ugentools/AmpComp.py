# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class AmpComp(PureUGen):
    """
    Basic psychoacoustic amplitude compensation.

    ::

        >>> amp_comp = ugentools.AmpComp.ar(
        ...     exp=0.3333,
        ...     frequency=1000,
        ...     root=0,
        ...     )
        >>> amp_comp
        AmpComp.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Line Utility UGens'

    __slots__ = ()

    _ordered_input_names = (
        'frequency',
        'root',
        'exp',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        exp=0.3333,
        frequency=None,
        root=None,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            exp=exp,
            frequency=frequency,
            root=root,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        exp=0.3333,
        frequency=None,
        root=None,
        ):
        """
        Constructs an audio-rate AmpComp.

        ::

            >>> amp_comp = ugentools.AmpComp.ar(
            ...     exp=0.3333,
            ...     frequency=1000,
            ...     root=0,
            ...     )
            >>> amp_comp
            AmpComp.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            exp=exp,
            frequency=frequency,
            root=root,
            )
        return ugen

    @classmethod
    def ir(
        cls,
        exp=0.3333,
        frequency=None,
        root=None,
        ):
        """
        Constructs a scale-rate AmpComp.

        ::

            >>> amp_comp = ugentools.AmpComp.ir(
            ...     exp=0.3333,
            ...     frequency=1000,
            ...     root=0,
            ...     )
            >>> amp_comp
            AmpComp.ir()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.SCALAR
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            exp=exp,
            frequency=frequency,
            root=root,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        exp=0.3333,
        frequency=None,
        root=None,
        ):
        """
        Constructs a control-rate AmpComp.

        ::

            >>> amp_comp = ugentools.AmpComp.kr(
            ...     exp=0.3333,
            ...     frequency=1000,
            ...     root=0,
            ...     )
            >>> amp_comp
            AmpComp.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            exp=exp,
            frequency=frequency,
            root=root,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def exp(self):
        """
        Gets `exp` input of AmpComp.

        ::

            >>> amp_comp = ugentools.AmpComp.ar(
            ...     exp=0.3333,
            ...     frequency=1000,
            ...     root=0,
            ...     )
            >>> amp_comp.exp
            0.3333

        Returns ugen input.
        """
        index = self._ordered_input_names.index('exp')
        return self._inputs[index]

    @property
    def frequency(self):
        """
        Gets `frequency` input of AmpComp.

        ::

            >>> amp_comp = ugentools.AmpComp.ar(
            ...     exp=0.3333,
            ...     frequency=1000,
            ...     root=0,
            ...     )
            >>> amp_comp.frequency
            1000.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def root(self):
        """
        Gets `root` input of AmpComp.

        ::

            >>> amp_comp = ugentools.AmpComp.ar(
            ...     exp=0.3333,
            ...     frequency=1000,
            ...     root=0,
            ...     )
            >>> amp_comp.root
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('root')
        return self._inputs[index]
