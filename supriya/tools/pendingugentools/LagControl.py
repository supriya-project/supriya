# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Control import Control


class LagControl(Control):
    r'''

    ::

        >>> lag_control = ugentools.LagControl.ar(
        ...     lags=lags,
        ...     values=values,
        ...     )
        >>> lag_control
        LagControl.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'values',
        'lags',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        ):
        Control.__init__(
            self,
            calculation_rate=calculation_rate,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ir(
        cls,
        ):
        r'''Constructs a scale-rate LagControl.

        ::

            >>> lag_control = ugentools.LagControl.ir(
            ...     )
            >>> lag_control
            LagControl.ir()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.SCALAR
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            )
        return ugen

    # def isControlUGen(): ...

    @classmethod
    def kr(
        cls,
        lags=None,
        values=None,
        ):
        r'''Constructs a control-rate LagControl.

        ::

            >>> lag_control = ugentools.LagControl.kr(
            ...     lags=lags,
            ...     values=values,
            ...     )
            >>> lag_control
            LagControl.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            lags=lags,
            values=values,
            )
        return ugen

    # def names(): ...

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def lags(self):
        r'''Gets `lags` input of LagControl.

        ::

            >>> lag_control = ugentools.LagControl.ar(
            ...     lags=lags,
            ...     values=values,
            ...     )
            >>> lag_control.lags

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('lags')
        return self._inputs[index]

    @property
    def values(self):
        r'''Gets `values` input of LagControl.

        ::

            >>> lag_control = ugentools.LagControl.ar(
            ...     lags=lags,
            ...     values=values,
            ...     )
            >>> lag_control.values

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('values')
        return self._inputs[index]