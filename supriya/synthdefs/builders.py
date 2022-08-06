import collections
import copy
import inspect
import threading
import uuid
from collections.abc import Sequence
from typing import List, Tuple, Union

from uqbar.objects import new

from supriya.enums import ParameterRate
from supriya.system import SupriyaObject

from .controls import Parameter

_local = threading.local()
_local._active_builders = []


class SynthDefBuilder(SupriyaObject):
    """
    A SynthDef builder.

    ::

        >>> import supriya.synthdefs
        >>> import supriya.ugens

    ::

        >>> builder = supriya.synthdefs.SynthDefBuilder(
        ...     frequency=440,
        ...     trigger=supriya.synthdefs.Parameter(
        ...         value=0,
        ...         parameter_rate=supriya.ParameterRate.TRIGGER,
        ...     ),
        ... )

    ::

        >>> with builder:
        ...     sin_osc = supriya.ugens.SinOsc.ar(
        ...         frequency=builder["frequency"],
        ...     )
        ...     decay = supriya.ugens.Decay.kr(
        ...         decay_time=0.5,
        ...         source=builder["trigger"],
        ...     )
        ...     enveloped_sin = sin_osc * decay
        ...     out = supriya.ugens.Out.ar(bus=0, source=enveloped_sin)
        ...

    ::

        >>> synthdef = builder.build()
        >>> supriya.graph(synthdef)  # doctest: +SKIP

    """

    ### CLASS VARIABLES ###

    _active_builders: List["SynthDefBuilder"] = _local._active_builders

    __slots__ = ("_name", "_parameters", "_ugens", "_uuid")

    ### INITIALIZER ###

    def __init__(self, name=None, **kwargs):
        self._name = name
        self._uuid = uuid.uuid4()
        self._parameters = collections.OrderedDict()
        self._ugens = []
        for key, value in kwargs.items():
            self._add_parameter(key, value)

    ### SPECIAL METHODS ###

    def __enter__(self):
        SynthDefBuilder._active_builders.append(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        SynthDefBuilder._active_builders.pop()

    def __getitem__(self, item):
        return self._parameters[item]

    ### PRIVATE METHODS ###

    def _add_ugens(self, ugens):
        import supriya.synthdefs
        import supriya.ugens

        if not isinstance(ugens, Sequence):
            ugens = [ugens]
        prototype = (
            supriya.synthdefs.OutputProxy,
            supriya.synthdefs.Parameter,
            supriya.synthdefs.UGen,
        )
        for ugen in ugens:
            assert isinstance(ugen, prototype), type(ugen)
            if isinstance(ugen, supriya.synthdefs.OutputProxy):
                ugen = ugen.source
            assert ugen._uuid == self._uuid
            if ugen not in self._ugens:
                self._ugens.append(ugen)

    def _add_parameter(self, *args):
        # TODO: Refactor without *args for clarity
        import supriya.synthdefs

        if 3 < len(args):
            raise ValueError(args)
        if len(args) == 1:
            assert isinstance(args[0], supriya.synthdefs.Parameter)
            name, value, parameter_rate = args[0].name, args[0], args[0].parameter_rate
        elif len(args) == 2:
            name, value = args
            if isinstance(value, supriya.synthdefs.Parameter):
                parameter_rate = value.parameter_rate
            else:
                parameter_rate = supriya.ParameterRate.CONTROL
                if name.startswith("a_"):
                    parameter_rate = supriya.ParameterRate.AUDIO
                elif name.startswith("i_"):
                    parameter_rate = supriya.ParameterRate.SCALAR
                elif name.startswith("t_"):
                    parameter_rate = supriya.ParameterRate.TRIGGER
        elif len(args) == 3:
            name, value, parameter_rate = args
            parameter_rate = supriya.ParameterRate.from_expr(parameter_rate)
        else:
            raise ValueError(args)
        if not isinstance(value, supriya.synthdefs.Parameter):
            parameter = supriya.synthdefs.Parameter(
                name=name, parameter_rate=parameter_rate, value=value
            )
        else:
            parameter = new(value, parameter_rate=parameter_rate, name=name)
        assert parameter._uuid is None
        parameter._uuid = self._uuid
        self._parameters[name] = parameter
        return parameter

    ### PUBLIC METHODS ###

    def build(self, name=None, optimize=True):
        import supriya.synthdefs
        import supriya.ugens

        # Calling build() creates controls each time, so strip out
        # previously created ones. This could be made cleaner by preventing
        # Control subclasses from being aggregated into SynthDefBuilders in
        # the first place.

        self._ugens[:] = [
            ugen
            for ugen in self._ugens
            if not isinstance(ugen, supriya.synthdefs.Control)
        ]
        name = self.name or name
        with self:
            ugens = list(self._parameters.values()) + list(self._ugens)
            ugens = copy.deepcopy(ugens)
            ugens, parameters = supriya.synthdefs.SynthDef._extract_parameters(ugens)
            (
                control_ugens,
                control_mapping,
                indexed_parameters,
            ) = supriya.synthdefs.SynthDef._build_control_mapping(parameters)
            supriya.synthdefs.SynthDef._remap_controls(ugens, control_mapping)
            ugens = control_ugens + ugens
            synthdef = supriya.synthdefs.SynthDef(ugens, name=name, optimize=optimize)
        return synthdef

    def poll_ugen(self, ugen, label=None, trigger=None, trigger_id=-1):
        import supriya.ugens

        if trigger is None:
            trigger = supriya.ugens.Impulse.kr(1)
        poll = supriya.ugens.Poll.new(
            source=ugen, label=label, trigger=trigger, trigger_id=trigger_id
        )
        self._add_ugens(poll)

    ### PUBLIC PROPERTIES ###

    @property
    def name(self):
        return self._name


def synthdef(*args: Union[str, Tuple[str, float]]):
    """
    Decorate for quickly constructing SynthDefs from functions.

    ::

        >>> from supriya.ugens import EnvGen, Out, SinOsc
        >>> from supriya.synthdefs import Envelope, synthdef

    ::

        >>> @synthdef()
        ... def sine(freq=440, amp=0.1, gate=1):
        ...     sig = SinOsc.ar(freq) * amp
        ...     env = EnvGen.kr(envelope=Envelope.adsr(), gate=gate, done_action=2)
        ...     Out.ar(0, [sig * env] * 2)
        ...

    ::

        >>> print(sine)
        synthdef:
            name: sine
            ugens:
            -   Control.kr: null
            -   SinOsc.ar:
                    frequency: Control.kr[1:freq]
                    phase: 0.0
            -   BinaryOpUGen(MULTIPLICATION).ar/0:
                    left: SinOsc.ar[0]
                    right: Control.kr[0:amp]
            -   EnvGen.kr:
                    gate: Control.kr[2:gate]
                    level_scale: 1.0
                    level_bias: 0.0
                    time_scale: 1.0
                    done_action: 2.0
                    envelope[0]: 0.0
                    envelope[1]: 3.0
                    envelope[2]: 2.0
                    envelope[3]: -99.0
                    envelope[4]: 1.0
                    envelope[5]: 0.01
                    envelope[6]: 5.0
                    envelope[7]: -4.0
                    envelope[8]: 0.5
                    envelope[9]: 0.3
                    envelope[10]: 5.0
                    envelope[11]: -4.0
                    envelope[12]: 0.0
                    envelope[13]: 1.0
                    envelope[14]: 5.0
                    envelope[15]: -4.0
            -   BinaryOpUGen(MULTIPLICATION).ar/1:
                    left: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                    right: EnvGen.kr[0]
            -   Out.ar:
                    bus: 0.0
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
                    source[1]: BinaryOpUGen(MULTIPLICATION).ar/1[0]

    ::

        >>> @synthdef("ar", ("kr", 0.5))
        ... def sine(freq=440, amp=0.1, gate=1):
        ...     sig = SinOsc.ar(freq) * amp
        ...     env = EnvGen.kr(envelope=Envelope.adsr(), gate=gate, done_action=2)
        ...     Out.ar(0, [sig * env] * 2)
        ...

    ::

        >>> print(sine)
        synthdef:
            name: sine
            ugens:
            -   AudioControl.ar: null
            -   SinOsc.ar:
                    frequency: AudioControl.ar[0:freq]
                    phase: 0.0
            -   LagControl.kr:
                    lags[0]: 0.5
                    lags[1]: 0.0
            -   BinaryOpUGen(MULTIPLICATION).ar/0:
                    left: SinOsc.ar[0]
                    right: LagControl.kr[0:amp]
            -   EnvGen.kr:
                    gate: LagControl.kr[1:gate]
                    level_scale: 1.0
                    level_bias: 0.0
                    time_scale: 1.0
                    done_action: 2.0
                    envelope[0]: 0.0
                    envelope[1]: 3.0
                    envelope[2]: 2.0
                    envelope[3]: -99.0
                    envelope[4]: 1.0
                    envelope[5]: 0.01
                    envelope[6]: 5.0
                    envelope[7]: -4.0
                    envelope[8]: 0.5
                    envelope[9]: 0.3
                    envelope[10]: 5.0
                    envelope[11]: -4.0
                    envelope[12]: 0.0
                    envelope[13]: 1.0
                    envelope[14]: 5.0
                    envelope[15]: -4.0
            -   BinaryOpUGen(MULTIPLICATION).ar/1:
                    left: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                    right: EnvGen.kr[0]
            -   Out.ar:
                    bus: 0.0
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
                    source[1]: BinaryOpUGen(MULTIPLICATION).ar/1[0]

    """

    def inner(func):
        signature = inspect.signature(func)
        builder = SynthDefBuilder()
        kwargs = {}
        for i, (name, parameter) in enumerate(signature.parameters.items()):
            rate = ParameterRate.CONTROL
            lag = None
            try:
                if isinstance(args[i], str):
                    rate_expr = args[i]
                else:
                    rate_expr, lag = args[i]
                rate = ParameterRate.from_expr(rate_expr)
            except (IndexError, TypeError):
                pass
            value = parameter.default
            if value is inspect._empty:
                value = 0.0
            parameter = Parameter(lag=lag, name=name, parameter_rate=rate, value=value)
            kwargs[name] = builder._add_parameter(parameter)
        with builder:
            func(**kwargs)
        return builder.build(name=func.__name__)

    return inner
