# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class DelTapWr(UGen):
    r'''Delay tap writer unit generator.

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
        'source',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        rate=None,
        source=None,
        ):
        buffer_id = int(buffer_id)
        UGen.__init__(
            self,
            buffer_id=buffer_id,
            rate=rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=None,
        source=None,
        ):
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.AUDIO
        source = cls.as_audio_rate_input(source)
        ugen = cls._new_expanded(
            buffer_id=buffer_id,
            rate=rate,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        buffer_id=None,
        source=None,
        ):
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.CONTROL
        source = cls.as_audio_rate_input(source)
        ugen = cls._new_expanded(
            buffer_id=buffer_id,
            rate=rate,
            source=source,
            )
        return ugen