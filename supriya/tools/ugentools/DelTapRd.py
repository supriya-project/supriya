# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class DelTapRd(UGen):
    r'''Delay tap reader unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> buffer_id = 0
        >>> source = ugentools.SoundIn.ar(0)
        >>> tapin = ugentools.DelTapWr.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ...     )

    ::

        >>> tapin
        DelTapWr.ar()

    ::

        >>> tapout = ugentools.DelTapRd.ar(
        ...     buffer_id=buffer_id,
        ...     phase=tapin,
        ...     delay_time=0.1,
        ...     interpolation=True,
        ...     )

    ::

        >>> tapout
        DelTapRd.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Delay UGens'

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'phase',
        'delay_time',
        'interpolation',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        rate=None,
        buffer_id=None,
        phase=None,
        delay_time=None,
        interpolation=None,
        ):
        buffer_id = int(buffer_id)
        interpolation = int(bool(interpolation))
        UGen.__init__(
            self,
            rate=rate,
            buffer_id=buffer_id,
            phase=phase,
            delay_time=delay_time,
            interpolation=interpolation,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=None,
        phase=None,
        delay_time=None,
        interpolation=True,
        ):
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.AUDIO
        ugen = cls._new_expanded(
            buffer_id=buffer_id,
            rate=rate,
            phase=phase,
            delay_time=delay_time,
            interpolation=interpolation,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        buffer_id=None,
        phase=None,
        delay_time=None,
        interpolation=True,
        ):
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.SCALAR
        ugen = cls._new_expanded(
            buffer_id=buffer_id,
            rate=rate,
            phase=phase,
            delay_time=delay_time,
            interpolation=interpolation,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of DelTapRd.

        ::

            >>> buffer_id = None
            >>> del_tap_rd = ugentools.DelTapRd.ar(
            ...     buffer_id=buffer_id,
            ...     )
            >>> del_tap_rd.buffer_id

        Returns input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def delay_time(self):
        r'''Gets `delay_time` input of DelTapRd.

        ::

            >>> delay_time = None
            >>> del_tap_rd = ugentools.DelTapRd.ar(
            ...     delay_time=delay_time,
            ...     )
            >>> del_tap_rd.delay_time

        Returns input.
        '''
        index = self._ordered_input_names.index('delay_time')
        return self._inputs[index]

    @property
    def interpolation(self):
        r'''Gets `interpolation` input of DelTapRd.

        ::

            >>> interpolation = None
            >>> del_tap_rd = ugentools.DelTapRd.ar(
            ...     interpolation=interpolation,
            ...     )
            >>> del_tap_rd.interpolation

        Returns input.
        '''
        index = self._ordered_input_names.index('interpolation')
        return self._inputs[index]

    @property
    def phase(self):
        r'''Gets `phase` input of DelTapRd.

        ::

            >>> phase = None
            >>> del_tap_rd = ugentools.DelTapRd.ar(
            ...     phase=phase,
            ...     )
            >>> del_tap_rd.phase

        Returns input.
        '''
        index = self._ordered_input_names.index('phase')
        return self._inputs[index]