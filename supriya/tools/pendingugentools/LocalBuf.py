# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.WidthFirstUGen import WidthFirstUGen


class LocalBuf(WidthFirstUGen):
    r'''

    ::

        >>> local_buf = ugentools.LocalBuf.(
        ...     )
        >>> local_buf

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = ()

    _valid_calculation_rates = None

    ### INITIALIZER ###

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
