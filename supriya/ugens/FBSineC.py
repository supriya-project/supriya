from supriya.ugens.UGen import UGen


class FBSineC(UGen):
    """
    A cubic-interpolating feedback sine with chaotic phase indexing.

    ::

        >>> fbsine_c = supriya.ugens.FBSineC.ar(
        ...     a=1.1,
        ...     c=0.5,
        ...     fb=0.1,
        ...     frequency=22050,
        ...     im=1,
        ...     xi=0.1,
        ...     yi=0.1,
        ...     )
        >>> fbsine_c
        FBSineC.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Chaos UGens'

    __slots__ = ()

    _ordered_input_names = (
        'frequency',
        'im',
        'fb',
        'a',
        'c',
        'xi',
        'yi',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        a=1.1,
        c=0.5,
        fb=0.1,
        frequency=22050,
        im=1,
        xi=0.1,
        yi=0.1,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            a=a,
            c=c,
            fb=fb,
            frequency=frequency,
            im=im,
            xi=xi,
            yi=yi,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        a=1.1,
        c=0.5,
        fb=0.1,
        frequency=22050,
        im=1,
        xi=0.1,
        yi=0.1,
        ):
        """
        Constructs an audio-rate FBSineC.

        ::

            >>> fbsine_c = supriya.ugens.FBSineC.ar(
            ...     a=1.1,
            ...     c=0.5,
            ...     fb=0.1,
            ...     frequency=22050,
            ...     im=1,
            ...     xi=0.1,
            ...     yi=0.1,
            ...     )
            >>> fbsine_c
            FBSineC.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            a=a,
            c=c,
            fb=fb,
            frequency=frequency,
            im=im,
            xi=xi,
            yi=yi,
            )
        return ugen

    # def equation(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def a(self):
        """
        Gets `a` input of FBSineC.

        ::

            >>> fbsine_c = supriya.ugens.FBSineC.ar(
            ...     a=1.1,
            ...     c=0.5,
            ...     fb=0.1,
            ...     frequency=22050,
            ...     im=1,
            ...     xi=0.1,
            ...     yi=0.1,
            ...     )
            >>> fbsine_c.a
            1.1

        Returns ugen input.
        """
        index = self._ordered_input_names.index('a')
        return self._inputs[index]

    @property
    def c(self):
        """
        Gets `c` input of FBSineC.

        ::

            >>> fbsine_c = supriya.ugens.FBSineC.ar(
            ...     a=1.1,
            ...     c=0.5,
            ...     fb=0.1,
            ...     frequency=22050,
            ...     im=1,
            ...     xi=0.1,
            ...     yi=0.1,
            ...     )
            >>> fbsine_c.c
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('c')
        return self._inputs[index]

    @property
    def fb(self):
        """
        Gets `fb` input of FBSineC.

        ::

            >>> fbsine_c = supriya.ugens.FBSineC.ar(
            ...     a=1.1,
            ...     c=0.5,
            ...     fb=0.1,
            ...     frequency=22050,
            ...     im=1,
            ...     xi=0.1,
            ...     yi=0.1,
            ...     )
            >>> fbsine_c.fb
            0.1

        Returns ugen input.
        """
        index = self._ordered_input_names.index('fb')
        return self._inputs[index]

    @property
    def frequency(self):
        """
        Gets `frequency` input of FBSineC.

        ::

            >>> fbsine_c = supriya.ugens.FBSineC.ar(
            ...     a=1.1,
            ...     c=0.5,
            ...     fb=0.1,
            ...     frequency=22050,
            ...     im=1,
            ...     xi=0.1,
            ...     yi=0.1,
            ...     )
            >>> fbsine_c.frequency
            22050.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def im(self):
        """
        Gets `im` input of FBSineC.

        ::

            >>> fbsine_c = supriya.ugens.FBSineC.ar(
            ...     a=1.1,
            ...     c=0.5,
            ...     fb=0.1,
            ...     frequency=22050,
            ...     im=1,
            ...     xi=0.1,
            ...     yi=0.1,
            ...     )
            >>> fbsine_c.im
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('im')
        return self._inputs[index]

    @property
    def xi(self):
        """
        Gets `xi` input of FBSineC.

        ::

            >>> fbsine_c = supriya.ugens.FBSineC.ar(
            ...     a=1.1,
            ...     c=0.5,
            ...     fb=0.1,
            ...     frequency=22050,
            ...     im=1,
            ...     xi=0.1,
            ...     yi=0.1,
            ...     )
            >>> fbsine_c.xi
            0.1

        Returns ugen input.
        """
        index = self._ordered_input_names.index('xi')
        return self._inputs[index]

    @property
    def yi(self):
        """
        Gets `yi` input of FBSineC.

        ::

            >>> fbsine_c = supriya.ugens.FBSineC.ar(
            ...     a=1.1,
            ...     c=0.5,
            ...     fb=0.1,
            ...     frequency=22050,
            ...     im=1,
            ...     xi=0.1,
            ...     yi=0.1,
            ...     )
            >>> fbsine_c.yi
            0.1

        Returns ugen input.
        """
        index = self._ordered_input_names.index('yi')
        return self._inputs[index]
