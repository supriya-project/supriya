# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.BEQSuite import BEQSuite


class BAllPass(BEQSuite):
    r'''

    ::

        >>> ball_pass = ugentools.BAllPass.(
        ...     frequency=1200,
        ...     reciprocal_of_q=1,
        ...     source=None,
        ...     )
        >>> ball_pass

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'frequency',
        'reciprocal_of_q',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        frequency=1200,
        reciprocal_of_q=1,
        source=None,
        ):
        BEQSuite.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            reciprocal_of_q=reciprocal_of_q,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=1200,
        reciprocal_of_q=1,
        source=None,
        ):
        r'''Constructs an audio-rate BAllPass.

        ::

            >>> ball_pass = ugentools.BAllPass.ar(
            ...     frequency=1200,
            ...     reciprocal_of_q=1,
            ...     source=None,
            ...     )
            >>> ball_pass

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            reciprocal_of_q=reciprocal_of_q,
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
    def frequency(self):
        r'''Gets `frequency` input of BAllPass.

        ::

            >>> ball_pass = ugentools.BAllPass.ar(
            ...     frequency=1200,
            ...     reciprocal_of_q=1,
            ...     source=None,
            ...     )
            >>> ball_pass.frequency

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def reciprocal_of_q(self):
        r'''Gets `reciprocal_of_q` input of BAllPass.

        ::

            >>> ball_pass = ugentools.BAllPass.ar(
            ...     frequency=1200,
            ...     reciprocal_of_q=1,
            ...     source=None,
            ...     )
            >>> ball_pass.reciprocal_of_q

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('reciprocal_of_q')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of BAllPass.

        ::

            >>> ball_pass = ugentools.BAllPass.ar(
            ...     frequency=1200,
            ...     reciprocal_of_q=1,
            ...     source=None,
            ...     )
            >>> ball_pass.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]