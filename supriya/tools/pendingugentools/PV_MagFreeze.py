# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_MagFreeze(PV_ChainUGen):
    r'''

    ::

        >>> pv_mag_freeze = ugentools.PV_MagFreeze.(
        ...     buffer_id=None,
        ...     freeze=0,
        ...     )
        >>> pv_mag_freeze

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'freeze',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        freeze=0,
        ):
        PV_ChainUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            freeze=freeze,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        buffer_id=None,
        freeze=0,
        ):
        r'''Constructs a PV_MagFreeze.

        ::

            >>> pv_mag_freeze = ugentools.PV_MagFreeze.new(
            ...     buffer_id=None,
            ...     freeze=0,
            ...     )
            >>> pv_mag_freeze

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            freeze=freeze,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of PV_MagFreeze.

        ::

            >>> pv_mag_freeze = ugentools.PV_MagFreeze.ar(
            ...     buffer_id=None,
            ...     freeze=0,
            ...     )
            >>> pv_mag_freeze.buffer_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def freeze(self):
        r'''Gets `freeze` input of PV_MagFreeze.

        ::

            >>> pv_mag_freeze = ugentools.PV_MagFreeze.ar(
            ...     buffer_id=None,
            ...     freeze=0,
            ...     )
            >>> pv_mag_freeze.freeze

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('freeze')
        return self._inputs[index]