# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Rand(UGen):
    r'''A uniform random distribution unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> ugentools.Rand.ir()
        Rand.ir()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Noise UGens'

    __slots__ = ()

    _ordered_input_names = (
        'minimum',
        'maximum',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        rate=None,
        minimum=0.,
        maximum=1.,
        ):
        UGen.__init__(
            self,
            rate=rate,
            minimum=minimum,
            maximum=maximum,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ir(
        cls,
        minimum=0.,
        maximum=1.,
        ):
        r'''Creates a scalar-rate uniform random distribution.

        ::

            >>> from supriya.tools import ugentools
            >>> ugentools.Rand.ir(
            ...     minimum=0.,
            ...     maximum=1.,
            ...     )
            Rand.ir()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.SCALAR
        ugen = cls._new_expanded(
            rate=rate,
            minimum=minimum,
            maximum=maximum,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def maximum(self):
        r'''Gets `maximum` input of Rand.

        ::

            >>> maximum = None
            >>> rand = ugentools.Rand.ar(
            ...     maximum=maximum,
            ...     )
            >>> rand.maximum

        Returns input.
        '''
        index = self._ordered_input_names.index('maximum')
        return self._inputs[index]

    @property
    def minimum(self):
        r'''Gets `minimum` input of Rand.

        ::

            >>> minimum = None
            >>> rand = ugentools.Rand.ar(
            ...     minimum=minimum,
            ...     )
            >>> rand.minimum

        Returns input.
        '''
        index = self._ordered_input_names.index('minimum')
        return self._inputs[index]