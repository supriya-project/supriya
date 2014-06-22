# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class In(MultiOutUGen):
    r'''A bus input unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> ugentools.In.ar(bus=0, channel_count=4)
        UGenArray(
            (
                OutputProxy(
                    source=In(
                        bus=0.0,
                        rate=<Rate.AUDIO: 2>,
                        channel_count=4
                        ),
                    output_index=0
                    ),
                OutputProxy(
                    source=In(
                        bus=0.0,
                        rate=<Rate.AUDIO: 2>,
                        channel_count=4
                        ),
                    output_index=1
                    ),
                OutputProxy(
                    source=In(
                        bus=0.0,
                        rate=<Rate.AUDIO: 2>,
                        channel_count=4
                        ),
                    output_index=2
                    ),
                OutputProxy(
                    source=In(
                        bus=0.0,
                        rate=<Rate.AUDIO: 2>,
                        channel_count=4
                        ),
                    output_index=3
                    ),
                )
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'bus',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        bus=0,
        rate=None,
        channel_count=1,
        ):
        MultiOutUGen.__init__(
            self,
            bus=bus,
            rate=rate,
            channel_count=channel_count,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        bus=None,
        channel_count=1,
        ):
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.AUDIO
        ugen = cls._new_expanded(
            rate=rate,
            special_index=0,
            bus=bus,
            channel_count=channel_count,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        bus=None,
        channel_count=1,
        ):
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.CONTROL
        ugen = cls._new_expanded(
            rate=rate,
            special_index=0,
            bus=bus,
            channel_count=channel_count,
            )
        return ugen
