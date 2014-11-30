# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.BEQSuite import BEQSuite


class BLowShelf(BEQSuite):
    r'''A low-shelf filter.

    ::

        >>> source = ugentools.In.ar(0)
        >>> blow_shelf = ugentools.BLowShelf.ar(
        ...     frequency=1200,
        ...     gain=0,
        ...     reciprocal_of_s=1,
        ...     source=source,
        ...     )
        >>> blow_shelf
        BLowShelf.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'frequency',
        'reciprocal_of_s',
        'gain',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        frequency=1200,
        gain=0,
        reciprocal_of_s=1,
        source=None,
        ):
        BEQSuite.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            gain=gain,
            reciprocal_of_s=reciprocal_of_s,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=1200,
        gain=0,
        reciprocal_of_s=1,
        source=None,
        ):
        r'''Constructs an audio-rate BLowShelf.

        ::

            >>> source = ugentools.In.ar(0)
            >>> blow_shelf = ugentools.BLowShelf.ar(
            ...     frequency=1200,
            ...     gain=0,
            ...     reciprocal_of_s=1,
            ...     source=source,
            ...     )
            >>> blow_shelf
            BLowShelf.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            gain=gain,
            reciprocal_of_s=reciprocal_of_s,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    # def magResponse(): ...

    # def magResponse2(): ...

    # def magResponse5(): ...

    # def magResponseN(): ...

    # def sc(): ...

    # def scopeResponse(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def gain(self):
        r'''Gets `gain` input of BLowShelf.

        ::

            >>> source = ugentools.In.ar(0)
            >>> blow_shelf = ugentools.BLowShelf.ar(
            ...     frequency=1200,
            ...     gain=0,
            ...     reciprocal_of_s=1,
            ...     source=source,
            ...     )
            >>> blow_shelf.gain
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('gain')
        return self._inputs[index]

    @property
    def frequency(self):
        r'''Gets `frequency` input of BLowShelf.

        ::

            >>> source = ugentools.In.ar(0)
            >>> blow_shelf = ugentools.BLowShelf.ar(
            ...     frequency=1200,
            ...     gain=0,
            ...     reciprocal_of_s=1,
            ...     source=source,
            ...     )
            >>> blow_shelf.frequency
            1200.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def reciprocal_of_s(self):
        r'''Gets `reciprocal_of_s` input of BLowShelf.

        ::

            >>> source = ugentools.In.ar(0)
            >>> blow_shelf = ugentools.BLowShelf.ar(
            ...     frequency=1200,
            ...     gain=0,
            ...     reciprocal_of_s=1,
            ...     source=source,
            ...     )
            >>> blow_shelf.reciprocal_of_s
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('reciprocal_of_s')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of BLowShelf.

        ::

            >>> source = ugentools.In.ar(0)
            >>> blow_shelf = ugentools.BLowShelf.ar(
            ...     frequency=1200,
            ...     gain=0,
            ...     reciprocal_of_s=1,
            ...     source=source,
            ...     )
            >>> blow_shelf.source
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