# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.WidthFirstUGen import WidthFirstUGen


class LocalBuf(WidthFirstUGen):
    r'''

    ::

        >>> local_buf = ugentools.LocalBuf.(
        ...     channel_count=1,
        ...     num_frames=1,
        ...     )
        >>> local_buf

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'num_frames',
        'channel_count',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        channel_count=1,
        num_frames=1,
        ):
        WidthFirstUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            num_frames=num_frames,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        channel_count=1,
        num_frames=1,
        ):
        r'''Constructs a LocalBuf.

        ::

            >>> local_buf = ugentools.LocalBuf.new(
            ...     channel_count=1,
            ...     num_frames=1,
            ...     )
            >>> local_buf

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            num_frames=num_frames,
            )
        return ugen

    # def new1(): ...

    # def newFrom(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def channel_count(self):
        r'''Gets `channel_count` input of LocalBuf.

        ::

            >>> local_buf = ugentools.LocalBuf.ar(
            ...     channel_count=1,
            ...     num_frames=1,
            ...     )
            >>> local_buf.channel_count

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('channel_count')
        return self._inputs[index]

    @property
    def num_frames(self):
        r'''Gets `num_frames` input of LocalBuf.

        ::

            >>> local_buf = ugentools.LocalBuf.ar(
            ...     channel_count=1,
            ...     num_frames=1,
            ...     )
            >>> local_buf.num_frames

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('num_frames')
        return self._inputs[index]