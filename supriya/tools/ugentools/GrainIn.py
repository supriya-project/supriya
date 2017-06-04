# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class GrainIn(MultiOutUGen):
    """

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> grain_in = ugentools.GrainIn.ar(
        ...     channel_count=1,
        ...     duration=1,
        ...     envelope_buffer_id=-1,
        ...     maximum_overlap=512,
        ...     position=0,
        ...     source=source,
        ...     trigger=0,
        ...     )
        >>> grain_in
        GrainIn.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'trigger',
        'duration',
        'source',
        'position',
        'envelope_buffer_id',
        'maximum_overlap',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        channel_count=1,
        duration=1,
        envelope_buffer_id=-1,
        maximum_overlap=512,
        position=0,
        source=None,
        trigger=0,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            duration=duration,
            envelope_buffer_id=envelope_buffer_id,
            maximum_overlap=maximum_overlap,
            position=position,
            source=source,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        channel_count=1,
        duration=1,
        envelope_buffer_id=-1,
        maximum_overlap=512,
        position=0,
        source=None,
        trigger=0,
        ):
        """
        Constructs an audio-rate GrainIn.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> grain_in = ugentools.GrainIn.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envelope_buffer_id=-1,
            ...     maximum_overlap=512,
            ...     position=0,
            ...     source=source,
            ...     trigger=0,
            ...     )
            >>> grain_in
            GrainIn.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            duration=duration,
            envelope_buffer_id=envelope_buffer_id,
            maximum_overlap=maximum_overlap,
            position=position,
            source=source,
            trigger=trigger,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        """
        Gets `duration` input of GrainIn.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> grain_in = ugentools.GrainIn.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envelope_buffer_id=-1,
            ...     maximum_overlap=512,
            ...     position=0,
            ...     source=source,
            ...     trigger=0,
            ...     )
            >>> grain_in.duration
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('duration')
        return self._inputs[index]

    @property
    def envelope_buffer_id(self):
        """
        Gets `envelope_buffer_id` input of GrainIn.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> grain_in = ugentools.GrainIn.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envelope_buffer_id=-1,
            ...     maximum_overlap=512,
            ...     position=0,
            ...     source=source,
            ...     trigger=0,
            ...     )
            >>> grain_in.envelope_buffer_id
            -1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('envelope_buffer_id')
        return self._inputs[index]

    @property
    def maximum_overlap(self):
        """
        Gets `maximum_overlap` input of GrainIn.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> grain_in = ugentools.GrainIn.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envelope_buffer_id=-1,
            ...     maximum_overlap=512,
            ...     position=0,
            ...     source=source,
            ...     trigger=0,
            ...     )
            >>> grain_in.maximum_overlap
            512.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('maximum_overlap')
        return self._inputs[index]

    @property
    def position(self):
        """
        Gets `position` input of GrainIn.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> grain_in = ugentools.GrainIn.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envelope_buffer_id=-1,
            ...     maximum_overlap=512,
            ...     position=0,
            ...     source=source,
            ...     trigger=0,
            ...     )
            >>> grain_in.position
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('position')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of GrainIn.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> grain_in = ugentools.GrainIn.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envelope_buffer_id=-1,
            ...     maximum_overlap=512,
            ...     position=0,
            ...     source=source,
            ...     trigger=0,
            ...     )
            >>> grain_in.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def trigger(self):
        """
        Gets `trigger` input of GrainIn.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> grain_in = ugentools.GrainIn.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envelope_buffer_id=-1,
            ...     maximum_overlap=512,
            ...     position=0,
            ...     source=source,
            ...     trigger=0,
            ...     )
            >>> grain_in.trigger
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]
