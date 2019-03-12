import collections
import copy
import uuid
from typing import List

from supriya import utils
from supriya.system.SupriyaObject import SupriyaObject


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
        ...         ),
        ...     )

    ::

        >>> with builder:
        ...     sin_osc = supriya.ugens.SinOsc.ar(
        ...         frequency=builder['frequency'],
        ...         )
        ...     decay = supriya.ugens.Decay.kr(
        ...         decay_time=0.5,
        ...         source=builder['trigger'],
        ...         )
        ...     enveloped_sin = sin_osc * decay
        ...     out = supriya.ugens.Out.ar(bus=0, source=enveloped_sin)
        ...

    ::

        >>> synthdef = builder.build()
        >>> supriya.graph(synthdef)  # doctest: +SKIP

    """

    ### CLASS VARIABLES ###

    _active_builders: List["SynthDefBuilder"] = []

    __documentation_section__ = "Main Classes"

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

        if not isinstance(ugens, collections.Sequence):
            ugens = [ugens]
        prototype = (
            supriya.ugens.UGen,
            supriya.synthdefs.OutputProxy,
            supriya.synthdefs.Parameter,
        )
        for ugen in ugens:
            assert isinstance(ugen, prototype), type(ugen)
            if isinstance(ugen, supriya.synthdefs.OutputProxy):
                ugen = ugen.source
            assert ugen._uuid == self._uuid
            if ugen not in self._ugens:
                self._ugens.append(ugen)

    def _add_parameter(self, *args):
        import supriya.synthdefs

        if 3 < len(args):
            raise ValueError(args)
        if len(args) == 1:
            assert isinstance(args[0], supriya.synthdefs.Parameter)
            name, value, parameter_rate = args[0].name, args[0], args[0].parameter_rate
        elif len(args) == 2:
            name, value = args
            if not isinstance(value, supriya.synthdefs.Parameter):
                parameter_rate = supriya.ParameterRate.SCALAR
                if name.startswith("a_"):
                    parameter_rate = supriya.ParameterRate.AUDIO
                elif name.startswith("i_"):
                    parameter_rate = supriya.ParameterRate.SCALAR
                elif name.startswith("t_"):
                    parameter_rate = supriya.ParameterRate.TRIGGER
                else:
                    parameter_rate = supriya.ParameterRate.CONTROL
            else:
                parameter_rate = value.parameter_rate
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
            parameter = utils.new(value, parameter_rate=parameter_rate, name=name)
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
            ugen for ugen in self._ugens if not isinstance(ugen, supriya.ugens.Control)
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
