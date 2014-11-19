# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.BEQSuite import BEQSuite


class BLowShelf(BEQSuite):
    r'''

    ::

        >>> blow_shelf = ugentools.BLowShelf.(
        ...     db=0,
        ...     frequency=1200,
        ...     rs=1,
        ...     source=None,
        ...     )
        >>> blow_shelf

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'frequency',
        'rs',
        'db',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        db=0,
        frequency=1200,
        rs=1,
        source=None,
        ):
        BEQSuite.__init__(
            self,
            calculation_rate=calculation_rate,
            db=db,
            frequency=frequency,
            rs=rs,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        db=0,
        frequency=1200,
        rs=1,
        source=None,
        ):
        r'''Constructs an audio-rate BLowShelf.

        ::

            >>> blow_shelf = ugentools.BLowShelf.ar(
            ...     db=0,
            ...     frequency=1200,
            ...     rs=1,
            ...     source=None,
            ...     )
            >>> blow_shelf

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            db=db,
            frequency=frequency,
            rs=rs,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    # def magResponse(): ...

    # def magResponse2(): ...

    # def magResponse5(): ...

    # def magResponseN(): ...

    # def sc(): ...

    # def scopeResponse(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def db(self):
        r'''Gets `db` input of BLowShelf.

        ::

            >>> blow_shelf = ugentools.BLowShelf.ar(
            ...     db=0,
            ...     frequency=1200,
            ...     rs=1,
            ...     source=None,
            ...     )
            >>> blow_shelf.db

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('db')
        return self._inputs[index]

    @property
    def frequency(self):
        r'''Gets `frequency` input of BLowShelf.

        ::

            >>> blow_shelf = ugentools.BLowShelf.ar(
            ...     db=0,
            ...     frequency=1200,
            ...     rs=1,
            ...     source=None,
            ...     )
            >>> blow_shelf.frequency

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def rs(self):
        r'''Gets `rs` input of BLowShelf.

        ::

            >>> blow_shelf = ugentools.BLowShelf.ar(
            ...     db=0,
            ...     frequency=1200,
            ...     rs=1,
            ...     source=None,
            ...     )
            >>> blow_shelf.rs

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('rs')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of BLowShelf.

        ::

            >>> blow_shelf = ugentools.BLowShelf.ar(
            ...     db=0,
            ...     frequency=1200,
            ...     rs=1,
            ...     source=None,
            ...     )
            >>> blow_shelf.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]