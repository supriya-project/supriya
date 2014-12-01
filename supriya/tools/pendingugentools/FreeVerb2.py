# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class FreeVerb2(MultiOutUGen):
    r'''

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> free_verb_2 = ugentools.FreeVerb2.ar(
        ...     damping=0.5,
        ...     in_2=in_2,
        ...     mix=0.33,
        ...     room=0.5,
        ...     source=source,
        ...     )
        >>> free_verb_2
        FreeVerb2.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'in_2',
        'mix',
        'room',
        'damping',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        damping=0.5,
        in_2=None,
        mix=0.33,
        room=0.5,
        source=None,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            damping=damping,
            in_2=in_2,
            mix=mix,
            room=room,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        damping=0.5,
        in_2=None,
        mix=0.33,
        room=0.5,
        source=None,
        ):
        r'''Constructs an audio-rate FreeVerb2.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> free_verb_2 = ugentools.FreeVerb2.ar(
            ...     damping=0.5,
            ...     in_2=in_2,
            ...     mix=0.33,
            ...     room=0.5,
            ...     source=source,
            ...     )
            >>> free_verb_2
            FreeVerb2.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            damping=damping,
            in_2=in_2,
            mix=mix,
            room=room,
            source=source,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def damping(self):
        r'''Gets `damping` input of FreeVerb2.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> free_verb_2 = ugentools.FreeVerb2.ar(
            ...     damping=0.5,
            ...     in_2=in_2,
            ...     mix=0.33,
            ...     room=0.5,
            ...     source=source,
            ...     )
            >>> free_verb_2.damping
            0.5

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('damping')
        return self._inputs[index]

    @property
    def in_2(self):
        r'''Gets `in_2` input of FreeVerb2.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> free_verb_2 = ugentools.FreeVerb2.ar(
            ...     damping=0.5,
            ...     in_2=in_2,
            ...     mix=0.33,
            ...     room=0.5,
            ...     source=source,
            ...     )
            >>> free_verb_2.in_2

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('in_2')
        return self._inputs[index]

    @property
    def mix(self):
        r'''Gets `mix` input of FreeVerb2.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> free_verb_2 = ugentools.FreeVerb2.ar(
            ...     damping=0.5,
            ...     in_2=in_2,
            ...     mix=0.33,
            ...     room=0.5,
            ...     source=source,
            ...     )
            >>> free_verb_2.mix
            0.33

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('mix')
        return self._inputs[index]

    @property
    def room(self):
        r'''Gets `room` input of FreeVerb2.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> free_verb_2 = ugentools.FreeVerb2.ar(
            ...     damping=0.5,
            ...     in_2=in_2,
            ...     mix=0.33,
            ...     room=0.5,
            ...     source=source,
            ...     )
            >>> free_verb_2.room
            0.5

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('room')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of FreeVerb2.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> free_verb_2 = ugentools.FreeVerb2.ar(
            ...     damping=0.5,
            ...     in_2=in_2,
            ...     mix=0.33,
            ...     room=0.5,
            ...     source=source,
            ...     )
            >>> free_verb_2.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=<CalculationRate.AUDIO: 2>,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]