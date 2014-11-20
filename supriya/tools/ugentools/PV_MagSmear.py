# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_MagSmear(PV_ChainUGen):
    r'''

    ::

        >>> pv_mag_smear = ugentools.PV_MagSmear.(
        ...     bins=0,
        ...     buffer_id=None,
        ...     )
        >>> pv_mag_smear

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'bins',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        bins=0,
        buffer_id=None,
        ):
        PV_ChainUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            bins=bins,
            buffer_id=buffer_id,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        bins=0,
        buffer_id=None,
        ):
        r'''Constructs a PV_MagSmear.

        ::

            >>> pv_mag_smear = ugentools.PV_MagSmear.new(
            ...     bins=0,
            ...     buffer_id=None,
            ...     )
            >>> pv_mag_smear

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bins=bins,
            buffer_id=buffer_id,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def bins(self):
        r'''Gets `bins` input of PV_MagSmear.

        ::

            >>> pv_mag_smear = ugentools.PV_MagSmear.ar(
            ...     bins=0,
            ...     buffer_id=None,
            ...     )
            >>> pv_mag_smear.bins

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('bins')
        return self._inputs[index]

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of PV_MagSmear.

        ::

            >>> pv_mag_smear = ugentools.PV_MagSmear.ar(
            ...     bins=0,
            ...     buffer_id=None,
            ...     )
            >>> pv_mag_smear.buffer_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]