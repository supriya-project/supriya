# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.UGen import UGen


class IEnvGen(UGen):
    """

    ::

        >>> ienv_gen = ugentools.IEnvGen.ar(
        ...     envelope=envelope,
        ...     index=index,
        ...     )
        >>> ienv_gen
        IEnvGen.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'envelope',
        'index',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        envelope=None,
        index=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            envelope=envelope,
            index=index,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        envelope=None,
        index=None,
        ):
        """
        Constructs an audio-rate IEnvGen.

        ::

            >>> ienv_gen = ugentools.IEnvGen.ar(
            ...     envelope=envelope,
            ...     index=index,
            ...     )
            >>> ienv_gen
            IEnvGen.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            envelope=envelope,
            index=index,
            )
        return ugen

    # def convertEnv(): ...

    @classmethod
    def kr(
        cls,
        envelope=None,
        index=None,
        ):
        """
        Constructs a control-rate IEnvGen.

        ::

            >>> ienv_gen = ugentools.IEnvGen.kr(
            ...     envelope=envelope,
            ...     index=index,
            ...     )
            >>> ienv_gen
            IEnvGen.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            envelope=envelope,
            index=index,
            )
        return ugen

    # def new1(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def envelope(self):
        """
        Gets `envelope` input of IEnvGen.

        ::

            >>> ienv_gen = ugentools.IEnvGen.ar(
            ...     envelope=envelope,
            ...     index=index,
            ...     )
            >>> ienv_gen.envelope

        Returns ugen input.
        """
        index = self._ordered_input_names.index('envelope')
        return self._inputs[index]

    @property
    def index(self):
        """
        Gets `index` input of IEnvGen.

        ::

            >>> ienv_gen = ugentools.IEnvGen.ar(
            ...     envelope=envelope,
            ...     index=index,
            ...     )
            >>> ienv_gen.index

        Returns ugen input.
        """
        index = self._ordered_input_names.index('index')
        return self._inputs[index]
