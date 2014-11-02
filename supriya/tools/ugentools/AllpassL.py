# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.AllpassN import AllpassN


class AllpassL(AllpassN):
    r'''Linear interpolating allpass delay line unit generator.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> allpass_l = ugentools.AllpassL.ar(source=source)
        >>> allpass_l
        AllpassL.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Delay UGens'

    __slots__ = ()

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        decay_time=1.0,
        delay_time=0.2,
        maximum_delay_time=0.2,
        source=None,
        ):
        r'''Create an audio-rate linear-interpolating allpass delay line.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> allpass_l = ugentools.AllpassL.ar(
            ...     decay_time=1.0,
            ...     delay_time=0.2,
            ...     maximum_delay_time=0.2,
            ...     source=source,
            ...     )
            >>> allpass_l
            AllpassL.ar()

        Returns unit generator graph.
        '''
        return super(AllpassL, cls).ar(
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )

    @classmethod
    def kr(
        cls,
        decay_time=1.0,
        delay_time=0.2,
        maximum_delay_time=0.2,
        source=None,
        ):
        r'''Create a control-rate linear-interpolating allpass delay line.

        ::

            >>> source = ugentools.In.kr(bus=0)
            >>> allpass_l = ugentools.AllpassL.kr(
            ...     decay_time=1.0,
            ...     delay_time=0.2,
            ...     maximum_delay_time=0.2,
            ...     source=source,
            ...     )
            >>> allpass_l
            AllpassL.ar()

        Returns unit generator graph.
        '''
        return super(AllpassL, cls).kr(
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def decay_time(self):
        r'''Gets `decay_time` input of AllpassL.

        ::

            >>> decay_time = 1.0
            >>> source = ugentools.In.ar(bus=0)
            >>> allpass_l = ugentools.AllpassL.ar(
            ...     decay_time=decay_time,
            ...     source=source,
            ...     )
            >>> allpass_l.decay_time
            1.0

        Returns input.
        '''
        index = self._ordered_input_names.index('decay_time')
        return self._inputs[index]

    @property
    def delay_time(self):
        r'''Gets `delay_time` input of AllpassL.

        ::

            >>> delay_time = 1.5
            >>> source = ugentools.In.ar(bus=0)
            >>> allpass_l = ugentools.AllpassL.ar(
            ...     delay_time=delay_time,
            ...     source=source,
            ...     )
            >>> allpass_l.delay_time
            1.5

        Returns input.
        '''
        index = self._ordered_input_names.index('delay_time')
        return self._inputs[index]

    @property
    def maximum_delay_time(self):
        r'''Gets `maximum_delay_time` input of AllpassL.

        ::

            >>> maximum_delay_time = 2.0
            >>> source = ugentools.In.ar(bus=0)
            >>> allpass_l = ugentools.AllpassL.ar(
            ...     maximum_delay_time=maximum_delay_time,
            ...     source=source,
            ...     )
            >>> allpass_l.maximum_delay_time
            2.0

        Returns input.
        '''
        index = self._ordered_input_names.index('maximum_delay_time')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of AllpassL.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> allpass_l = ugentools.AllpassL.ar(
            ...     source=source,
            ...     )
            >>> allpass_l.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    rate=<Rate.AUDIO: 2>,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]