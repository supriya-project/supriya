# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class Pan4(MultiOutUGen):
    r'''

    ::

        >>> pan_4 = ugentools.Pan4.(
        ...     level=1,
        ...     source=None,
        ...     xpos=0,
        ...     ypos=0,
        ...     )
        >>> pan_4

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'xpos',
        'ypos',
        'level',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        level=1,
        source=None,
        xpos=0,
        ypos=0,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            level=level,
            source=source,
            xpos=xpos,
            ypos=ypos,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        level=1,
        source=None,
        xpos=0,
        ypos=0,
        ):
        r'''Constructs an audio-rate Pan4.

        ::

            >>> pan_4 = ugentools.Pan4.ar(
            ...     level=1,
            ...     source=None,
            ...     xpos=0,
            ...     ypos=0,
            ...     )
            >>> pan_4

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            level=level,
            source=source,
            xpos=xpos,
            ypos=ypos,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        level=1,
        source=None,
        xpos=0,
        ypos=0,
        ):
        r'''Constructs a control-rate Pan4.

        ::

            >>> pan_4 = ugentools.Pan4.kr(
            ...     level=1,
            ...     source=None,
            ...     xpos=0,
            ...     ypos=0,
            ...     )
            >>> pan_4

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            level=level,
            source=source,
            xpos=xpos,
            ypos=ypos,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def level(self):
        r'''Gets `level` input of Pan4.

        ::

            >>> pan_4 = ugentools.Pan4.ar(
            ...     level=1,
            ...     source=None,
            ...     xpos=0,
            ...     ypos=0,
            ...     )
            >>> pan_4.level

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('level')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of Pan4.

        ::

            >>> pan_4 = ugentools.Pan4.ar(
            ...     level=1,
            ...     source=None,
            ...     xpos=0,
            ...     ypos=0,
            ...     )
            >>> pan_4.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def xpos(self):
        r'''Gets `xpos` input of Pan4.

        ::

            >>> pan_4 = ugentools.Pan4.ar(
            ...     level=1,
            ...     source=None,
            ...     xpos=0,
            ...     ypos=0,
            ...     )
            >>> pan_4.xpos

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('xpos')
        return self._inputs[index]

    @property
    def ypos(self):
        r'''Gets `ypos` input of Pan4.

        ::

            >>> pan_4 = ugentools.Pan4.ar(
            ...     level=1,
            ...     source=None,
            ...     xpos=0,
            ...     ypos=0,
            ...     )
            >>> pan_4.ypos

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('ypos')
        return self._inputs[index]