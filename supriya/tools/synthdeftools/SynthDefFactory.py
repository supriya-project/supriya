# -*- encoding: utf-8 -*-
import copy
import types
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class SynthDefFactory(SupriyaObject):

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
        self._signal_blocks = []
        self._silence_detection = None

    ### PRIVATE METHODS ###

    def _setup_parameters_and_state(self, builder, state):
        from supriya.tools import synthdeftools
        from supriya.tools import ugentools
        state['channel_count'] = self._channel_count
        for parameter_block in self._parameter_blocks:
            parameter_block(builder, state)
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
            channel_count=self._channel_count,
            )
        if self._input.get('windowed'):
            source *= state['window']
        return source

    def _build_feedback_loop_input(self, builder, source, state):
        from supriya.tools import ugentools
        if self._feedback_loop:
            local_in = ugentools.LocalIn.ar(
                channel_count=self._channel_count,
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
        windowed = self._output.get('windowed')
        gate = state.get('gate')
        if self._output.get('leveled') and not crossfaded:
            source *= builder['level']
        out_class = ugentools.Out
        kwargs = dict(
            bus=builder['out'],
            source=source,
            )
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

    def build(self, **kwargs):
        from supriya.tools import synthdeftools
        from supriya.tools import ugentools
        builder = synthdeftools.SynthDefBuilder()
        state = self._initial_state.copy()
        state.update(**kwargs)
        with builder:
            self._setup_parameters_and_state(builder, state)
            source = self._build_input(builder, state)
            source = self._build_feedback_loop_input(builder, source, state)
            for signal_block in self._signal_blocks:
                source = signal_block(builder, source, state)
                assert isinstance(source, synthdeftools.UGenMethodMixin)
            self._build_output(builder, source, state)
            self._build_feedback_loop_output(builder, source, state)
            self._build_silence_detection(builder, source, state)
        return builder.build()

    def with_channel_count(self, channel_count):
        channel_count = int(channel_count)
        assert channel_count > 0
        clone = self._clone()
        clone._channel_count = channel_count
        return clone

    def with_feedback_loop(self, block_function=None):
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
        clone = self._clone()
        clone._gate.update(
            attack_time=float(attack_time),
            release_time=float(release_time),
            )
        return clone

    def with_initial_state(self, **state):
        clone = self._clone()
        clone._initial_state.update(**state)
        return clone

    def with_input(
        self,
        windowed=False,
        ):
        clone = self._clone()
        clone._input.update(
            windowed=bool(windowed),
            )
        return clone

    def with_output(
        self,
        crossfaded=False,
        leveled=False,
        windowed=False,
        ):
        clone = self._clone()
        clone._output.update(
            crossfaded=bool(crossfaded),
            leveled=bool(leveled),
            windowed=bool(windowed),
            )
        return clone

    def with_parameter_block(self, block_function):
        clone = self._clone()
        clone._parameter_blocks.append(block_function)
        return clone

    def with_signal_block(self, block_function):
        clone = self._clone()
        clone._signal_blocks.append(block_function)
        return clone

    def with_silence_detection(self):
        clone = self._clone()
        clone._silence_detection = True
        return clone
