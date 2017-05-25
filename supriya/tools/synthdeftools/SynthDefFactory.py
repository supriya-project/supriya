# -*- encoding: utf-8 -*-
import copy
import types
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class SynthDefFactory(SupriyaObject):
    """
    A factory class for building SynthDefs with common signal flow structures.

    ..  container:: example

        ::

            >>> factory = synthdeftools.SynthDefFactory()

        ::

            >>> def signal_block(builder, source, state):
            ...     iterations = state.get('iterations') or 2
            ...     for _ in range(iterations):
            ...         source = ugentools.AllpassC.ar(
            ...             decay_time=ugentools.ExpRand.ir(0.01, 0.1),
            ...             delay_time=ugentools.ExpRand.ir(0.01, 0.1),
            ...             source=source,
            ...             maximum_delay_time=0.1,
            ...             )
            ...     return source

        ::

            >>> factory = factory.with_input()
            >>> factory = factory.with_output()
            >>> factory = factory.with_signal_block(signal_block)
            >>> synthdef = factory.build()
            >>> graph(synthdef)  # doctest: +SKIP

        ..  doctest::

            >>> print(synthdef)
            SynthDef ... {
                0_Control[0:out] -> 1_In[0:bus]
                const_0:0.1 -> 2_ExpRand[0:minimum]
                const_1:0.01 -> 2_ExpRand[1:maximum]
                const_0:0.1 -> 3_ExpRand[0:minimum]
                const_1:0.01 -> 3_ExpRand[1:maximum]
                1_In[0] -> 4_AllpassC[0:source]
                const_0:0.1 -> 4_AllpassC[1:maximum_delay_time]
                3_ExpRand[0] -> 4_AllpassC[2:delay_time]
                2_ExpRand[0] -> 4_AllpassC[3:decay_time]
                const_0:0.1 -> 5_ExpRand[0:minimum]
                const_1:0.01 -> 5_ExpRand[1:maximum]
                const_0:0.1 -> 6_ExpRand[0:minimum]
                const_1:0.01 -> 6_ExpRand[1:maximum]
                4_AllpassC[0] -> 7_AllpassC[0:source]
                const_0:0.1 -> 7_AllpassC[1:maximum_delay_time]
                6_ExpRand[0] -> 7_AllpassC[2:delay_time]
                5_ExpRand[0] -> 7_AllpassC[3:decay_time]
                0_Control[0:out] -> 8_Out[0:bus]
                7_AllpassC[0] -> 8_Out[1:source]
            }

    ..  container:: example

        ::

            >>> synthdef = factory.build(iterations=4)
            >>> graph(synthdef)  # doctest: +SKIP

        ..  doctest::

            >>> print(synthdef)
            SynthDef ... {
                0_Control[0:out] -> 1_In[0:bus]
                const_0:0.1 -> 2_ExpRand[0:minimum]
                const_1:0.01 -> 2_ExpRand[1:maximum]
                const_0:0.1 -> 3_ExpRand[0:minimum]
                const_1:0.01 -> 3_ExpRand[1:maximum]
                1_In[0] -> 4_AllpassC[0:source]
                const_0:0.1 -> 4_AllpassC[1:maximum_delay_time]
                3_ExpRand[0] -> 4_AllpassC[2:delay_time]
                2_ExpRand[0] -> 4_AllpassC[3:decay_time]
                const_0:0.1 -> 5_ExpRand[0:minimum]
                const_1:0.01 -> 5_ExpRand[1:maximum]
                const_0:0.1 -> 6_ExpRand[0:minimum]
                const_1:0.01 -> 6_ExpRand[1:maximum]
                4_AllpassC[0] -> 7_AllpassC[0:source]
                const_0:0.1 -> 7_AllpassC[1:maximum_delay_time]
                6_ExpRand[0] -> 7_AllpassC[2:delay_time]
                5_ExpRand[0] -> 7_AllpassC[3:decay_time]
                const_0:0.1 -> 8_ExpRand[0:minimum]
                const_1:0.01 -> 8_ExpRand[1:maximum]
                const_0:0.1 -> 9_ExpRand[0:minimum]
                const_1:0.01 -> 9_ExpRand[1:maximum]
                7_AllpassC[0] -> 10_AllpassC[0:source]
                const_0:0.1 -> 10_AllpassC[1:maximum_delay_time]
                9_ExpRand[0] -> 10_AllpassC[2:delay_time]
                8_ExpRand[0] -> 10_AllpassC[3:decay_time]
                const_0:0.1 -> 11_ExpRand[0:minimum]
                const_1:0.01 -> 11_ExpRand[1:maximum]
                const_0:0.1 -> 12_ExpRand[0:minimum]
                const_1:0.01 -> 12_ExpRand[1:maximum]
                10_AllpassC[0] -> 13_AllpassC[0:source]
                const_0:0.1 -> 13_AllpassC[1:maximum_delay_time]
                12_ExpRand[0] -> 13_AllpassC[2:delay_time]
                11_ExpRand[0] -> 13_AllpassC[3:decay_time]
                0_Control[0:out] -> 14_Out[0:bus]
                13_AllpassC[0] -> 14_Out[1:source]
            }

    ..  container:: example

        ::

            >>> synthdef = factory.build(channel_count=2)
            >>> graph(synthdef)  # doctest: +SKIP

        ..  doctest::

            >>> print(synthdef)
            SynthDef ... {
                0_Control[0:out] -> 1_In[0:bus]
                const_0:0.1 -> 2_ExpRand[0:minimum]
                const_1:0.01 -> 2_ExpRand[1:maximum]
                const_0:0.1 -> 3_ExpRand[0:minimum]
                const_1:0.01 -> 3_ExpRand[1:maximum]
                1_In[0] -> 4_AllpassC[0:source]
                const_0:0.1 -> 4_AllpassC[1:maximum_delay_time]
                3_ExpRand[0] -> 4_AllpassC[2:delay_time]
                2_ExpRand[0] -> 4_AllpassC[3:decay_time]
                1_In[1] -> 5_AllpassC[0:source]
                const_0:0.1 -> 5_AllpassC[1:maximum_delay_time]
                3_ExpRand[0] -> 5_AllpassC[2:delay_time]
                2_ExpRand[0] -> 5_AllpassC[3:decay_time]
                const_0:0.1 -> 6_ExpRand[0:minimum]
                const_1:0.01 -> 6_ExpRand[1:maximum]
                const_0:0.1 -> 7_ExpRand[0:minimum]
                const_1:0.01 -> 7_ExpRand[1:maximum]
                4_AllpassC[0] -> 8_AllpassC[0:source]
                const_0:0.1 -> 8_AllpassC[1:maximum_delay_time]
                7_ExpRand[0] -> 8_AllpassC[2:delay_time]
                6_ExpRand[0] -> 8_AllpassC[3:decay_time]
                5_AllpassC[0] -> 9_AllpassC[0:source]
                const_0:0.1 -> 9_AllpassC[1:maximum_delay_time]
                7_ExpRand[0] -> 9_AllpassC[2:delay_time]
                6_ExpRand[0] -> 9_AllpassC[3:decay_time]
                0_Control[0:out] -> 10_Out[0:bus]
                8_AllpassC[0] -> 10_Out[1:source]
                9_AllpassC[0] -> 10_Out[2]
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_channel_count',
        '_feedback_loop',
        '_gate',
        '_initial_state',
        '_input',
        '_output',
        '_parameter_blocks',
        '_parameters',
        '_rand_id',
        '_signal_blocks',
        '_silence_detection',
        )

    ### INITIALIZER ###

    def __init__(self, channel_count=1, **kwargs):
        channel_count = int(channel_count)
        assert channel_count > 0
        self._channel_count = channel_count
        self._feedback_loop = None
        self._gate = {}
        self._initial_state = {}
        self._input = {}
        self._output = {}
        self._parameter_blocks = []
        self._parameters = sorted(tuple(kwargs.items()))
        self._rand_id = None
        self._signal_blocks = []
        self._silence_detection = None

    ### PRIVATE METHODS ###

    def _setup_parameters_and_state(self, builder, state, kwargs):
        from supriya.tools import synthdeftools
        from supriya.tools import ugentools
        state['channel_count'] = self._channel_count
        state.update(kwargs)
        for parameter_block in self._parameter_blocks:
            parameter_block(builder, state)
        if self._rand_id:
            builder._add_parameter('rand_id', self._rand_id, 'SCALAR')
            ugentools.RandID.ir(rand_id=builder['rand_id'])
        if self._gate:
            builder._add_parameter('gate', 1, 'TRIGGER')
            state['gate'] = ugentools.Linen.kr(
                attack_time=self._gate['attack_time'],
                done_action=synthdeftools.DoneAction.FREE_SYNTH,
                gate=builder['gate'],
                release_time=self._gate['release_time'],
                )
        if self._output or self._input:
            builder._add_parameter('out', 0, 'SCALAR')
        if (
            self._output.get('windowed') or
            self._input.get('windowed')
            ):
            builder._add_parameter('duration', 1, 'SCALAR')
            state['line'] = ugentools.Line.kr(
                done_action=synthdeftools.DoneAction.FREE_SYNTH,
                duration=builder['duration'],
                )
            state['window'] = state['line'].hanning_window()
        if (
            not self._output.get('windowed') and
            self._output.get('crossfaded')
            ):
            builder._add_parameter('crossfade', 0, 'CONTROL')
        if self._output.get('leveled'):
            builder._add_parameter('level', 1, 'CONTROL')
        for key, value in self._parameters:
            builder._add_parameter(key, value)

    def _build_input(self, builder, state):
        from supriya.tools import ugentools
        if not self._input:
            return
        source = ugentools.In.ar(
            bus=builder['out'],
            channel_count=state['channel_count'],
            )
        if self._input.get('windowed'):
            source *= state['window']
        return source

    def _build_feedback_loop_input(self, builder, source, state):
        from supriya.tools import ugentools
        if self._feedback_loop:
            local_in = ugentools.LocalIn.ar(
                channel_count=state['channel_count'],
                )
            if source is None:
                source = local_in
            else:
                source += local_in
        return source

    def _build_feedback_loop_output(self, builder, source, state):
        from supriya.tools import ugentools
        if not self._feedback_loop:
            return
        if isinstance(self._feedback_loop, types.FunctionType):
            source = self._feedback_loop(builder, source, state)
        ugentools.LocalOut.ar(
            source=source,
            )

    def _build_output(self, builder, source, state):
        from supriya.tools import ugentools
        if not self._output:
            return
        crossfaded = self._output.get('crossfaded')
        replacing = self._output.get('replacing')
        windowed = self._output.get('windowed')
        gate = state.get('gate')
        if self._output.get('leveled') and not crossfaded:
            source *= builder['level']
        out_class = ugentools.Out
        kwargs = dict(
            bus=builder['out'],
            source=source,
            )
        if replacing:
            out_class = ugentools.ReplaceOut
        if crossfaded:
            out_class = ugentools.XOut
            if windowed:
                window = state['window']
                if self._output.get('leveled'):
                    window *= builder['level']
                kwargs['crossfade'] = window
            else:
                kwargs['crossfade'] = builder['crossfade']
            if gate:
                kwargs['crossfade'] *= gate
        elif windowed:
            window = state['window']
            kwargs['source'] *= window
            if gate:
                kwargs['source'] *= gate
        elif gate:
            kwargs['source'] *= gate
        out_class.ar(**kwargs)

    def _build_silence_detection(self, builder, source, state):
        from supriya.tools import synthdeftools
        from supriya.tools import ugentools
        if not self._silence_detection:
            return
        ugentools.DetectSilence.kr(
            done_action=synthdeftools.DoneAction.FREE_SYNTH,
            source=ugentools.Mix.new(source),
            )

    def _clone(self):
        clone = type(self)()
        for name in self.__slots__:
            value = getattr(self, name)
            setattr(clone, name, copy.copy(value))
        return clone

    ### PUBLIC METHODS ###

    def build(self, name=None, **kwargs):
        """
        Build the SynthDef.
        """
        from supriya.tools import synthdeftools
        builder = synthdeftools.SynthDefBuilder()
        state = self._initial_state.copy()
        with builder:
            state.update(**kwargs)
            self._setup_parameters_and_state(builder, state, kwargs)
            source = self._build_input(builder, state)
            source = self._build_feedback_loop_input(builder, source, state)
            for signal_block in self._signal_blocks:
                source = signal_block(builder, source, state)
                assert isinstance(source, synthdeftools.UGenMethodMixin)
            self._build_output(builder, source, state)
            self._build_feedback_loop_output(builder, source, state)
            self._build_silence_detection(builder, source, state)
        return builder.build(name=name)

    def with_channel_count(self, channel_count):
        """
        Return a new factory configured with `channel_count`.

        ..  container:: example

            ::

                >>> factory = synthdeftools.SynthDefFactory()

            ::

                >>> def signal_block(builder, source, state):
                ...     iterations = state.get('iterations') or 2
                ...     for _ in range(iterations):
                ...         source = ugentools.AllpassC.ar(
                ...             decay_time=ugentools.ExpRand.ir(0.01, 0.1),
                ...             delay_time=ugentools.ExpRand.ir(0.01, 0.1),
                ...             source=source,
                ...             maximum_delay_time=0.1,
                ...             )
                ...     return source

            ::

                >>> factory = factory.with_input()
                >>> factory = factory.with_output()
                >>> factory = factory.with_signal_block(signal_block)

        ..  container:: example

            Configure the factory with 4 channels:

            ::

                >>> factory = factory.with_channel_count(4)
                >>> synthdef = factory.build()
                >>> graph(synthdef)  # doctest: +SKIP

            ..  doctest::

                >>> print(synthdef)
                SynthDef ... {
                    0_Control[0:out] -> 1_In[0:bus]
                    const_0:0.1 -> 2_ExpRand[0:minimum]
                    const_1:0.01 -> 2_ExpRand[1:maximum]
                    const_0:0.1 -> 3_ExpRand[0:minimum]
                    const_1:0.01 -> 3_ExpRand[1:maximum]
                    1_In[0] -> 4_AllpassC[0:source]
                    const_0:0.1 -> 4_AllpassC[1:maximum_delay_time]
                    3_ExpRand[0] -> 4_AllpassC[2:delay_time]
                    2_ExpRand[0] -> 4_AllpassC[3:decay_time]
                    1_In[1] -> 5_AllpassC[0:source]
                    const_0:0.1 -> 5_AllpassC[1:maximum_delay_time]
                    3_ExpRand[0] -> 5_AllpassC[2:delay_time]
                    2_ExpRand[0] -> 5_AllpassC[3:decay_time]
                    1_In[2] -> 6_AllpassC[0:source]
                    const_0:0.1 -> 6_AllpassC[1:maximum_delay_time]
                    3_ExpRand[0] -> 6_AllpassC[2:delay_time]
                    2_ExpRand[0] -> 6_AllpassC[3:decay_time]
                    1_In[3] -> 7_AllpassC[0:source]
                    const_0:0.1 -> 7_AllpassC[1:maximum_delay_time]
                    3_ExpRand[0] -> 7_AllpassC[2:delay_time]
                    2_ExpRand[0] -> 7_AllpassC[3:decay_time]
                    const_0:0.1 -> 8_ExpRand[0:minimum]
                    const_1:0.01 -> 8_ExpRand[1:maximum]
                    const_0:0.1 -> 9_ExpRand[0:minimum]
                    const_1:0.01 -> 9_ExpRand[1:maximum]
                    4_AllpassC[0] -> 10_AllpassC[0:source]
                    const_0:0.1 -> 10_AllpassC[1:maximum_delay_time]
                    9_ExpRand[0] -> 10_AllpassC[2:delay_time]
                    8_ExpRand[0] -> 10_AllpassC[3:decay_time]
                    5_AllpassC[0] -> 11_AllpassC[0:source]
                    const_0:0.1 -> 11_AllpassC[1:maximum_delay_time]
                    9_ExpRand[0] -> 11_AllpassC[2:delay_time]
                    8_ExpRand[0] -> 11_AllpassC[3:decay_time]
                    6_AllpassC[0] -> 12_AllpassC[0:source]
                    const_0:0.1 -> 12_AllpassC[1:maximum_delay_time]
                    9_ExpRand[0] -> 12_AllpassC[2:delay_time]
                    8_ExpRand[0] -> 12_AllpassC[3:decay_time]
                    7_AllpassC[0] -> 13_AllpassC[0:source]
                    const_0:0.1 -> 13_AllpassC[1:maximum_delay_time]
                    9_ExpRand[0] -> 13_AllpassC[2:delay_time]
                    8_ExpRand[0] -> 13_AllpassC[3:decay_time]
                    0_Control[0:out] -> 14_Out[0:bus]
                    10_AllpassC[0] -> 14_Out[1:source]
                    11_AllpassC[0] -> 14_Out[2]
                    12_AllpassC[0] -> 14_Out[3]
                    13_AllpassC[0] -> 14_Out[4]
                }

        ..  container:: example

            Channel count can be overridden at build time:

            ::

                >>> synthdef = factory.build(channel_count=3)
                >>> graph(synthdef)  # doctest: +SKIP

            ..  doctest::

                >>> print(synthdef)
                SynthDef ... {
                    0_Control[0:out] -> 1_In[0:bus]
                    const_0:0.1 -> 2_ExpRand[0:minimum]
                    const_1:0.01 -> 2_ExpRand[1:maximum]
                    const_0:0.1 -> 3_ExpRand[0:minimum]
                    const_1:0.01 -> 3_ExpRand[1:maximum]
                    1_In[0] -> 4_AllpassC[0:source]
                    const_0:0.1 -> 4_AllpassC[1:maximum_delay_time]
                    3_ExpRand[0] -> 4_AllpassC[2:delay_time]
                    2_ExpRand[0] -> 4_AllpassC[3:decay_time]
                    1_In[1] -> 5_AllpassC[0:source]
                    const_0:0.1 -> 5_AllpassC[1:maximum_delay_time]
                    3_ExpRand[0] -> 5_AllpassC[2:delay_time]
                    2_ExpRand[0] -> 5_AllpassC[3:decay_time]
                    1_In[2] -> 6_AllpassC[0:source]
                    const_0:0.1 -> 6_AllpassC[1:maximum_delay_time]
                    3_ExpRand[0] -> 6_AllpassC[2:delay_time]
                    2_ExpRand[0] -> 6_AllpassC[3:decay_time]
                    const_0:0.1 -> 7_ExpRand[0:minimum]
                    const_1:0.01 -> 7_ExpRand[1:maximum]
                    const_0:0.1 -> 8_ExpRand[0:minimum]
                    const_1:0.01 -> 8_ExpRand[1:maximum]
                    4_AllpassC[0] -> 9_AllpassC[0:source]
                    const_0:0.1 -> 9_AllpassC[1:maximum_delay_time]
                    8_ExpRand[0] -> 9_AllpassC[2:delay_time]
                    7_ExpRand[0] -> 9_AllpassC[3:decay_time]
                    5_AllpassC[0] -> 10_AllpassC[0:source]
                    const_0:0.1 -> 10_AllpassC[1:maximum_delay_time]
                    8_ExpRand[0] -> 10_AllpassC[2:delay_time]
                    7_ExpRand[0] -> 10_AllpassC[3:decay_time]
                    6_AllpassC[0] -> 11_AllpassC[0:source]
                    const_0:0.1 -> 11_AllpassC[1:maximum_delay_time]
                    8_ExpRand[0] -> 11_AllpassC[2:delay_time]
                    7_ExpRand[0] -> 11_AllpassC[3:decay_time]
                    0_Control[0:out] -> 12_Out[0:bus]
                    9_AllpassC[0] -> 12_Out[1:source]
                    10_AllpassC[0] -> 12_Out[2]
                    11_AllpassC[0] -> 12_Out[3]
                }

        """
        channel_count = int(channel_count)
        assert channel_count > 0
        clone = self._clone()
        clone._channel_count = channel_count
        return clone

    def with_feedback_loop(self, block_function=None):
        """
        Return a new factory configured with a feedback loop.

        Feedback block functions follow the same guidelines as other signal
        block functions.

        ..  container:: example

            ::

                >>> factory = synthdeftools.SynthDefFactory()

            ::

                >>> def signal_block(builder, source, state):
                ...     iterations = state.get('iterations') or 2
                ...     for _ in range(iterations):
                ...         source = ugentools.AllpassC.ar(
                ...             decay_time=ugentools.ExpRand.ir(0.01, 0.1),
                ...             delay_time=ugentools.ExpRand.ir(0.01, 0.1),
                ...             source=source,
                ...             maximum_delay_time=0.1,
                ...             )
                ...     return source

            ::

                >>> factory = factory.with_input()
                >>> factory = factory.with_output()
                >>> factory = factory.with_signal_block(signal_block)

        ..  container:: example

            Configure the factory with a basic feedback loop:

            ::

                >>> factory = factory.with_feedback_loop()
                >>> synthdef = factory.build()
                >>> graph(synthdef)  # doctest: +SKIP

            ..  doctest::

                >>> print(synthdef)
                SynthDef ... {
                    0_Control[0:out] -> 1_In[0:bus]
                    const_0:0.0 -> 2_LocalIn[0:default]
                    1_In[0] -> 3_BinaryOpUGen:ADDITION[0:left]
                    2_LocalIn[0] -> 3_BinaryOpUGen:ADDITION[1:right]
                    const_1:0.1 -> 4_ExpRand[0:minimum]
                    const_2:0.01 -> 4_ExpRand[1:maximum]
                    const_1:0.1 -> 5_ExpRand[0:minimum]
                    const_2:0.01 -> 5_ExpRand[1:maximum]
                    3_BinaryOpUGen:ADDITION[0] -> 6_AllpassC[0:source]
                    const_1:0.1 -> 6_AllpassC[1:maximum_delay_time]
                    5_ExpRand[0] -> 6_AllpassC[2:delay_time]
                    4_ExpRand[0] -> 6_AllpassC[3:decay_time]
                    const_1:0.1 -> 7_ExpRand[0:minimum]
                    const_2:0.01 -> 7_ExpRand[1:maximum]
                    const_1:0.1 -> 8_ExpRand[0:minimum]
                    const_2:0.01 -> 8_ExpRand[1:maximum]
                    6_AllpassC[0] -> 9_AllpassC[0:source]
                    const_1:0.1 -> 9_AllpassC[1:maximum_delay_time]
                    8_ExpRand[0] -> 9_AllpassC[2:delay_time]
                    7_ExpRand[0] -> 9_AllpassC[3:decay_time]
                    0_Control[0:out] -> 10_Out[0:bus]
                    9_AllpassC[0] -> 10_Out[1:source]
                    9_AllpassC[0] -> 11_LocalOut[0:source]
                }

        ..  container:: example

            Configure the factory with a modulated feedback loop via a signal
            block function:

            ::

                >>> def feedback_block(builder, source, state):
                ...     return source * ugentools.SinOsc.kr(frequency=0.3)

            ::

                >>> factory = factory.with_feedback_loop(feedback_block)
                >>> synthdef = factory.build()
                >>> graph(synthdef)  # doctest: +SKIP

            ..  doctest::

                >>> print(synthdef)
                SynthDef ... {
                    0_Control[0:out] -> 1_In[0:bus]
                    const_0:0.0 -> 2_LocalIn[0:default]
                    1_In[0] -> 3_BinaryOpUGen:ADDITION[0:left]
                    2_LocalIn[0] -> 3_BinaryOpUGen:ADDITION[1:right]
                    const_1:0.1 -> 4_ExpRand[0:minimum]
                    const_2:0.01 -> 4_ExpRand[1:maximum]
                    const_1:0.1 -> 5_ExpRand[0:minimum]
                    const_2:0.01 -> 5_ExpRand[1:maximum]
                    3_BinaryOpUGen:ADDITION[0] -> 6_AllpassC[0:source]
                    const_1:0.1 -> 6_AllpassC[1:maximum_delay_time]
                    5_ExpRand[0] -> 6_AllpassC[2:delay_time]
                    4_ExpRand[0] -> 6_AllpassC[3:decay_time]
                    const_1:0.1 -> 7_ExpRand[0:minimum]
                    const_2:0.01 -> 7_ExpRand[1:maximum]
                    const_1:0.1 -> 8_ExpRand[0:minimum]
                    const_2:0.01 -> 8_ExpRand[1:maximum]
                    6_AllpassC[0] -> 9_AllpassC[0:source]
                    const_1:0.1 -> 9_AllpassC[1:maximum_delay_time]
                    8_ExpRand[0] -> 9_AllpassC[2:delay_time]
                    7_ExpRand[0] -> 9_AllpassC[3:decay_time]
                    0_Control[0:out] -> 10_Out[0:bus]
                    9_AllpassC[0] -> 10_Out[1:source]
                    const_3:0.3 -> 11_SinOsc[0:frequency]
                    const_0:0.0 -> 11_SinOsc[1:phase]
                    9_AllpassC[0] -> 12_BinaryOpUGen:MULTIPLICATION[0:left]
                    11_SinOsc[0] -> 12_BinaryOpUGen:MULTIPLICATION[1:right]
                    12_BinaryOpUGen:MULTIPLICATION[0] -> 13_LocalOut[0:source]
                }

        """
        clone = self._clone()
        if block_function:
            clone._feedback_loop = block_function
        else:
            clone._feedback_loop = True
        return clone

    def with_gate(
        self,
        attack_time=0.02,
        release_time=0.02,
        ):
        """
        Return a new factory configured with a gate.

        ..  container:: example

            ::

                >>> factory = synthdeftools.SynthDefFactory()

            ::

                >>> def signal_block(builder, source, state):
                ...     iterations = state.get('iterations') or 2
                ...     for _ in range(iterations):
                ...         source = ugentools.AllpassC.ar(
                ...             decay_time=ugentools.ExpRand.ir(0.01, 0.1),
                ...             delay_time=ugentools.ExpRand.ir(0.01, 0.1),
                ...             source=source,
                ...             maximum_delay_time=0.1,
                ...             )
                ...     return source

            ::

                >>> factory = factory.with_input()
                >>> factory = factory.with_output()
                >>> factory = factory.with_signal_block(signal_block)

        ..  container:: example

            Configure the factory with a gate envelope and corresponding gate
            parameter:

            ::

                >>> factory = factory.with_gate()
                >>> synthdef = factory.build()
                >>> graph(synthdef)  # doctest: +SKIP

            ..  doctest::

                >>> print(synthdef)
                SynthDef ... {
                    0_Control[0:out] -> 1_In[0:bus]
                    2_TrigControl[0:gate] -> 3_Linen[0:gate]
                    const_0:0.02 -> 3_Linen[1:attack_time]
                    const_1:1.0 -> 3_Linen[2:sustain_level]
                    const_0:0.02 -> 3_Linen[3:release_time]
                    const_2:2.0 -> 3_Linen[4:done_action]
                    const_3:0.1 -> 4_ExpRand[0:minimum]
                    const_4:0.01 -> 4_ExpRand[1:maximum]
                    const_3:0.1 -> 5_ExpRand[0:minimum]
                    const_4:0.01 -> 5_ExpRand[1:maximum]
                    1_In[0] -> 6_AllpassC[0:source]
                    const_3:0.1 -> 6_AllpassC[1:maximum_delay_time]
                    5_ExpRand[0] -> 6_AllpassC[2:delay_time]
                    4_ExpRand[0] -> 6_AllpassC[3:decay_time]
                    const_3:0.1 -> 7_ExpRand[0:minimum]
                    const_4:0.01 -> 7_ExpRand[1:maximum]
                    const_3:0.1 -> 8_ExpRand[0:minimum]
                    const_4:0.01 -> 8_ExpRand[1:maximum]
                    6_AllpassC[0] -> 9_AllpassC[0:source]
                    const_3:0.1 -> 9_AllpassC[1:maximum_delay_time]
                    8_ExpRand[0] -> 9_AllpassC[2:delay_time]
                    7_ExpRand[0] -> 9_AllpassC[3:decay_time]
                    9_AllpassC[0] -> 10_BinaryOpUGen:MULTIPLICATION[0:left]
                    3_Linen[0] -> 10_BinaryOpUGen:MULTIPLICATION[1:right]
                    0_Control[0:out] -> 11_Out[0:bus]
                    10_BinaryOpUGen:MULTIPLICATION[0] -> 11_Out[1:source]
                }

        """
        clone = self._clone()
        clone._gate.update(
            attack_time=float(attack_time),
            release_time=float(release_time),
            )
        return clone

    def with_initial_state(self, **state):
        """
        Return a new factory configured with an inital state comprised of
        key/value pairs.

        ..  container:: example

            ::

                >>> factory = synthdeftools.SynthDefFactory()

            ::

                >>> def signal_block(builder, source, state):
                ...     iterations = state.get('iterations') or 2
                ...     for _ in range(iterations):
                ...         source = ugentools.AllpassC.ar(
                ...             decay_time=ugentools.ExpRand.ir(0.01, 0.1),
                ...             delay_time=ugentools.ExpRand.ir(0.01, 0.1),
                ...             source=source,
                ...             maximum_delay_time=0.1,
                ...             )
                ...     return source

            ::

                >>> factory = factory.with_input()
                >>> factory = factory.with_output()
                >>> factory = factory.with_signal_block(signal_block)

        ..  container:: example

            Configure the factory with an initial state consisting of a single
            key/value pair which can be accessed in the previously configured
            signal block function:

            ::

                >>> factory = factory.with_initial_state(iterations=4)
                >>> synthdef = factory.build()
                >>> graph(synthdef)  # doctest: +SKIP

            ..  doctest::

                >>> print(synthdef)
                SynthDef ... {
                    0_Control[0:out] -> 1_In[0:bus]
                    const_0:0.1 -> 2_ExpRand[0:minimum]
                    const_1:0.01 -> 2_ExpRand[1:maximum]
                    const_0:0.1 -> 3_ExpRand[0:minimum]
                    const_1:0.01 -> 3_ExpRand[1:maximum]
                    1_In[0] -> 4_AllpassC[0:source]
                    const_0:0.1 -> 4_AllpassC[1:maximum_delay_time]
                    3_ExpRand[0] -> 4_AllpassC[2:delay_time]
                    2_ExpRand[0] -> 4_AllpassC[3:decay_time]
                    const_0:0.1 -> 5_ExpRand[0:minimum]
                    const_1:0.01 -> 5_ExpRand[1:maximum]
                    const_0:0.1 -> 6_ExpRand[0:minimum]
                    const_1:0.01 -> 6_ExpRand[1:maximum]
                    4_AllpassC[0] -> 7_AllpassC[0:source]
                    const_0:0.1 -> 7_AllpassC[1:maximum_delay_time]
                    6_ExpRand[0] -> 7_AllpassC[2:delay_time]
                    5_ExpRand[0] -> 7_AllpassC[3:decay_time]
                    const_0:0.1 -> 8_ExpRand[0:minimum]
                    const_1:0.01 -> 8_ExpRand[1:maximum]
                    const_0:0.1 -> 9_ExpRand[0:minimum]
                    const_1:0.01 -> 9_ExpRand[1:maximum]
                    7_AllpassC[0] -> 10_AllpassC[0:source]
                    const_0:0.1 -> 10_AllpassC[1:maximum_delay_time]
                    9_ExpRand[0] -> 10_AllpassC[2:delay_time]
                    8_ExpRand[0] -> 10_AllpassC[3:decay_time]
                    const_0:0.1 -> 11_ExpRand[0:minimum]
                    const_1:0.01 -> 11_ExpRand[1:maximum]
                    const_0:0.1 -> 12_ExpRand[0:minimum]
                    const_1:0.01 -> 12_ExpRand[1:maximum]
                    10_AllpassC[0] -> 13_AllpassC[0:source]
                    const_0:0.1 -> 13_AllpassC[1:maximum_delay_time]
                    12_ExpRand[0] -> 13_AllpassC[2:delay_time]
                    11_ExpRand[0] -> 13_AllpassC[3:decay_time]
                    0_Control[0:out] -> 14_Out[0:bus]
                    13_AllpassC[0] -> 14_Out[1:source]
                }

        """
        clone = self._clone()
        clone._initial_state.update(**state)
        return clone

    def with_input(
        self,
        windowed=False,
        ):
        """
        Return a new factory configured with a bus input.

        ..  container:: example

            ::

                >>> factory = synthdeftools.SynthDefFactory()

            ::

                >>> def signal_block(builder, source, state):
                ...     iterations = state.get('iterations') or 2
                ...     for _ in range(iterations):
                ...         source = ugentools.AllpassC.ar(
                ...             decay_time=ugentools.ExpRand.ir(0.01, 0.1),
                ...             delay_time=ugentools.ExpRand.ir(0.01, 0.1),
                ...             source=source,
                ...             maximum_delay_time=0.1,
                ...             )
                ...     return source

            ::

                >>> factory = factory.with_signal_block(signal_block)
                >>> factory = factory.with_output()

        ..  container:: example

            Configure the factory with a basic bus input:

            ::

                >>> factory = factory.with_input()
                >>> synthdef = factory.build()
                >>> graph(synthdef)  # doctest: +SKIP

            ..  doctest::

                >>> print(synthdef)
                SynthDef ... {
                    0_Control[0:out] -> 1_In[0:bus]
                    const_0:0.1 -> 2_ExpRand[0:minimum]
                    const_1:0.01 -> 2_ExpRand[1:maximum]
                    const_0:0.1 -> 3_ExpRand[0:minimum]
                    const_1:0.01 -> 3_ExpRand[1:maximum]
                    1_In[0] -> 4_AllpassC[0:source]
                    const_0:0.1 -> 4_AllpassC[1:maximum_delay_time]
                    3_ExpRand[0] -> 4_AllpassC[2:delay_time]
                    2_ExpRand[0] -> 4_AllpassC[3:decay_time]
                    const_0:0.1 -> 5_ExpRand[0:minimum]
                    const_1:0.01 -> 5_ExpRand[1:maximum]
                    const_0:0.1 -> 6_ExpRand[0:minimum]
                    const_1:0.01 -> 6_ExpRand[1:maximum]
                    4_AllpassC[0] -> 7_AllpassC[0:source]
                    const_0:0.1 -> 7_AllpassC[1:maximum_delay_time]
                    6_ExpRand[0] -> 7_AllpassC[2:delay_time]
                    5_ExpRand[0] -> 7_AllpassC[3:decay_time]
                    0_Control[0:out] -> 8_Out[0:bus]
                    7_AllpassC[0] -> 8_Out[1:source]
                }

        ..  container:: example

            Configure the factory with a windowed bus input:

            ::

                >>> factory = factory.with_input(windowed=True)
                >>> synthdef = factory.build()
                >>> graph(synthdef)  # doctest: +SKIP

            ..  doctest::

                >>> print(synthdef)
                SynthDef ... {
                    const_0:0.0 -> 1_Line[0:start]
                    const_1:1.0 -> 1_Line[1:stop]
                    0_Control[0:duration] -> 1_Line[2:duration]
                    const_2:2.0 -> 1_Line[3:done_action]
                    1_Line[0] -> 2_UnaryOpUGen:HANNING_WINDOW[0:source]
                    0_Control[1:out] -> 3_In[0:bus]
                    3_In[0] -> 4_BinaryOpUGen:MULTIPLICATION[0:left]
                    2_UnaryOpUGen:HANNING_WINDOW[0] -> 4_BinaryOpUGen:MULTIPLICATION[1:right]
                    const_3:0.1 -> 5_ExpRand[0:minimum]
                    const_4:0.01 -> 5_ExpRand[1:maximum]
                    const_3:0.1 -> 6_ExpRand[0:minimum]
                    const_4:0.01 -> 6_ExpRand[1:maximum]
                    4_BinaryOpUGen:MULTIPLICATION[0] -> 7_AllpassC[0:source]
                    const_3:0.1 -> 7_AllpassC[1:maximum_delay_time]
                    6_ExpRand[0] -> 7_AllpassC[2:delay_time]
                    5_ExpRand[0] -> 7_AllpassC[3:decay_time]
                    const_3:0.1 -> 8_ExpRand[0:minimum]
                    const_4:0.01 -> 8_ExpRand[1:maximum]
                    const_3:0.1 -> 9_ExpRand[0:minimum]
                    const_4:0.01 -> 9_ExpRand[1:maximum]
                    7_AllpassC[0] -> 10_AllpassC[0:source]
                    const_3:0.1 -> 10_AllpassC[1:maximum_delay_time]
                    9_ExpRand[0] -> 10_AllpassC[2:delay_time]
                    8_ExpRand[0] -> 10_AllpassC[3:decay_time]
                    0_Control[1:out] -> 11_Out[0:bus]
                    10_AllpassC[0] -> 11_Out[1:source]
                }

        ..  container:: example

            A factory configured with both a windowed bus input and output will
            re-use the windowing signal:

            ::

                >>> factory = factory.with_input(windowed=True)
                >>> factory = factory.with_output(windowed=True)
                >>> synthdef = factory.build()
                >>> graph(synthdef)  # doctest: +SKIP

            ..  doctest::

                >>> print(synthdef)
                SynthDef ... {
                    const_0:0.0 -> 1_Line[0:start]
                    const_1:1.0 -> 1_Line[1:stop]
                    0_Control[0:duration] -> 1_Line[2:duration]
                    const_2:2.0 -> 1_Line[3:done_action]
                    1_Line[0] -> 2_UnaryOpUGen:HANNING_WINDOW[0:source]
                    0_Control[1:out] -> 3_In[0:bus]
                    3_In[0] -> 4_BinaryOpUGen:MULTIPLICATION[0:left]
                    2_UnaryOpUGen:HANNING_WINDOW[0] -> 4_BinaryOpUGen:MULTIPLICATION[1:right]
                    const_3:0.1 -> 5_ExpRand[0:minimum]
                    const_4:0.01 -> 5_ExpRand[1:maximum]
                    const_3:0.1 -> 6_ExpRand[0:minimum]
                    const_4:0.01 -> 6_ExpRand[1:maximum]
                    4_BinaryOpUGen:MULTIPLICATION[0] -> 7_AllpassC[0:source]
                    const_3:0.1 -> 7_AllpassC[1:maximum_delay_time]
                    6_ExpRand[0] -> 7_AllpassC[2:delay_time]
                    5_ExpRand[0] -> 7_AllpassC[3:decay_time]
                    const_3:0.1 -> 8_ExpRand[0:minimum]
                    const_4:0.01 -> 8_ExpRand[1:maximum]
                    const_3:0.1 -> 9_ExpRand[0:minimum]
                    const_4:0.01 -> 9_ExpRand[1:maximum]
                    7_AllpassC[0] -> 10_AllpassC[0:source]
                    const_3:0.1 -> 10_AllpassC[1:maximum_delay_time]
                    9_ExpRand[0] -> 10_AllpassC[2:delay_time]
                    8_ExpRand[0] -> 10_AllpassC[3:decay_time]
                    10_AllpassC[0] -> 11_BinaryOpUGen:MULTIPLICATION[0:left]
                    2_UnaryOpUGen:HANNING_WINDOW[0] -> 11_BinaryOpUGen:MULTIPLICATION[1:right]
                    0_Control[1:out] -> 12_Out[0:bus]
                    11_BinaryOpUGen:MULTIPLICATION[0] -> 12_Out[1:source]
                }

        """
        clone = self._clone()
        clone._input.update(
            windowed=bool(windowed),
            )
        return clone

    def with_output(
        self,
        crossfaded=False,
        leveled=False,
        replacing=False,
        windowed=False,
        ):
        """
        Return a new factory configured with a bus output.

        ..  container:: example

            ::

                >>> factory = synthdeftools.SynthDefFactory()

            ::

                >>> def signal_block(builder, source, state):
                ...     iterations = state.get('iterations') or 2
                ...     for _ in range(iterations):
                ...         source = ugentools.AllpassC.ar(
                ...             decay_time=ugentools.ExpRand.ir(0.01, 0.1),
                ...             delay_time=ugentools.ExpRand.ir(0.01, 0.1),
                ...             source=source,
                ...             maximum_delay_time=0.1,
                ...             )
                ...     return source

            ::

                >>> factory = factory.with_input()
                >>> factory = factory.with_signal_block(signal_block)

        ..  container:: example


            Configure the factory with a basic bus output:

            ::

                >>> factory = factory.with_output()
                >>> synthdef = factory.build()
                >>> graph(synthdef)  # doctest: +SKIP

            ..  doctest::

                >>> print(synthdef)
                SynthDef ... {
                    0_Control[0:out] -> 1_In[0:bus]
                    const_0:0.1 -> 2_ExpRand[0:minimum]
                    const_1:0.01 -> 2_ExpRand[1:maximum]
                    const_0:0.1 -> 3_ExpRand[0:minimum]
                    const_1:0.01 -> 3_ExpRand[1:maximum]
                    1_In[0] -> 4_AllpassC[0:source]
                    const_0:0.1 -> 4_AllpassC[1:maximum_delay_time]
                    3_ExpRand[0] -> 4_AllpassC[2:delay_time]
                    2_ExpRand[0] -> 4_AllpassC[3:decay_time]
                    const_0:0.1 -> 5_ExpRand[0:minimum]
                    const_1:0.01 -> 5_ExpRand[1:maximum]
                    const_0:0.1 -> 6_ExpRand[0:minimum]
                    const_1:0.01 -> 6_ExpRand[1:maximum]
                    4_AllpassC[0] -> 7_AllpassC[0:source]
                    const_0:0.1 -> 7_AllpassC[1:maximum_delay_time]
                    6_ExpRand[0] -> 7_AllpassC[2:delay_time]
                    5_ExpRand[0] -> 7_AllpassC[3:decay_time]
                    0_Control[0:out] -> 8_Out[0:bus]
                    7_AllpassC[0] -> 8_Out[1:source]
                }

        ..  container:: example

            Configure the factory with a windowed bus output:

            ::

                >>> factory = factory.with_output(windowed=True)
                >>> synthdef = factory.build()
                >>> graph(synthdef)  # doctest: +SKIP

            ..  doctest::

                >>> print(synthdef)
                SynthDef ... {
                    const_0:0.0 -> 1_Line[0:start]
                    const_1:1.0 -> 1_Line[1:stop]
                    0_Control[0:duration] -> 1_Line[2:duration]
                    const_2:2.0 -> 1_Line[3:done_action]
                    1_Line[0] -> 2_UnaryOpUGen:HANNING_WINDOW[0:source]
                    0_Control[1:out] -> 3_In[0:bus]
                    const_3:0.1 -> 4_ExpRand[0:minimum]
                    const_4:0.01 -> 4_ExpRand[1:maximum]
                    const_3:0.1 -> 5_ExpRand[0:minimum]
                    const_4:0.01 -> 5_ExpRand[1:maximum]
                    3_In[0] -> 6_AllpassC[0:source]
                    const_3:0.1 -> 6_AllpassC[1:maximum_delay_time]
                    5_ExpRand[0] -> 6_AllpassC[2:delay_time]
                    4_ExpRand[0] -> 6_AllpassC[3:decay_time]
                    const_3:0.1 -> 7_ExpRand[0:minimum]
                    const_4:0.01 -> 7_ExpRand[1:maximum]
                    const_3:0.1 -> 8_ExpRand[0:minimum]
                    const_4:0.01 -> 8_ExpRand[1:maximum]
                    6_AllpassC[0] -> 9_AllpassC[0:source]
                    const_3:0.1 -> 9_AllpassC[1:maximum_delay_time]
                    8_ExpRand[0] -> 9_AllpassC[2:delay_time]
                    7_ExpRand[0] -> 9_AllpassC[3:decay_time]
                    9_AllpassC[0] -> 10_BinaryOpUGen:MULTIPLICATION[0:left]
                    2_UnaryOpUGen:HANNING_WINDOW[0] -> 10_BinaryOpUGen:MULTIPLICATION[1:right]
                    0_Control[1:out] -> 11_Out[0:bus]
                    10_BinaryOpUGen:MULTIPLICATION[0] -> 11_Out[1:source]
                }

        ..  container:: example

            Configure the factory with a crossfade-able bus output:

            ::

                >>> factory = factory.with_output(crossfaded=True)
                >>> synthdef = factory.build()
                >>> graph(synthdef)  # doctest: +SKIP

            ..  doctest::

                >>> print(synthdef)
                SynthDef ... {
                    0_Control[0:out] -> 1_In[0:bus]
                    const_0:0.1 -> 3_ExpRand[0:minimum]
                    const_1:0.01 -> 3_ExpRand[1:maximum]
                    const_0:0.1 -> 4_ExpRand[0:minimum]
                    const_1:0.01 -> 4_ExpRand[1:maximum]
                    1_In[0] -> 5_AllpassC[0:source]
                    const_0:0.1 -> 5_AllpassC[1:maximum_delay_time]
                    4_ExpRand[0] -> 5_AllpassC[2:delay_time]
                    3_ExpRand[0] -> 5_AllpassC[3:decay_time]
                    const_0:0.1 -> 6_ExpRand[0:minimum]
                    const_1:0.01 -> 6_ExpRand[1:maximum]
                    const_0:0.1 -> 7_ExpRand[0:minimum]
                    const_1:0.01 -> 7_ExpRand[1:maximum]
                    5_AllpassC[0] -> 8_AllpassC[0:source]
                    const_0:0.1 -> 8_AllpassC[1:maximum_delay_time]
                    7_ExpRand[0] -> 8_AllpassC[2:delay_time]
                    6_ExpRand[0] -> 8_AllpassC[3:decay_time]
                    0_Control[0:out] -> 9_XOut[0:bus]
                    2_Control[0:crossfade] -> 9_XOut[1:crossfade]
                    8_AllpassC[0] -> 9_XOut[2:source]
                }

        ..  container:: example

            Configure the factory with a basic bus output preceded by an
            amplitude level control:

            ::

                >>> factory = factory.with_output(leveled=True)
                >>> synthdef = factory.build()
                >>> graph(synthdef)  # doctest: +SKIP

            ..  doctest::

                >>> print(synthdef)
                SynthDef ... {
                    0_Control[0:out] -> 1_In[0:bus]
                    const_0:0.1 -> 3_ExpRand[0:minimum]
                    const_1:0.01 -> 3_ExpRand[1:maximum]
                    const_0:0.1 -> 4_ExpRand[0:minimum]
                    const_1:0.01 -> 4_ExpRand[1:maximum]
                    1_In[0] -> 5_AllpassC[0:source]
                    const_0:0.1 -> 5_AllpassC[1:maximum_delay_time]
                    4_ExpRand[0] -> 5_AllpassC[2:delay_time]
                    3_ExpRand[0] -> 5_AllpassC[3:decay_time]
                    const_0:0.1 -> 6_ExpRand[0:minimum]
                    const_1:0.01 -> 6_ExpRand[1:maximum]
                    const_0:0.1 -> 7_ExpRand[0:minimum]
                    const_1:0.01 -> 7_ExpRand[1:maximum]
                    5_AllpassC[0] -> 8_AllpassC[0:source]
                    const_0:0.1 -> 8_AllpassC[1:maximum_delay_time]
                    7_ExpRand[0] -> 8_AllpassC[2:delay_time]
                    6_ExpRand[0] -> 8_AllpassC[3:decay_time]
                    8_AllpassC[0] -> 9_BinaryOpUGen:MULTIPLICATION[0:left]
                    2_Control[0:level] -> 9_BinaryOpUGen:MULTIPLICATION[1:right]
                    0_Control[0:out] -> 10_Out[0:bus]
                    9_BinaryOpUGen:MULTIPLICATION[0] -> 10_Out[1:source]
                }

        ..  container:: example

            A factory configured with a crossfaded *and* windowed bus output
            will use the windowing signal to control the crossfade:

            ::

                >>> factory = factory.with_output(
                ...     crossfaded=True,
                ...     windowed=True,
                ...     )
                >>> synthdef = factory.build()
                >>> graph(synthdef)  # doctest: +SKIP

            ..  doctest::

                >>> print(synthdef)
                SynthDef ... {
                    const_0:0.0 -> 1_Line[0:start]
                    const_1:1.0 -> 1_Line[1:stop]
                    0_Control[0:duration] -> 1_Line[2:duration]
                    const_2:2.0 -> 1_Line[3:done_action]
                    1_Line[0] -> 2_UnaryOpUGen:HANNING_WINDOW[0:source]
                    0_Control[1:out] -> 3_In[0:bus]
                    const_3:0.1 -> 4_ExpRand[0:minimum]
                    const_4:0.01 -> 4_ExpRand[1:maximum]
                    const_3:0.1 -> 5_ExpRand[0:minimum]
                    const_4:0.01 -> 5_ExpRand[1:maximum]
                    3_In[0] -> 6_AllpassC[0:source]
                    const_3:0.1 -> 6_AllpassC[1:maximum_delay_time]
                    5_ExpRand[0] -> 6_AllpassC[2:delay_time]
                    4_ExpRand[0] -> 6_AllpassC[3:decay_time]
                    const_3:0.1 -> 7_ExpRand[0:minimum]
                    const_4:0.01 -> 7_ExpRand[1:maximum]
                    const_3:0.1 -> 8_ExpRand[0:minimum]
                    const_4:0.01 -> 8_ExpRand[1:maximum]
                    6_AllpassC[0] -> 9_AllpassC[0:source]
                    const_3:0.1 -> 9_AllpassC[1:maximum_delay_time]
                    8_ExpRand[0] -> 9_AllpassC[2:delay_time]
                    7_ExpRand[0] -> 9_AllpassC[3:decay_time]
                    0_Control[1:out] -> 10_XOut[0:bus]
                    2_UnaryOpUGen:HANNING_WINDOW[0] -> 10_XOut[1:crossfade]
                    9_AllpassC[0] -> 10_XOut[2:source]
                }

        ..  container:: example

            A level-control can be combined with the windowing and crossfading:

            ::

                >>> factory = factory.with_output(
                ...     crossfaded=True,
                ...     leveled=True,
                ...     windowed=True,
                ...     )
                >>> synthdef = factory.build()
                >>> graph(synthdef)  # doctest: +SKIP

            ..  doctest::

                >>> print(synthdef)
                SynthDef ... {
                    const_0:0.0 -> 1_Line[0:start]
                    const_1:1.0 -> 1_Line[1:stop]
                    0_Control[0:duration] -> 1_Line[2:duration]
                    const_2:2.0 -> 1_Line[3:done_action]
                    1_Line[0] -> 2_UnaryOpUGen:HANNING_WINDOW[0:source]
                    0_Control[1:out] -> 3_In[0:bus]
                    2_UnaryOpUGen:HANNING_WINDOW[0] -> 5_BinaryOpUGen:MULTIPLICATION[0:left]
                    4_Control[0:level] -> 5_BinaryOpUGen:MULTIPLICATION[1:right]
                    const_3:0.1 -> 6_ExpRand[0:minimum]
                    const_4:0.01 -> 6_ExpRand[1:maximum]
                    const_3:0.1 -> 7_ExpRand[0:minimum]
                    const_4:0.01 -> 7_ExpRand[1:maximum]
                    3_In[0] -> 8_AllpassC[0:source]
                    const_3:0.1 -> 8_AllpassC[1:maximum_delay_time]
                    7_ExpRand[0] -> 8_AllpassC[2:delay_time]
                    6_ExpRand[0] -> 8_AllpassC[3:decay_time]
                    const_3:0.1 -> 9_ExpRand[0:minimum]
                    const_4:0.01 -> 9_ExpRand[1:maximum]
                    const_3:0.1 -> 10_ExpRand[0:minimum]
                    const_4:0.01 -> 10_ExpRand[1:maximum]
                    8_AllpassC[0] -> 11_AllpassC[0:source]
                    const_3:0.1 -> 11_AllpassC[1:maximum_delay_time]
                    10_ExpRand[0] -> 11_AllpassC[2:delay_time]
                    9_ExpRand[0] -> 11_AllpassC[3:decay_time]
                    0_Control[1:out] -> 12_XOut[0:bus]
                    5_BinaryOpUGen:MULTIPLICATION[0] -> 12_XOut[1:crossfade]
                    11_AllpassC[0] -> 12_XOut[2:source]
                }

        ..  container:: example

            A factory configured with both a windowed bus input and output will
            re-use the windowing signal:

            ::

                >>> factory = factory.with_input(windowed=True)
                >>> synthdef = factory.build()
                >>> graph(synthdef)  # doctest: +SKIP

            ..  doctest::

                >>> print(synthdef)
                SynthDef ... {
                    const_0:0.0 -> 1_Line[0:start]
                    const_1:1.0 -> 1_Line[1:stop]
                    0_Control[0:duration] -> 1_Line[2:duration]
                    const_2:2.0 -> 1_Line[3:done_action]
                    1_Line[0] -> 2_UnaryOpUGen:HANNING_WINDOW[0:source]
                    0_Control[1:out] -> 3_In[0:bus]
                    3_In[0] -> 4_BinaryOpUGen:MULTIPLICATION[0:left]
                    2_UnaryOpUGen:HANNING_WINDOW[0] -> 4_BinaryOpUGen:MULTIPLICATION[1:right]
                    2_UnaryOpUGen:HANNING_WINDOW[0] -> 6_BinaryOpUGen:MULTIPLICATION[0:left]
                    5_Control[0:level] -> 6_BinaryOpUGen:MULTIPLICATION[1:right]
                    const_3:0.1 -> 7_ExpRand[0:minimum]
                    const_4:0.01 -> 7_ExpRand[1:maximum]
                    const_3:0.1 -> 8_ExpRand[0:minimum]
                    const_4:0.01 -> 8_ExpRand[1:maximum]
                    4_BinaryOpUGen:MULTIPLICATION[0] -> 9_AllpassC[0:source]
                    const_3:0.1 -> 9_AllpassC[1:maximum_delay_time]
                    8_ExpRand[0] -> 9_AllpassC[2:delay_time]
                    7_ExpRand[0] -> 9_AllpassC[3:decay_time]
                    const_3:0.1 -> 10_ExpRand[0:minimum]
                    const_4:0.01 -> 10_ExpRand[1:maximum]
                    const_3:0.1 -> 11_ExpRand[0:minimum]
                    const_4:0.01 -> 11_ExpRand[1:maximum]
                    9_AllpassC[0] -> 12_AllpassC[0:source]
                    const_3:0.1 -> 12_AllpassC[1:maximum_delay_time]
                    11_ExpRand[0] -> 12_AllpassC[2:delay_time]
                    10_ExpRand[0] -> 12_AllpassC[3:decay_time]
                    0_Control[1:out] -> 13_XOut[0:bus]
                    6_BinaryOpUGen:MULTIPLICATION[0] -> 13_XOut[1:crossfade]
                    12_AllpassC[0] -> 13_XOut[2:source]
                }

        """
        assert not (replacing and crossfaded)
        clone = self._clone()
        clone._output.update(
            crossfaded=bool(crossfaded),
            leveled=bool(leveled),
            replacing=bool(replacing),
            windowed=bool(windowed),
            )
        return clone

    def with_parameter_block(self, block_function):
        """
        Return a new factory configured with a parameter block function.

        Use parameter block functions to build repetitive sets of SynthDef
        parameters, e.g. each set of band parameters for a multi-band
        compressor.

        Parameter block functions take two parameters:

        builder
            the SynthDef builder instance

        state
            a dictionary of arbitrary key/value pairs for parameterizing the
            signal and parameter block functions

        The return values of parameter block functions are ignored.

        ..  container:: example

            A factory configured to build multi-band compressor SynthDefs,
            using frequency bands split at ``frequencies``:

            ::

                >>> def parameter_block(builder, state):
                ...     frequencies = state['frequencies']
                ...     band_count = len(frequencies) + 1
                ...     for i in range(band_count):
                ...         band_name = 'band_{}_'.format(i + 1)
                ...         builder._add_parameter(band_name + 'pregain', 0)
                ...         builder._add_parameter(band_name + 'clamp_time', 0.01)
                ...         builder._add_parameter(band_name + 'relax_time', 0.1)
                ...         builder._add_parameter(band_name + 'threshold', -6)
                ...         builder._add_parameter(band_name + 'slope_above', 0.5)
                ...         builder._add_parameter(band_name + 'slope_below', 1.0)
                ...         builder._add_parameter(band_name + 'postgain', 0)

            ::

                >>> def signal_block(builder, source, state):
                ...     bands = []
                ...     frequencies = state['frequencies']
                ...     for frequency in frequencies:
                ...         band = ugentools.LPF.ar(source=source, frequency=frequency)
                ...         bands.append(band)
                ...         source -= band
                ...     bands.append(source)
                ...     compressors = []
                ...     for i, band in enumerate(bands):
                ...         band_name = 'band_{}_'.format(i + 1)
                ...         band *= builder[band_name + 'pregain'].db_to_amplitude()
                ...         band = ugentools.CompanderD.ar(
                ...             source=band,
                ...             clamp_time=builder[band_name + 'clamp_time'],
                ...             relax_time=builder[band_name + 'relax_time'],
                ...             slope_above=builder[band_name + 'slope_above'],
                ...             slope_below=builder[band_name + 'slope_below'],
                ...             threshold=builder[band_name + 'threshold'].db_to_amplitude(),
                ...             )
                ...         band *= builder[band_name + 'postgain'].db_to_amplitude()
                ...         compressors.extend(band)
                ...     source = ugentools.Mix.multichannel(
                ...         compressors,
                ...         state['channel_count'],
                ...         )
                ...     return source

            ::

                >>> factory = synthdeftools.SynthDefFactory()
                >>> factory = factory.with_initial_state(frequencies=(300, 1200, 9600))
                >>> factory = factory.with_parameter_block(parameter_block)
                >>> factory = factory.with_input()
                >>> factory = factory.with_signal_block(signal_block)
                >>> factory = factory.with_output(crossfaded=True)
                >>> synthdef = factory.build()
                >>> graph(synthdef)  # doctest: +SKIP

            ..  doctest::

                >>> print(synthdef)
                SynthDef ... {
                    0_Control[0:out] -> 1_In[0:bus]
                    1_In[0] -> 2_LPF[0:source]
                    const_0:300.0 -> 2_LPF[1:frequency]
                    1_In[0] -> 3_BinaryOpUGen:SUBTRACTION[0:left]
                    2_LPF[0] -> 3_BinaryOpUGen:SUBTRACTION[1:right]
                    3_BinaryOpUGen:SUBTRACTION[0] -> 4_LPF[0:source]
                    const_1:1200.0 -> 4_LPF[1:frequency]
                    3_BinaryOpUGen:SUBTRACTION[0] -> 5_BinaryOpUGen:SUBTRACTION[0:left]
                    4_LPF[0] -> 5_BinaryOpUGen:SUBTRACTION[1:right]
                    5_BinaryOpUGen:SUBTRACTION[0] -> 6_LPF[0:source]
                    const_2:9600.0 -> 6_LPF[1:frequency]
                    5_BinaryOpUGen:SUBTRACTION[0] -> 7_BinaryOpUGen:SUBTRACTION[0:left]
                    6_LPF[0] -> 7_BinaryOpUGen:SUBTRACTION[1:right]
                    8_Control[2:band_1_pregain] -> 9_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    2_LPF[0] -> 10_BinaryOpUGen:MULTIPLICATION[0:left]
                    9_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 10_BinaryOpUGen:MULTIPLICATION[1:right]
                    10_BinaryOpUGen:MULTIPLICATION[0] -> 11_DelayN[0:source]
                    8_Control[0:band_1_clamp_time] -> 11_DelayN[1:maximum_delay_time]
                    8_Control[0:band_1_clamp_time] -> 11_DelayN[2:delay_time]
                    8_Control[6:band_1_threshold] -> 12_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    10_BinaryOpUGen:MULTIPLICATION[0] -> 13_Compander[0:source]
                    11_DelayN[0] -> 13_Compander[1:control]
                    12_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 13_Compander[2:threshold]
                    8_Control[5:band_1_slope_below] -> 13_Compander[3:slope_below]
                    8_Control[4:band_1_slope_above] -> 13_Compander[4:slope_above]
                    8_Control[0:band_1_clamp_time] -> 13_Compander[5:clamp_time]
                    8_Control[3:band_1_relax_time] -> 13_Compander[6:relax_time]
                    8_Control[1:band_1_postgain] -> 14_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    13_Compander[0] -> 15_BinaryOpUGen:MULTIPLICATION[0:left]
                    14_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 15_BinaryOpUGen:MULTIPLICATION[1:right]
                    8_Control[9:band_2_pregain] -> 16_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    4_LPF[0] -> 17_BinaryOpUGen:MULTIPLICATION[0:left]
                    16_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 17_BinaryOpUGen:MULTIPLICATION[1:right]
                    17_BinaryOpUGen:MULTIPLICATION[0] -> 18_DelayN[0:source]
                    8_Control[7:band_2_clamp_time] -> 18_DelayN[1:maximum_delay_time]
                    8_Control[7:band_2_clamp_time] -> 18_DelayN[2:delay_time]
                    8_Control[13:band_2_threshold] -> 19_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    17_BinaryOpUGen:MULTIPLICATION[0] -> 20_Compander[0:source]
                    18_DelayN[0] -> 20_Compander[1:control]
                    19_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 20_Compander[2:threshold]
                    8_Control[12:band_2_slope_below] -> 20_Compander[3:slope_below]
                    8_Control[11:band_2_slope_above] -> 20_Compander[4:slope_above]
                    8_Control[7:band_2_clamp_time] -> 20_Compander[5:clamp_time]
                    8_Control[10:band_2_relax_time] -> 20_Compander[6:relax_time]
                    8_Control[8:band_2_postgain] -> 21_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    20_Compander[0] -> 22_BinaryOpUGen:MULTIPLICATION[0:left]
                    21_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 22_BinaryOpUGen:MULTIPLICATION[1:right]
                    8_Control[16:band_3_pregain] -> 23_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    6_LPF[0] -> 24_BinaryOpUGen:MULTIPLICATION[0:left]
                    23_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 24_BinaryOpUGen:MULTIPLICATION[1:right]
                    24_BinaryOpUGen:MULTIPLICATION[0] -> 25_DelayN[0:source]
                    8_Control[14:band_3_clamp_time] -> 25_DelayN[1:maximum_delay_time]
                    8_Control[14:band_3_clamp_time] -> 25_DelayN[2:delay_time]
                    8_Control[20:band_3_threshold] -> 26_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    24_BinaryOpUGen:MULTIPLICATION[0] -> 27_Compander[0:source]
                    25_DelayN[0] -> 27_Compander[1:control]
                    26_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 27_Compander[2:threshold]
                    8_Control[19:band_3_slope_below] -> 27_Compander[3:slope_below]
                    8_Control[18:band_3_slope_above] -> 27_Compander[4:slope_above]
                    8_Control[14:band_3_clamp_time] -> 27_Compander[5:clamp_time]
                    8_Control[17:band_3_relax_time] -> 27_Compander[6:relax_time]
                    8_Control[15:band_3_postgain] -> 28_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    27_Compander[0] -> 29_BinaryOpUGen:MULTIPLICATION[0:left]
                    28_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 29_BinaryOpUGen:MULTIPLICATION[1:right]
                    8_Control[23:band_4_pregain] -> 30_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    7_BinaryOpUGen:SUBTRACTION[0] -> 31_BinaryOpUGen:MULTIPLICATION[0:left]
                    30_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 31_BinaryOpUGen:MULTIPLICATION[1:right]
                    31_BinaryOpUGen:MULTIPLICATION[0] -> 32_DelayN[0:source]
                    8_Control[21:band_4_clamp_time] -> 32_DelayN[1:maximum_delay_time]
                    8_Control[21:band_4_clamp_time] -> 32_DelayN[2:delay_time]
                    8_Control[27:band_4_threshold] -> 33_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    31_BinaryOpUGen:MULTIPLICATION[0] -> 34_Compander[0:source]
                    32_DelayN[0] -> 34_Compander[1:control]
                    33_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 34_Compander[2:threshold]
                    8_Control[26:band_4_slope_below] -> 34_Compander[3:slope_below]
                    8_Control[25:band_4_slope_above] -> 34_Compander[4:slope_above]
                    8_Control[21:band_4_clamp_time] -> 34_Compander[5:clamp_time]
                    8_Control[24:band_4_relax_time] -> 34_Compander[6:relax_time]
                    8_Control[22:band_4_postgain] -> 35_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    34_Compander[0] -> 36_BinaryOpUGen:MULTIPLICATION[0:left]
                    35_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 36_BinaryOpUGen:MULTIPLICATION[1:right]
                    15_BinaryOpUGen:MULTIPLICATION[0] -> 37_Sum4[0:input_one]
                    22_BinaryOpUGen:MULTIPLICATION[0] -> 37_Sum4[1:input_two]
                    29_BinaryOpUGen:MULTIPLICATION[0] -> 37_Sum4[2:input_three]
                    36_BinaryOpUGen:MULTIPLICATION[0] -> 37_Sum4[3:input_four]
                    0_Control[0:out] -> 38_XOut[0:bus]
                    8_Control[28:crossfade] -> 38_XOut[1:crossfade]
                    37_Sum4[0] -> 38_XOut[2:source]
                }

        ..  container:: example

            The above factory can be parameterized to use smaller or larger
            numbers of bands during the build stage:

            ::

                >>> frequencies = (150, 300, 600, 1200, 2400, 4800, 9600)
                >>> synthdef = factory.build(frequencies=frequencies)
                >>> graph(synthdef)  # doctest: +SKIP

            ..  doctest::

                >>> print(synthdef)
                SynthDef ... {
                    0_Control[0:out] -> 1_In[0:bus]
                    1_In[0] -> 2_LPF[0:source]
                    const_0:150.0 -> 2_LPF[1:frequency]
                    1_In[0] -> 3_BinaryOpUGen:SUBTRACTION[0:left]
                    2_LPF[0] -> 3_BinaryOpUGen:SUBTRACTION[1:right]
                    3_BinaryOpUGen:SUBTRACTION[0] -> 4_LPF[0:source]
                    const_1:300.0 -> 4_LPF[1:frequency]
                    3_BinaryOpUGen:SUBTRACTION[0] -> 5_BinaryOpUGen:SUBTRACTION[0:left]
                    4_LPF[0] -> 5_BinaryOpUGen:SUBTRACTION[1:right]
                    5_BinaryOpUGen:SUBTRACTION[0] -> 6_LPF[0:source]
                    const_2:600.0 -> 6_LPF[1:frequency]
                    5_BinaryOpUGen:SUBTRACTION[0] -> 7_BinaryOpUGen:SUBTRACTION[0:left]
                    6_LPF[0] -> 7_BinaryOpUGen:SUBTRACTION[1:right]
                    7_BinaryOpUGen:SUBTRACTION[0] -> 8_LPF[0:source]
                    const_3:1200.0 -> 8_LPF[1:frequency]
                    7_BinaryOpUGen:SUBTRACTION[0] -> 9_BinaryOpUGen:SUBTRACTION[0:left]
                    8_LPF[0] -> 9_BinaryOpUGen:SUBTRACTION[1:right]
                    9_BinaryOpUGen:SUBTRACTION[0] -> 10_LPF[0:source]
                    const_4:2400.0 -> 10_LPF[1:frequency]
                    9_BinaryOpUGen:SUBTRACTION[0] -> 11_BinaryOpUGen:SUBTRACTION[0:left]
                    10_LPF[0] -> 11_BinaryOpUGen:SUBTRACTION[1:right]
                    11_BinaryOpUGen:SUBTRACTION[0] -> 12_LPF[0:source]
                    const_5:4800.0 -> 12_LPF[1:frequency]
                    11_BinaryOpUGen:SUBTRACTION[0] -> 13_BinaryOpUGen:SUBTRACTION[0:left]
                    12_LPF[0] -> 13_BinaryOpUGen:SUBTRACTION[1:right]
                    13_BinaryOpUGen:SUBTRACTION[0] -> 14_LPF[0:source]
                    const_6:9600.0 -> 14_LPF[1:frequency]
                    13_BinaryOpUGen:SUBTRACTION[0] -> 15_BinaryOpUGen:SUBTRACTION[0:left]
                    14_LPF[0] -> 15_BinaryOpUGen:SUBTRACTION[1:right]
                    16_Control[2:band_1_pregain] -> 17_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    2_LPF[0] -> 18_BinaryOpUGen:MULTIPLICATION[0:left]
                    17_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 18_BinaryOpUGen:MULTIPLICATION[1:right]
                    18_BinaryOpUGen:MULTIPLICATION[0] -> 19_DelayN[0:source]
                    16_Control[0:band_1_clamp_time] -> 19_DelayN[1:maximum_delay_time]
                    16_Control[0:band_1_clamp_time] -> 19_DelayN[2:delay_time]
                    16_Control[6:band_1_threshold] -> 20_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    18_BinaryOpUGen:MULTIPLICATION[0] -> 21_Compander[0:source]
                    19_DelayN[0] -> 21_Compander[1:control]
                    20_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 21_Compander[2:threshold]
                    16_Control[5:band_1_slope_below] -> 21_Compander[3:slope_below]
                    16_Control[4:band_1_slope_above] -> 21_Compander[4:slope_above]
                    16_Control[0:band_1_clamp_time] -> 21_Compander[5:clamp_time]
                    16_Control[3:band_1_relax_time] -> 21_Compander[6:relax_time]
                    16_Control[1:band_1_postgain] -> 22_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    21_Compander[0] -> 23_BinaryOpUGen:MULTIPLICATION[0:left]
                    22_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 23_BinaryOpUGen:MULTIPLICATION[1:right]
                    16_Control[9:band_2_pregain] -> 24_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    4_LPF[0] -> 25_BinaryOpUGen:MULTIPLICATION[0:left]
                    24_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 25_BinaryOpUGen:MULTIPLICATION[1:right]
                    25_BinaryOpUGen:MULTIPLICATION[0] -> 26_DelayN[0:source]
                    16_Control[7:band_2_clamp_time] -> 26_DelayN[1:maximum_delay_time]
                    16_Control[7:band_2_clamp_time] -> 26_DelayN[2:delay_time]
                    16_Control[13:band_2_threshold] -> 27_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    25_BinaryOpUGen:MULTIPLICATION[0] -> 28_Compander[0:source]
                    26_DelayN[0] -> 28_Compander[1:control]
                    27_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 28_Compander[2:threshold]
                    16_Control[12:band_2_slope_below] -> 28_Compander[3:slope_below]
                    16_Control[11:band_2_slope_above] -> 28_Compander[4:slope_above]
                    16_Control[7:band_2_clamp_time] -> 28_Compander[5:clamp_time]
                    16_Control[10:band_2_relax_time] -> 28_Compander[6:relax_time]
                    16_Control[8:band_2_postgain] -> 29_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    28_Compander[0] -> 30_BinaryOpUGen:MULTIPLICATION[0:left]
                    29_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 30_BinaryOpUGen:MULTIPLICATION[1:right]
                    16_Control[16:band_3_pregain] -> 31_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    6_LPF[0] -> 32_BinaryOpUGen:MULTIPLICATION[0:left]
                    31_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 32_BinaryOpUGen:MULTIPLICATION[1:right]
                    32_BinaryOpUGen:MULTIPLICATION[0] -> 33_DelayN[0:source]
                    16_Control[14:band_3_clamp_time] -> 33_DelayN[1:maximum_delay_time]
                    16_Control[14:band_3_clamp_time] -> 33_DelayN[2:delay_time]
                    16_Control[20:band_3_threshold] -> 34_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    32_BinaryOpUGen:MULTIPLICATION[0] -> 35_Compander[0:source]
                    33_DelayN[0] -> 35_Compander[1:control]
                    34_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 35_Compander[2:threshold]
                    16_Control[19:band_3_slope_below] -> 35_Compander[3:slope_below]
                    16_Control[18:band_3_slope_above] -> 35_Compander[4:slope_above]
                    16_Control[14:band_3_clamp_time] -> 35_Compander[5:clamp_time]
                    16_Control[17:band_3_relax_time] -> 35_Compander[6:relax_time]
                    16_Control[15:band_3_postgain] -> 36_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    35_Compander[0] -> 37_BinaryOpUGen:MULTIPLICATION[0:left]
                    36_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 37_BinaryOpUGen:MULTIPLICATION[1:right]
                    16_Control[23:band_4_pregain] -> 38_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    8_LPF[0] -> 39_BinaryOpUGen:MULTIPLICATION[0:left]
                    38_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 39_BinaryOpUGen:MULTIPLICATION[1:right]
                    39_BinaryOpUGen:MULTIPLICATION[0] -> 40_DelayN[0:source]
                    16_Control[21:band_4_clamp_time] -> 40_DelayN[1:maximum_delay_time]
                    16_Control[21:band_4_clamp_time] -> 40_DelayN[2:delay_time]
                    16_Control[27:band_4_threshold] -> 41_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    39_BinaryOpUGen:MULTIPLICATION[0] -> 42_Compander[0:source]
                    40_DelayN[0] -> 42_Compander[1:control]
                    41_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 42_Compander[2:threshold]
                    16_Control[26:band_4_slope_below] -> 42_Compander[3:slope_below]
                    16_Control[25:band_4_slope_above] -> 42_Compander[4:slope_above]
                    16_Control[21:band_4_clamp_time] -> 42_Compander[5:clamp_time]
                    16_Control[24:band_4_relax_time] -> 42_Compander[6:relax_time]
                    16_Control[22:band_4_postgain] -> 43_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    42_Compander[0] -> 44_BinaryOpUGen:MULTIPLICATION[0:left]
                    43_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 44_BinaryOpUGen:MULTIPLICATION[1:right]
                    23_BinaryOpUGen:MULTIPLICATION[0] -> 45_Sum4[0:input_one]
                    30_BinaryOpUGen:MULTIPLICATION[0] -> 45_Sum4[1:input_two]
                    37_BinaryOpUGen:MULTIPLICATION[0] -> 45_Sum4[2:input_three]
                    44_BinaryOpUGen:MULTIPLICATION[0] -> 45_Sum4[3:input_four]
                    16_Control[30:band_5_pregain] -> 46_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    10_LPF[0] -> 47_BinaryOpUGen:MULTIPLICATION[0:left]
                    46_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 47_BinaryOpUGen:MULTIPLICATION[1:right]
                    47_BinaryOpUGen:MULTIPLICATION[0] -> 48_DelayN[0:source]
                    16_Control[28:band_5_clamp_time] -> 48_DelayN[1:maximum_delay_time]
                    16_Control[28:band_5_clamp_time] -> 48_DelayN[2:delay_time]
                    16_Control[34:band_5_threshold] -> 49_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    47_BinaryOpUGen:MULTIPLICATION[0] -> 50_Compander[0:source]
                    48_DelayN[0] -> 50_Compander[1:control]
                    49_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 50_Compander[2:threshold]
                    16_Control[33:band_5_slope_below] -> 50_Compander[3:slope_below]
                    16_Control[32:band_5_slope_above] -> 50_Compander[4:slope_above]
                    16_Control[28:band_5_clamp_time] -> 50_Compander[5:clamp_time]
                    16_Control[31:band_5_relax_time] -> 50_Compander[6:relax_time]
                    16_Control[29:band_5_postgain] -> 51_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    50_Compander[0] -> 52_BinaryOpUGen:MULTIPLICATION[0:left]
                    51_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 52_BinaryOpUGen:MULTIPLICATION[1:right]
                    16_Control[37:band_6_pregain] -> 53_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    12_LPF[0] -> 54_BinaryOpUGen:MULTIPLICATION[0:left]
                    53_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 54_BinaryOpUGen:MULTIPLICATION[1:right]
                    54_BinaryOpUGen:MULTIPLICATION[0] -> 55_DelayN[0:source]
                    16_Control[35:band_6_clamp_time] -> 55_DelayN[1:maximum_delay_time]
                    16_Control[35:band_6_clamp_time] -> 55_DelayN[2:delay_time]
                    16_Control[41:band_6_threshold] -> 56_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    54_BinaryOpUGen:MULTIPLICATION[0] -> 57_Compander[0:source]
                    55_DelayN[0] -> 57_Compander[1:control]
                    56_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 57_Compander[2:threshold]
                    16_Control[40:band_6_slope_below] -> 57_Compander[3:slope_below]
                    16_Control[39:band_6_slope_above] -> 57_Compander[4:slope_above]
                    16_Control[35:band_6_clamp_time] -> 57_Compander[5:clamp_time]
                    16_Control[38:band_6_relax_time] -> 57_Compander[6:relax_time]
                    16_Control[36:band_6_postgain] -> 58_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    57_Compander[0] -> 59_BinaryOpUGen:MULTIPLICATION[0:left]
                    58_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 59_BinaryOpUGen:MULTIPLICATION[1:right]
                    16_Control[44:band_7_pregain] -> 60_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    14_LPF[0] -> 61_BinaryOpUGen:MULTIPLICATION[0:left]
                    60_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 61_BinaryOpUGen:MULTIPLICATION[1:right]
                    61_BinaryOpUGen:MULTIPLICATION[0] -> 62_DelayN[0:source]
                    16_Control[42:band_7_clamp_time] -> 62_DelayN[1:maximum_delay_time]
                    16_Control[42:band_7_clamp_time] -> 62_DelayN[2:delay_time]
                    16_Control[48:band_7_threshold] -> 63_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    61_BinaryOpUGen:MULTIPLICATION[0] -> 64_Compander[0:source]
                    62_DelayN[0] -> 64_Compander[1:control]
                    63_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 64_Compander[2:threshold]
                    16_Control[47:band_7_slope_below] -> 64_Compander[3:slope_below]
                    16_Control[46:band_7_slope_above] -> 64_Compander[4:slope_above]
                    16_Control[42:band_7_clamp_time] -> 64_Compander[5:clamp_time]
                    16_Control[45:band_7_relax_time] -> 64_Compander[6:relax_time]
                    16_Control[43:band_7_postgain] -> 65_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    64_Compander[0] -> 66_BinaryOpUGen:MULTIPLICATION[0:left]
                    65_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 66_BinaryOpUGen:MULTIPLICATION[1:right]
                    16_Control[51:band_8_pregain] -> 67_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    15_BinaryOpUGen:SUBTRACTION[0] -> 68_BinaryOpUGen:MULTIPLICATION[0:left]
                    67_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 68_BinaryOpUGen:MULTIPLICATION[1:right]
                    68_BinaryOpUGen:MULTIPLICATION[0] -> 69_DelayN[0:source]
                    16_Control[49:band_8_clamp_time] -> 69_DelayN[1:maximum_delay_time]
                    16_Control[49:band_8_clamp_time] -> 69_DelayN[2:delay_time]
                    16_Control[55:band_8_threshold] -> 70_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    68_BinaryOpUGen:MULTIPLICATION[0] -> 71_Compander[0:source]
                    69_DelayN[0] -> 71_Compander[1:control]
                    70_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 71_Compander[2:threshold]
                    16_Control[54:band_8_slope_below] -> 71_Compander[3:slope_below]
                    16_Control[53:band_8_slope_above] -> 71_Compander[4:slope_above]
                    16_Control[49:band_8_clamp_time] -> 71_Compander[5:clamp_time]
                    16_Control[52:band_8_relax_time] -> 71_Compander[6:relax_time]
                    16_Control[50:band_8_postgain] -> 72_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                    71_Compander[0] -> 73_BinaryOpUGen:MULTIPLICATION[0:left]
                    72_UnaryOpUGen:DB_TO_AMPLITUDE[0] -> 73_BinaryOpUGen:MULTIPLICATION[1:right]
                    52_BinaryOpUGen:MULTIPLICATION[0] -> 74_Sum4[0:input_one]
                    59_BinaryOpUGen:MULTIPLICATION[0] -> 74_Sum4[1:input_two]
                    66_BinaryOpUGen:MULTIPLICATION[0] -> 74_Sum4[2:input_three]
                    73_BinaryOpUGen:MULTIPLICATION[0] -> 74_Sum4[3:input_four]
                    45_Sum4[0] -> 75_BinaryOpUGen:ADDITION[0:left]
                    74_Sum4[0] -> 75_BinaryOpUGen:ADDITION[1:right]
                    0_Control[0:out] -> 76_XOut[0:bus]
                    16_Control[56:crossfade] -> 76_XOut[1:crossfade]
                    75_BinaryOpUGen:ADDITION[0] -> 76_XOut[2:source]
                }

        """
        clone = self._clone()
        clone._parameter_blocks.append(block_function)
        return clone

    def with_rand_id(self, rand_id=0):
        """
        Return a new factory configured with a random number generator ID.

        ..  container:: example

            ::

                >>> factory = synthdeftools.SynthDefFactory()

            ::

                >>> def signal_block(builder, source, state):
                ...     iterations = state.get('iterations') or 2
                ...     for _ in range(iterations):
                ...         source = ugentools.AllpassC.ar(
                ...             decay_time=ugentools.ExpRand.ir(0.01, 0.1),
                ...             delay_time=ugentools.ExpRand.ir(0.01, 0.1),
                ...             source=source,
                ...             maximum_delay_time=0.1,
                ...             )
                ...     return source

            ::

                >>> factory = factory.with_input()
                >>> factory = factory.with_output()
                >>> factory = factory.with_signal_block(signal_block)

        ..  container:: example

            Configure the factory with a random number generator ID, defaulting
            to 23:

            ::

                >>> factory = factory.with_rand_id(rand_id=23)
                >>> synthdef = factory.build()
                >>> graph(synthdef)  # doctest: +SKIP

            ..  doctest::

                >>> print(synthdef)
                SynthDef ... {
                    0_Control[1:rand_id] -> 1_RandID[0:rand_id]
                    0_Control[0:out] -> 2_In[0:bus]
                    const_0:0.1 -> 3_ExpRand[0:minimum]
                    const_1:0.01 -> 3_ExpRand[1:maximum]
                    const_0:0.1 -> 4_ExpRand[0:minimum]
                    const_1:0.01 -> 4_ExpRand[1:maximum]
                    2_In[0] -> 5_AllpassC[0:source]
                    const_0:0.1 -> 5_AllpassC[1:maximum_delay_time]
                    4_ExpRand[0] -> 5_AllpassC[2:delay_time]
                    3_ExpRand[0] -> 5_AllpassC[3:decay_time]
                    const_0:0.1 -> 6_ExpRand[0:minimum]
                    const_1:0.01 -> 6_ExpRand[1:maximum]
                    const_0:0.1 -> 7_ExpRand[0:minimum]
                    const_1:0.01 -> 7_ExpRand[1:maximum]
                    5_AllpassC[0] -> 8_AllpassC[0:source]
                    const_0:0.1 -> 8_AllpassC[1:maximum_delay_time]
                    7_ExpRand[0] -> 8_AllpassC[2:delay_time]
                    6_ExpRand[0] -> 8_AllpassC[3:decay_time]
                    0_Control[0:out] -> 9_Out[0:bus]
                    8_AllpassC[0] -> 9_Out[1:source]
                }

        """
        clone = self._clone()
        if rand_id is not None:
            clone._rand_id = int(rand_id)
        else:
            clone._rand_id = None
        return clone

    def with_signal_block(self, block_function):
        """
        Return a new factory configured with an additional signal block
        function.

        Signal block functions take three parameters:

        builder
            the SynthDef builder instance

        source
            a UGenMethodMixin representing the signal flow

        state
            a dictionary of arbitrary key/value pairs for parameterizing the
            signal and parameter block functions

        Signal block functions should return a UGenMethodMixin.

        ..  container:: example

            ::

                >>> factory = synthdeftools.SynthDefFactory()

            ::

                >>> def signal_block(builder, source, state):
                ...     iterations = state.get('iterations') or 2
                ...     for _ in range(iterations):
                ...         source = ugentools.AllpassC.ar(
                ...             decay_time=ugentools.ExpRand.ir(0.01, 0.1),
                ...             delay_time=ugentools.ExpRand.ir(0.01, 0.1),
                ...             source=source,
                ...             maximum_delay_time=0.1,
                ...             )
                ...     return source

            ::

                >>> factory = factory.with_input()
                >>> factory = factory.with_output()
                >>> factory = factory.with_signal_block(signal_block)

        ..  container:: example

            Configure the factory with an additional signal block:

            ::

                >>> def signal_block_post(builder, source, state):
                ...     source = ugentools.LeakDC.ar(source=source)
                ...     source = ugentools.Limiter.ar(
                ...         duration=ugentools.Rand.ir(0.005, 0.015),
                ...         source=source,
                ...         )
                ...     return source

            ::

                >>> factory = factory.with_signal_block(signal_block_post)
                >>> synthdef = factory.build()
                >>> graph(synthdef)  # doctest: +SKIP

            ..  doctest::

                >>> print(synthdef)
                SynthDef ... {
                    0_Control[0:out] -> 1_In[0:bus]
                    const_0:0.1 -> 2_ExpRand[0:minimum]
                    const_1:0.01 -> 2_ExpRand[1:maximum]
                    const_0:0.1 -> 3_ExpRand[0:minimum]
                    const_1:0.01 -> 3_ExpRand[1:maximum]
                    1_In[0] -> 4_AllpassC[0:source]
                    const_0:0.1 -> 4_AllpassC[1:maximum_delay_time]
                    3_ExpRand[0] -> 4_AllpassC[2:delay_time]
                    2_ExpRand[0] -> 4_AllpassC[3:decay_time]
                    const_0:0.1 -> 5_ExpRand[0:minimum]
                    const_1:0.01 -> 5_ExpRand[1:maximum]
                    const_0:0.1 -> 6_ExpRand[0:minimum]
                    const_1:0.01 -> 6_ExpRand[1:maximum]
                    4_AllpassC[0] -> 7_AllpassC[0:source]
                    const_0:0.1 -> 7_AllpassC[1:maximum_delay_time]
                    6_ExpRand[0] -> 7_AllpassC[2:delay_time]
                    5_ExpRand[0] -> 7_AllpassC[3:decay_time]
                    7_AllpassC[0] -> 8_LeakDC[0:source]
                    const_2:0.995 -> 8_LeakDC[1:coefficient]
                    const_3:0.005 -> 9_Rand[0:minimum]
                    const_4:0.015 -> 9_Rand[1:maximum]
                    8_LeakDC[0] -> 10_Limiter[0:source]
                    const_5:1.0 -> 10_Limiter[1:level]
                    9_Rand[0] -> 10_Limiter[2:duration]
                    0_Control[0:out] -> 11_Out[0:bus]
                    10_Limiter[0] -> 11_Out[1:source]
                }

        """
        clone = self._clone()
        clone._signal_blocks.append(block_function)
        return clone

    def with_silence_detection(self):
        """
        Return a new factory configured with silence detection.

        ..  container:: example

            ::

                >>> factory = synthdeftools.SynthDefFactory()

            ::

                >>> def signal_block(builder, source, state):
                ...     iterations = state.get('iterations') or 2
                ...     for _ in range(iterations):
                ...         source = ugentools.AllpassC.ar(
                ...             decay_time=ugentools.ExpRand.ir(0.01, 0.1),
                ...             delay_time=ugentools.ExpRand.ir(0.01, 0.1),
                ...             source=source,
                ...             maximum_delay_time=0.1,
                ...             )
                ...     return source

            ::

                >>> factory = factory.with_input()
                >>> factory = factory.with_output()
                >>> factory = factory.with_signal_block(signal_block)

        ..  container:: example

            Configure the factory with silence detection.

            ::

                >>> factory = factory.with_silence_detection()
                >>> synthdef = factory.build()
                >>> graph(synthdef)  # doctest: +SKIP

            ..  doctest::

                >>> print(synthdef)
                SynthDef ... {
                    0_Control[0:out] -> 1_In[0:bus]
                    const_0:0.1 -> 2_ExpRand[0:minimum]
                    const_1:0.01 -> 2_ExpRand[1:maximum]
                    const_0:0.1 -> 3_ExpRand[0:minimum]
                    const_1:0.01 -> 3_ExpRand[1:maximum]
                    1_In[0] -> 4_AllpassC[0:source]
                    const_0:0.1 -> 4_AllpassC[1:maximum_delay_time]
                    3_ExpRand[0] -> 4_AllpassC[2:delay_time]
                    2_ExpRand[0] -> 4_AllpassC[3:decay_time]
                    const_0:0.1 -> 5_ExpRand[0:minimum]
                    const_1:0.01 -> 5_ExpRand[1:maximum]
                    const_0:0.1 -> 6_ExpRand[0:minimum]
                    const_1:0.01 -> 6_ExpRand[1:maximum]
                    4_AllpassC[0] -> 7_AllpassC[0:source]
                    const_0:0.1 -> 7_AllpassC[1:maximum_delay_time]
                    6_ExpRand[0] -> 7_AllpassC[2:delay_time]
                    5_ExpRand[0] -> 7_AllpassC[3:decay_time]
                    0_Control[0:out] -> 8_Out[0:bus]
                    7_AllpassC[0] -> 8_Out[1:source]
                    7_AllpassC[0] -> 9_DetectSilence[0:source]
                    const_2:0.0001 -> 9_DetectSilence[1:threshold]
                    const_0:0.1 -> 9_DetectSilence[2:time]
                    const_3:2.0 -> 9_DetectSilence[3:done_action]
                }

        ..  container:: example

            Silence detection is applied before any output leveling or
            windowing.

            ::

                >>> factory = factory.with_output(
                ...     leveled=True,
                ...     windowed=True,
                ...     )
                >>> synthdef = factory.build()
                >>> graph(synthdef)  # doctest: +SKIP

            ..  doctest::

                >>> print(synthdef)
                SynthDef ... {
                    const_0:0.0 -> 1_Line[0:start]
                    const_1:1.0 -> 1_Line[1:stop]
                    0_Control[0:duration] -> 1_Line[2:duration]
                    const_2:2.0 -> 1_Line[3:done_action]
                    1_Line[0] -> 2_UnaryOpUGen:HANNING_WINDOW[0:source]
                    0_Control[1:out] -> 3_In[0:bus]
                    const_3:0.1 -> 5_ExpRand[0:minimum]
                    const_4:0.01 -> 5_ExpRand[1:maximum]
                    const_3:0.1 -> 6_ExpRand[0:minimum]
                    const_4:0.01 -> 6_ExpRand[1:maximum]
                    3_In[0] -> 7_AllpassC[0:source]
                    const_3:0.1 -> 7_AllpassC[1:maximum_delay_time]
                    6_ExpRand[0] -> 7_AllpassC[2:delay_time]
                    5_ExpRand[0] -> 7_AllpassC[3:decay_time]
                    const_3:0.1 -> 8_ExpRand[0:minimum]
                    const_4:0.01 -> 8_ExpRand[1:maximum]
                    const_3:0.1 -> 9_ExpRand[0:minimum]
                    const_4:0.01 -> 9_ExpRand[1:maximum]
                    7_AllpassC[0] -> 10_AllpassC[0:source]
                    const_3:0.1 -> 10_AllpassC[1:maximum_delay_time]
                    9_ExpRand[0] -> 10_AllpassC[2:delay_time]
                    8_ExpRand[0] -> 10_AllpassC[3:decay_time]
                    10_AllpassC[0] -> 11_BinaryOpUGen:MULTIPLICATION[0:left]
                    4_Control[0:level] -> 11_BinaryOpUGen:MULTIPLICATION[1:right]
                    11_BinaryOpUGen:MULTIPLICATION[0] -> 12_BinaryOpUGen:MULTIPLICATION[0:left]
                    2_UnaryOpUGen:HANNING_WINDOW[0] -> 12_BinaryOpUGen:MULTIPLICATION[1:right]
                    0_Control[1:out] -> 13_Out[0:bus]
                    12_BinaryOpUGen:MULTIPLICATION[0] -> 13_Out[1:source]
                    10_AllpassC[0] -> 14_DetectSilence[0:source]
                    const_5:0.0001 -> 14_DetectSilence[1:threshold]
                    const_3:0.1 -> 14_DetectSilence[2:time]
                    const_2:2.0 -> 14_DetectSilence[3:done_action]
                }

        """
        clone = self._clone()
        clone._silence_detection = True
        return clone
