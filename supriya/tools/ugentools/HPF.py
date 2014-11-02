# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Filter import Filter


class HPF(Filter):
    r'''Highpass filter unit generator.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> ugentools.HPF.ar(source=source)
        HPF.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'frequency',
        )

    ### PUBLIC METHODS ###

    def __init__(
        self,
        frequency=440,
        rate=None,
        source=None,
        ):
        Filter.__init__(
            self,
            frequency=frequency,
            rate=rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=440,
        source=None,
        ):
        r'''Creates an audio-rate highpass filter.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> ugentools.HPF.ar(
            ...     frequency=440,
            ...     source=source,
            ...     )
            HPF.ar()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.AUDIO
        ugen = cls._new_expanded(
            frequency=frequency,
            rate=rate,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        frequency=440,
        source=None,
        ):
        r'''Creates a control-rate highpass filter.

        ::

            >>> source = ugentools.In.kr(bus=0)
            >>> ugentools.HPF.kr(
            ...     frequency=440,
            ...     source=source,
            ...     )
            HPF.kr()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.CONTROL
        ugen = cls._new_expanded(
            frequency=frequency,
            rate=rate,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def frequency(self):
        r'''Gets `frequency` input of HPF.

        ::

            >>> frequency = None
            >>> hpf = ugentools.HPF.ar(
            ...     frequency=frequency,
            ...     )
            >>> hpf.frequency

        Returns input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of HPF.

        ::

            >>> source = None
            >>> hpf = ugentools.HPF.ar(
            ...     source=source,
            ...     )
            >>> hpf.source

        Returns input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]