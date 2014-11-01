# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Compander(UGen):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Dynamics UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'control',
        'thresh',
        'slope_below',
        'slope_above',
        'clamp_time',
        'relax_time',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        clamp_time=0.01,
        control=0.,
        rate=None,
        relax_time=0.1,
        slope_above=1.,
        slope_below=1.,
        source=0.,
        thresh=0.5,
        ):
        UGen.__init__(
            self,
            clamp_time=clamp_time,
            control=control,
            rate=rate,
            relax_time=relax_time,
            slope_above=slope_above,
            slope_below=slope_below,
            source=source,
            thresh=thresh,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        clamp_time=0.01,
        control=0.,
        relax_time=0.1,
        slope_above=1.,
        slope_below=1.,
        source=0.,
        thresh=0.5,
        ):
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.AUDIO
        ugen = cls._new_expanded(
            clamp_time=clamp_time,
            control=control,
            rate=rate,
            relax_time=relax_time,
            slope_above=slope_above,
            slope_below=slope_below,
            source=source,
            thresh=thresh,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def clamp_time(self):
        r'''Gets `clamp_time` input of Compander.

        ::

            >>> clamp_time = None
            >>> compander = ugentools.Compander.ar(
            ...     clamp_time=clamp_time,
            ...     )
            >>> compander.clamp_time

        Returns input.
        '''
        index = self._ordered_input_names.index('clamp_time')
        return self._inputs[index]

    @property
    def control(self):
        r'''Gets `control` input of Compander.

        ::

            >>> control = None
            >>> compander = ugentools.Compander.ar(
            ...     control=control,
            ...     )
            >>> compander.control

        Returns input.
        '''
        index = self._ordered_input_names.index('control')
        return self._inputs[index]

    @property
    def relax_time(self):
        r'''Gets `relax_time` input of Compander.

        ::

            >>> relax_time = None
            >>> compander = ugentools.Compander.ar(
            ...     relax_time=relax_time,
            ...     )
            >>> compander.relax_time

        Returns input.
        '''
        index = self._ordered_input_names.index('relax_time')
        return self._inputs[index]

    @property
    def slope_above(self):
        r'''Gets `slope_above` input of Compander.

        ::

            >>> slope_above = None
            >>> compander = ugentools.Compander.ar(
            ...     slope_above=slope_above,
            ...     )
            >>> compander.slope_above

        Returns input.
        '''
        index = self._ordered_input_names.index('slope_above')
        return self._inputs[index]

    @property
    def slope_below(self):
        r'''Gets `slope_below` input of Compander.

        ::

            >>> slope_below = None
            >>> compander = ugentools.Compander.ar(
            ...     slope_below=slope_below,
            ...     )
            >>> compander.slope_below

        Returns input.
        '''
        index = self._ordered_input_names.index('slope_below')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of Compander.

        ::

            >>> source = None
            >>> compander = ugentools.Compander.ar(
            ...     source=source,
            ...     )
            >>> compander.source

        Returns input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def thresh(self):
        r'''Gets `thresh` input of Compander.

        ::

            >>> thresh = None
            >>> compander = ugentools.Compander.ar(
            ...     thresh=thresh,
            ...     )
            >>> compander.thresh

        Returns input.
        '''
        index = self._ordered_input_names.index('thresh')
        return self._inputs[index]