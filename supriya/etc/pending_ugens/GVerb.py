from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class GVerb(MultiOutUGen):
    """

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> gverb = ugentools.GVerb.ar(
        ...     damping=0.5,
        ...     drylevel=1,
        ...     earlyreflevel=0.7,
        ...     inputbw=0.5,
        ...     maxroomsize=300,
        ...     revtime=3,
        ...     roomsize=10,
        ...     source=source,
        ...     spread=15,
        ...     taillevel=0.5,
        ...     )
        >>> gverb
        GVerb.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'roomsize',
        'revtime',
        'damping',
        'inputbw',
        'spread',
        'drylevel',
        'earlyreflevel',
        'taillevel',
        'maxroomsize',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        damping=0.5,
        drylevel=1,
        earlyreflevel=0.7,
        inputbw=0.5,
        maxroomsize=300,
        revtime=3,
        roomsize=10,
        source=None,
        spread=15,
        taillevel=0.5,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            damping=damping,
            drylevel=drylevel,
            earlyreflevel=earlyreflevel,
            inputbw=inputbw,
            maxroomsize=maxroomsize,
            revtime=revtime,
            roomsize=roomsize,
            source=source,
            spread=spread,
            taillevel=taillevel,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        damping=0.5,
        drylevel=1,
        earlyreflevel=0.7,
        inputbw=0.5,
        maxroomsize=300,
        revtime=3,
        roomsize=10,
        source=None,
        spread=15,
        taillevel=0.5,
        ):
        """
        Constructs an audio-rate GVerb.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> gverb = ugentools.GVerb.ar(
            ...     damping=0.5,
            ...     drylevel=1,
            ...     earlyreflevel=0.7,
            ...     inputbw=0.5,
            ...     maxroomsize=300,
            ...     revtime=3,
            ...     roomsize=10,
            ...     source=source,
            ...     spread=15,
            ...     taillevel=0.5,
            ...     )
            >>> gverb
            GVerb.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            damping=damping,
            drylevel=drylevel,
            earlyreflevel=earlyreflevel,
            inputbw=inputbw,
            maxroomsize=maxroomsize,
            revtime=revtime,
            roomsize=roomsize,
            source=source,
            spread=spread,
            taillevel=taillevel,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def damping(self):
        """
        Gets `damping` input of GVerb.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> gverb = ugentools.GVerb.ar(
            ...     damping=0.5,
            ...     drylevel=1,
            ...     earlyreflevel=0.7,
            ...     inputbw=0.5,
            ...     maxroomsize=300,
            ...     revtime=3,
            ...     roomsize=10,
            ...     source=source,
            ...     spread=15,
            ...     taillevel=0.5,
            ...     )
            >>> gverb.damping
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('damping')
        return self._inputs[index]

    @property
    def drylevel(self):
        """
        Gets `drylevel` input of GVerb.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> gverb = ugentools.GVerb.ar(
            ...     damping=0.5,
            ...     drylevel=1,
            ...     earlyreflevel=0.7,
            ...     inputbw=0.5,
            ...     maxroomsize=300,
            ...     revtime=3,
            ...     roomsize=10,
            ...     source=source,
            ...     spread=15,
            ...     taillevel=0.5,
            ...     )
            >>> gverb.drylevel
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('drylevel')
        return self._inputs[index]

    @property
    def earlyreflevel(self):
        """
        Gets `earlyreflevel` input of GVerb.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> gverb = ugentools.GVerb.ar(
            ...     damping=0.5,
            ...     drylevel=1,
            ...     earlyreflevel=0.7,
            ...     inputbw=0.5,
            ...     maxroomsize=300,
            ...     revtime=3,
            ...     roomsize=10,
            ...     source=source,
            ...     spread=15,
            ...     taillevel=0.5,
            ...     )
            >>> gverb.earlyreflevel
            0.7

        Returns ugen input.
        """
        index = self._ordered_input_names.index('earlyreflevel')
        return self._inputs[index]

    @property
    def inputbw(self):
        """
        Gets `inputbw` input of GVerb.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> gverb = ugentools.GVerb.ar(
            ...     damping=0.5,
            ...     drylevel=1,
            ...     earlyreflevel=0.7,
            ...     inputbw=0.5,
            ...     maxroomsize=300,
            ...     revtime=3,
            ...     roomsize=10,
            ...     source=source,
            ...     spread=15,
            ...     taillevel=0.5,
            ...     )
            >>> gverb.inputbw
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('inputbw')
        return self._inputs[index]

    @property
    def maxroomsize(self):
        """
        Gets `maxroomsize` input of GVerb.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> gverb = ugentools.GVerb.ar(
            ...     damping=0.5,
            ...     drylevel=1,
            ...     earlyreflevel=0.7,
            ...     inputbw=0.5,
            ...     maxroomsize=300,
            ...     revtime=3,
            ...     roomsize=10,
            ...     source=source,
            ...     spread=15,
            ...     taillevel=0.5,
            ...     )
            >>> gverb.maxroomsize
            300.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('maxroomsize')
        return self._inputs[index]

    @property
    def revtime(self):
        """
        Gets `revtime` input of GVerb.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> gverb = ugentools.GVerb.ar(
            ...     damping=0.5,
            ...     drylevel=1,
            ...     earlyreflevel=0.7,
            ...     inputbw=0.5,
            ...     maxroomsize=300,
            ...     revtime=3,
            ...     roomsize=10,
            ...     source=source,
            ...     spread=15,
            ...     taillevel=0.5,
            ...     )
            >>> gverb.revtime
            3.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('revtime')
        return self._inputs[index]

    @property
    def roomsize(self):
        """
        Gets `roomsize` input of GVerb.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> gverb = ugentools.GVerb.ar(
            ...     damping=0.5,
            ...     drylevel=1,
            ...     earlyreflevel=0.7,
            ...     inputbw=0.5,
            ...     maxroomsize=300,
            ...     revtime=3,
            ...     roomsize=10,
            ...     source=source,
            ...     spread=15,
            ...     taillevel=0.5,
            ...     )
            >>> gverb.roomsize
            10.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('roomsize')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of GVerb.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> gverb = ugentools.GVerb.ar(
            ...     damping=0.5,
            ...     drylevel=1,
            ...     earlyreflevel=0.7,
            ...     inputbw=0.5,
            ...     maxroomsize=300,
            ...     revtime=3,
            ...     roomsize=10,
            ...     source=source,
            ...     spread=15,
            ...     taillevel=0.5,
            ...     )
            >>> gverb.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def spread(self):
        """
        Gets `spread` input of GVerb.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> gverb = ugentools.GVerb.ar(
            ...     damping=0.5,
            ...     drylevel=1,
            ...     earlyreflevel=0.7,
            ...     inputbw=0.5,
            ...     maxroomsize=300,
            ...     revtime=3,
            ...     roomsize=10,
            ...     source=source,
            ...     spread=15,
            ...     taillevel=0.5,
            ...     )
            >>> gverb.spread
            15.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('spread')
        return self._inputs[index]

    @property
    def taillevel(self):
        """
        Gets `taillevel` input of GVerb.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> gverb = ugentools.GVerb.ar(
            ...     damping=0.5,
            ...     drylevel=1,
            ...     earlyreflevel=0.7,
            ...     inputbw=0.5,
            ...     maxroomsize=300,
            ...     revtime=3,
            ...     roomsize=10,
            ...     source=source,
            ...     spread=15,
            ...     taillevel=0.5,
            ...     )
            >>> gverb.taillevel
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('taillevel')
        return self._inputs[index]
