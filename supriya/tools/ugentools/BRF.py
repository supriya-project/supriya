# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Filter import Filter


class BRF(Filter):
    r'''A 2nd order Butterworth band-reject filter.

    ::

        >>> from supriya.tools import ugentools
        >>> source = ugentools.In.ar(bus=0)
        >>> b_r_f =ugentools.BRF.ar(source=source)
        >>> b_r_f
        BRF.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'frequency',
        'reciprocal_of_q',
        )

    ### PUBLIC METHODS ###

    def __init__(
        self,
        frequency=440,
        rate=None,
        reciprocal_of_q=1.0,
        source=None,
        ):
        Filter.__init__(
            self,
            frequency=frequency,
            rate=rate,
            reciprocal_of_q=reciprocal_of_q,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=440,
        reciprocal_of_q=1.0,
        source=None,
        ):
        r'''Creates an audio-rate band-reject filter.

        ::

            >>> from supriya.tools import ugentools
            >>> source = ugentools.In.ar(bus=0)
            >>> b_r_f = ugentools.BRF.ar(
            ...     frequency=440,
            ...     reciprocal_of_q=1.0,
            ...     source=source,
            ...     )
            >>> b_r_f
            BRF.ar()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.AUDIO
        ugen = cls._new_expanded(
            frequency=frequency,
            rate=rate,
            reciprocal_of_q=reciprocal_of_q,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        frequency=440,
        reciprocal_of_q=1.0,
        source=None,
        ):
        r'''Creates a control-rate band-reject filter.

        ::

            >>> from supriya.tools import ugentools
            >>> source = ugentools.In.kr(bus=0)
            >>> b_r_f = ugentools.BRF.kr(
            ...     frequency=440,
            ...     reciprocal_of_q=1.0,
            ...     source=source,
            ...     )
            >>> b_r_f
            BRF.kr()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.CONTROL
        ugen = cls._new_expanded(
            frequency=frequency,
            rate=rate,
            reciprocal_of_q=reciprocal_of_q,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def frequency(self):
        r'''Gets `frequency` input of BRF.

        ::

            >>> frequency = None
            >>> brf = ugentools.BRF.ar(
            ...     frequency=frequency,
            ...     )
            >>> brf.frequency

        Returns input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def reciprocal_of_q(self):
        r'''Gets `reciprocal_of_q` input of BRF.

        ::

            >>> reciprocal_of_q = None
            >>> brf = ugentools.BRF.ar(
            ...     reciprocal_of_q=reciprocal_of_q,
            ...     )
            >>> brf.reciprocal_of_q

        Returns input.
        '''
        index = self._ordered_input_names.index('reciprocal_of_q')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of BRF.

        ::

            >>> source = None
            >>> brf = ugentools.BRF.ar(
            ...     source=source,
            ...     )
            >>> brf.source

        Returns input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]