# -*- encoding: utf-8 -*-
import collections
from supriya.tools.ugentools.PureMultiOutUGen import PureMultiOutUGen


class DC(PureMultiOutUGen):
    r'''DC unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> ugentools.DC.ar(source=0)
        OutputProxy(
            source=DC(
                rate=<Rate.AUDIO: 2>,
                channel_count=1,
                source=0.0
                ),
            output_index=0
            )

    ::

        >>> ugentools.DC.ar(source=(1, 2, 3))
        UGenArray(
            (
                OutputProxy(
                    source=DC(
                        rate=<Rate.AUDIO: 2>,
                        channel_count=3,
                        source=1.0
                        ),
                    output_index=0
                    ),
                OutputProxy(
                    source=DC(
                        rate=<Rate.AUDIO: 2>,
                        channel_count=3,
                        source=1.0
                        ),
                    output_index=1
                    ),
                OutputProxy(
                    source=DC(
                        rate=<Rate.AUDIO: 2>,
                        channel_count=3,
                        source=1.0
                        ),
                    output_index=2
                    ),
                )
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'source',
        )

    _unexpanded_input_names = (
        'source',
        'channel_count',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        rate=None,
        channel_count=None,
        source=None,
        ):
        PureMultiOutUGen.__init__(
            self,
            rate=rate,
            channel_count=channel_count,
            source=source,
            )

    ### PRIVATE METHODS ###

    @classmethod
    def _new_expanded(
        cls,
        rate=None,
        source=None,
        ):
        if not isinstance(source, collections.Sequence):
            source = (source,)
        channel_count = len(source)
        return super(DC, cls)._new_expanded(
            rate=rate,
            channel_count=channel_count,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        source=None,
        ):
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.AUDIO
        ugen = cls._new_expanded(
            rate=rate,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        source=None,
        ):
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.CONTROL
        ugen = cls._new_expanded(
            rate=rate,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        return self._inputs[self._ordered_input_names.index('source')]
