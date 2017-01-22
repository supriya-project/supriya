# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.UGen import UGen


class MulAdd(UGen):
    """
    An Optimized multiplication / addition ugen.

    ::

        >>> source = ugentools.SinOsc.ar()
        >>> mul_add = ugentools.MulAdd.new(
        ...     addend=0.5,
        ...     multiplier=-1.5,
        ...     source=source,
        ...     )
        >>> mul_add
        MulAdd.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Basic Operator UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'multiplier',
        'addend',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        addend=0.0,
        multiplier=1.0,
        calculation_rate=None,
        source=None,
        ):
        UGen.__init__(
            self,
            addend=addend,
            multiplier=multiplier,
            calculation_rate=calculation_rate,
            source=source,
            )

    ### PRIVATE METHODS ###

    @staticmethod
    def _inputs_are_valid(
        source,
        multiplier,
        addend,
        ):
        from supriya.tools import synthdeftools
        CalculationRate = synthdeftools.CalculationRate
        if CalculationRate.from_input(source) == CalculationRate.AUDIO:
            return True
        if CalculationRate.from_input(source) == CalculationRate.CONTROL:
            if CalculationRate.from_input(multiplier) in (
                CalculationRate.CONTROL, CalculationRate.SCALAR):
                if CalculationRate.from_input(addend) in (
                    CalculationRate.CONTROL, CalculationRate.SCALAR):
                    return True
        return False

    @classmethod
    def _new_single(
        cls,
        addend=None,
        multiplier=None,
        calculation_rate=None,
        source=None,
        ):
        if multiplier == 0.0:
            return addend
        minus = multiplier == -1
        no_multiplier = multiplier == 1
        no_addend = addend == 0
        if no_multiplier and no_addend:
            return source
        if minus and no_addend:
            return -source
        if no_addend:
            return source * multiplier
        if minus:
            return addend - source
        if no_multiplier:
            return source + addend
        if cls._inputs_are_valid(source, multiplier, addend):
            return cls(
                addend=addend,
                multiplier=multiplier,
                calculation_rate=calculation_rate,
                source=source,
                )
        if cls._inputs_are_valid(multiplier, source, addend):
            return cls(
                addend=addend,
                multiplier=source,
                calculation_rate=calculation_rate,
                source=multiplier,
                )
        return (source * multiplier) + addend

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        source=None,
        multiplier=1.0,
        addend=0.0,
        ):
        """
        Constructs a multiplication / addition ugen.

        ::

            >>> addend = 0.5
            >>> multiplier = 1.5
            >>> source = ugentools.SinOsc.ar(frequency=[440, 442])
            >>> mul_add = ugentools.MulAdd.new(
            ...     addend=addend,
            ...     multiplier=multiplier,
            ...     source=source,
            ...     )
            >>> mul_add
            UGenArray({2})

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        # TODO: handle case of array as source
        calculation_rate = synthdeftools.CalculationRate.from_input((source, multiplier, addend))
        ugen = cls._new_expanded(
            addend=addend,
            multiplier=multiplier,
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def addend(self):
        """
        Gets `addend` input of MulAdd.

        ::

            >>> addend = 0.5
            >>> multiplier = 1.5
            >>> source = ugentools.SinOsc.ar()
            >>> mul_add = ugentools.MulAdd.new(
            ...     addend=addend,
            ...     multiplier=multiplier,
            ...     source=source,
            ...     )
            >>> mul_add.addend
            0.5

        Returns input.
        """
        index = self._ordered_input_names.index('addend')
        return self._inputs[index]

    @property
    def multiplier(self):
        """
        Gets `multiplier` input of MulAdd.

        ::

            >>> addend = 0.5
            >>> multiplier = 1.5
            >>> source = ugentools.SinOsc.ar()
            >>> mul_add = ugentools.MulAdd.new(
            ...     addend=addend,
            ...     multiplier=multiplier,
            ...     source=source,
            ...     )
            >>> mul_add.multiplier
            1.5

        Returns input.
        """
        index = self._ordered_input_names.index('multiplier')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of MulAdd.

        ::

            >>> addend = 0.5
            >>> multiplier = 1.5
            >>> source = ugentools.SinOsc.ar()
            >>> mul_add = ugentools.MulAdd.new(
            ...     addend=addend,
            ...     multiplier=multiplier,
            ...     source=source,
            ...     )
            >>> mul_add.source
            OutputProxy(
                source=SinOsc(
                    calculation_rate=CalculationRate.AUDIO,
                    frequency=440.0,
                    phase=0.0
                    ),
                output_index=0
                )

        Returns input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
