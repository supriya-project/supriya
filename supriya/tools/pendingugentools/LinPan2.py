# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Pan2 import Pan2


class LinPan2(Pan2):
    r'''

    ::

        >>> lin_pan_2 = ugentools.LinPan2.(
        ...     level=1,
        ...     pos=0,
        ...     source=None,
        ...     )
        >>> lin_pan_2

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'pos',
        'level',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        level=1,
        pos=0,
        source=None,
        ):
        Pan2.__init__(
            self,
            calculation_rate=calculation_rate,
            level=level,
            pos=pos,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        level=1,
        pos=0,
        source=None,
        ):
        r'''Constructs an audio-rate LinPan2.

        ::

            >>> lin_pan_2 = ugentools.LinPan2.ar(
            ...     level=1,
            ...     pos=0,
            ...     source=None,
            ...     )
            >>> lin_pan_2

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            level=level,
            pos=pos,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        level=1,
        pos=0,
        source=None,
        ):
        r'''Constructs a control-rate LinPan2.

        ::

            >>> lin_pan_2 = ugentools.LinPan2.kr(
            ...     level=1,
            ...     pos=0,
            ...     source=None,
            ...     )
            >>> lin_pan_2

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            level=level,
            pos=pos,
            source=source,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def level(self):
        r'''Gets `level` input of LinPan2.

        ::

            >>> lin_pan_2 = ugentools.LinPan2.ar(
            ...     level=1,
            ...     pos=0,
            ...     source=None,
            ...     )
            >>> lin_pan_2.level

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('level')
        return self._inputs[index]

    @property
    def pos(self):
        r'''Gets `pos` input of LinPan2.

        ::

            >>> lin_pan_2 = ugentools.LinPan2.ar(
            ...     level=1,
            ...     pos=0,
            ...     source=None,
            ...     )
            >>> lin_pan_2.pos

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('pos')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of LinPan2.

        ::

            >>> lin_pan_2 = ugentools.LinPan2.ar(
            ...     level=1,
            ...     pos=0,
            ...     source=None,
            ...     )
            >>> lin_pan_2.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]