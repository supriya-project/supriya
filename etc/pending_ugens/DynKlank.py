from supriya.tools.ugentools.UGen import UGen


class DynKlank(UGen):
    """

    ::

        >>> dyn_klank = ugentools.DynKlank.ar(
        ...     decayscale=1,
        ...     freqoffset=0,
        ...     freqscale=1,
        ...     input=input,
        ...     specifications_array_ref=specifications_array_ref,
        ...     )
        >>> dyn_klank
        DynKlank.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'specifications_array_ref',
        'input',
        'freqscale',
        'freqoffset',
        'decayscale',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        decayscale=1,
        freqoffset=0,
        freqscale=1,
        input=None,
        specifications_array_ref=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            decayscale=decayscale,
            freqoffset=freqoffset,
            freqscale=freqscale,
            input=input,
            specifications_array_ref=specifications_array_ref,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        decayscale=1,
        freqoffset=0,
        freqscale=1,
        input=None,
        specifications_array_ref=None,
        ):
        """
        Constructs an audio-rate DynKlank.

        ::

            >>> dyn_klank = ugentools.DynKlank.ar(
            ...     decayscale=1,
            ...     freqoffset=0,
            ...     freqscale=1,
            ...     input=input,
            ...     specifications_array_ref=specifications_array_ref,
            ...     )
            >>> dyn_klank
            DynKlank.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            decayscale=decayscale,
            freqoffset=freqoffset,
            freqscale=freqscale,
            input=input,
            specifications_array_ref=specifications_array_ref,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        decayscale=1,
        freqoffset=0,
        freqscale=1,
        input=None,
        specifications_array_ref=None,
        ):
        """
        Constructs a control-rate DynKlank.

        ::

            >>> dyn_klank = ugentools.DynKlank.kr(
            ...     decayscale=1,
            ...     freqoffset=0,
            ...     freqscale=1,
            ...     input=input,
            ...     specifications_array_ref=specifications_array_ref,
            ...     )
            >>> dyn_klank
            DynKlank.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            decayscale=decayscale,
            freqoffset=freqoffset,
            freqscale=freqscale,
            input=input,
            specifications_array_ref=specifications_array_ref,
            )
        return ugen

    # def new1(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def decayscale(self):
        """
        Gets `decayscale` input of DynKlank.

        ::

            >>> dyn_klank = ugentools.DynKlank.ar(
            ...     decayscale=1,
            ...     freqoffset=0,
            ...     freqscale=1,
            ...     input=input,
            ...     specifications_array_ref=specifications_array_ref,
            ...     )
            >>> dyn_klank.decayscale
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('decayscale')
        return self._inputs[index]

    @property
    def freqoffset(self):
        """
        Gets `freqoffset` input of DynKlank.

        ::

            >>> dyn_klank = ugentools.DynKlank.ar(
            ...     decayscale=1,
            ...     freqoffset=0,
            ...     freqscale=1,
            ...     input=input,
            ...     specifications_array_ref=specifications_array_ref,
            ...     )
            >>> dyn_klank.freqoffset
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('freqoffset')
        return self._inputs[index]

    @property
    def freqscale(self):
        """
        Gets `freqscale` input of DynKlank.

        ::

            >>> dyn_klank = ugentools.DynKlank.ar(
            ...     decayscale=1,
            ...     freqoffset=0,
            ...     freqscale=1,
            ...     input=input,
            ...     specifications_array_ref=specifications_array_ref,
            ...     )
            >>> dyn_klank.freqscale
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('freqscale')
        return self._inputs[index]

    @property
    def input(self):
        """
        Gets `input` input of DynKlank.

        ::

            >>> dyn_klank = ugentools.DynKlank.ar(
            ...     decayscale=1,
            ...     freqoffset=0,
            ...     freqscale=1,
            ...     input=input,
            ...     specifications_array_ref=specifications_array_ref,
            ...     )
            >>> dyn_klank.input

        Returns ugen input.
        """
        index = self._ordered_input_names.index('input')
        return self._inputs[index]

    @property
    def specifications_array_ref(self):
        """
        Gets `specifications_array_ref` input of DynKlank.

        ::

            >>> dyn_klank = ugentools.DynKlank.ar(
            ...     decayscale=1,
            ...     freqoffset=0,
            ...     freqscale=1,
            ...     input=input,
            ...     specifications_array_ref=specifications_array_ref,
            ...     )
            >>> dyn_klank.specifications_array_ref

        Returns ugen input.
        """
        index = self._ordered_input_names.index('specifications_array_ref')
        return self._inputs[index]
