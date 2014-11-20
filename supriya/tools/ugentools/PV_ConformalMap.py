# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_ConformalMap(PV_ChainUGen):
    r'''

    ::

        >>> pv_conformal_map = ugentools.PV_ConformalMap.(
        ...     aimag=0,
        ...     areal=0,
        ...     buffer_id=None,
        ...     )
        >>> pv_conformal_map

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'areal',
        'aimag',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        aimag=0,
        areal=0,
        buffer_id=None,
        ):
        PV_ChainUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            aimag=aimag,
            areal=areal,
            buffer_id=buffer_id,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        aimag=0,
        areal=0,
        buffer_id=None,
        ):
        r'''Constructs a PV_ConformalMap.

        ::

            >>> pv_conformal_map = ugentools.PV_ConformalMap.new(
            ...     aimag=0,
            ...     areal=0,
            ...     buffer_id=None,
            ...     )
            >>> pv_conformal_map

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            aimag=aimag,
            areal=areal,
            buffer_id=buffer_id,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def aimag(self):
        r'''Gets `aimag` input of PV_ConformalMap.

        ::

            >>> pv_conformal_map = ugentools.PV_ConformalMap.ar(
            ...     aimag=0,
            ...     areal=0,
            ...     buffer_id=None,
            ...     )
            >>> pv_conformal_map.aimag

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('aimag')
        return self._inputs[index]

    @property
    def areal(self):
        r'''Gets `areal` input of PV_ConformalMap.

        ::

            >>> pv_conformal_map = ugentools.PV_ConformalMap.ar(
            ...     aimag=0,
            ...     areal=0,
            ...     buffer_id=None,
            ...     )
            >>> pv_conformal_map.areal

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('areal')
        return self._inputs[index]

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of PV_ConformalMap.

        ::

            >>> pv_conformal_map = ugentools.PV_ConformalMap.ar(
            ...     aimag=0,
            ...     areal=0,
            ...     buffer_id=None,
            ...     )
            >>> pv_conformal_map.buffer_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]