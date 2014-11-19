# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_JensenAndersen(PV_ChainUGen):
    r'''

    ::

        >>> pv_jensen_andersen = ugentools.PV_JensenAndersen.(
        ...     buffer_=None,
        ...     prophfc=0.25,
        ...     prophfe=0.25,
        ...     propsc=0.25,
        ...     propsf=0.25,
        ...     threshold=1,
        ...     waittime=0.04,
        ...     )
        >>> pv_jensen_andersen

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_',
        'propsc',
        'prophfe',
        'prophfc',
        'propsf',
        'threshold',
        'waittime',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_=None,
        prophfc=0.25,
        prophfe=0.25,
        propsc=0.25,
        propsf=0.25,
        threshold=1,
        waittime=0.04,
        ):
        PV_ChainUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_=buffer_,
            prophfc=prophfc,
            prophfe=prophfe,
            propsc=propsc,
            propsf=propsf,
            threshold=threshold,
            waittime=waittime,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_=None,
        prophfc=0.25,
        prophfe=0.25,
        propsc=0.25,
        propsf=0.25,
        threshold=1,
        waittime=0.04,
        ):
        r'''Constructs an audio-rate PV_JensenAndersen.

        ::

            >>> pv_jensen_andersen = ugentools.PV_JensenAndersen.ar(
            ...     buffer_=None,
            ...     prophfc=0.25,
            ...     prophfe=0.25,
            ...     propsc=0.25,
            ...     propsf=0.25,
            ...     threshold=1,
            ...     waittime=0.04,
            ...     )
            >>> pv_jensen_andersen

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_=buffer_,
            prophfc=prophfc,
            prophfe=prophfe,
            propsc=propsc,
            propsf=propsf,
            threshold=threshold,
            waittime=waittime,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_(self):
        r'''Gets `buffer_` input of PV_JensenAndersen.

        ::

            >>> pv_jensen_andersen = ugentools.PV_JensenAndersen.ar(
            ...     buffer_=None,
            ...     prophfc=0.25,
            ...     prophfe=0.25,
            ...     propsc=0.25,
            ...     propsf=0.25,
            ...     threshold=1,
            ...     waittime=0.04,
            ...     )
            >>> pv_jensen_andersen.buffer_

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_')
        return self._inputs[index]

    @property
    def propsc(self):
        r'''Gets `propsc` input of PV_JensenAndersen.

        ::

            >>> pv_jensen_andersen = ugentools.PV_JensenAndersen.ar(
            ...     buffer_=None,
            ...     prophfc=0.25,
            ...     prophfe=0.25,
            ...     propsc=0.25,
            ...     propsf=0.25,
            ...     threshold=1,
            ...     waittime=0.04,
            ...     )
            >>> pv_jensen_andersen.propsc

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('propsc')
        return self._inputs[index]

    @property
    def prophfe(self):
        r'''Gets `prophfe` input of PV_JensenAndersen.

        ::

            >>> pv_jensen_andersen = ugentools.PV_JensenAndersen.ar(
            ...     buffer_=None,
            ...     prophfc=0.25,
            ...     prophfe=0.25,
            ...     propsc=0.25,
            ...     propsf=0.25,
            ...     threshold=1,
            ...     waittime=0.04,
            ...     )
            >>> pv_jensen_andersen.prophfe

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('prophfe')
        return self._inputs[index]

    @property
    def prophfc(self):
        r'''Gets `prophfc` input of PV_JensenAndersen.

        ::

            >>> pv_jensen_andersen = ugentools.PV_JensenAndersen.ar(
            ...     buffer_=None,
            ...     prophfc=0.25,
            ...     prophfe=0.25,
            ...     propsc=0.25,
            ...     propsf=0.25,
            ...     threshold=1,
            ...     waittime=0.04,
            ...     )
            >>> pv_jensen_andersen.prophfc

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('prophfc')
        return self._inputs[index]

    @property
    def propsf(self):
        r'''Gets `propsf` input of PV_JensenAndersen.

        ::

            >>> pv_jensen_andersen = ugentools.PV_JensenAndersen.ar(
            ...     buffer_=None,
            ...     prophfc=0.25,
            ...     prophfe=0.25,
            ...     propsc=0.25,
            ...     propsf=0.25,
            ...     threshold=1,
            ...     waittime=0.04,
            ...     )
            >>> pv_jensen_andersen.propsf

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('propsf')
        return self._inputs[index]

    @property
    def threshold(self):
        r'''Gets `threshold` input of PV_JensenAndersen.

        ::

            >>> pv_jensen_andersen = ugentools.PV_JensenAndersen.ar(
            ...     buffer_=None,
            ...     prophfc=0.25,
            ...     prophfe=0.25,
            ...     propsc=0.25,
            ...     propsf=0.25,
            ...     threshold=1,
            ...     waittime=0.04,
            ...     )
            >>> pv_jensen_andersen.threshold

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('threshold')
        return self._inputs[index]

    @property
    def waittime(self):
        r'''Gets `waittime` input of PV_JensenAndersen.

        ::

            >>> pv_jensen_andersen = ugentools.PV_JensenAndersen.ar(
            ...     buffer_=None,
            ...     prophfc=0.25,
            ...     prophfe=0.25,
            ...     propsc=0.25,
            ...     propsf=0.25,
            ...     threshold=1,
            ...     waittime=0.04,
            ...     )
            >>> pv_jensen_andersen.waittime

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('waittime')
        return self._inputs[index]