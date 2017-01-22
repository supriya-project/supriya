# -*- encoding: utf-8 -*-
import collections
import copy
import uuid
from abjad.tools.topleveltools import new
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class SynthDefBuilder(SupriyaObject):
    """
    A SynthDef builder.

    ::

        >>> from supriya.tools import synthdeftools
        >>> from supriya.tools import ugentools

    ::

        >>> builder = synthdeftools.SynthDefBuilder(
        ...     frequency=440,
        ...     trigger=synthdeftools.Parameter(
        ...         value=0,
        ...         parameter_rate=synthdeftools.ParameterRate.TRIGGER,
        ...         ),
        ...     )

    ::

        >>> with builder:
        ...     sin_osc = ugentools.SinOsc.ar(
        ...         frequency=builder['frequency'],
        ...         )
        ...     decay = ugentools.Decay.kr(
        ...         decay_time=0.5,
        ...         source=builder['trigger'],
        ...         )
        ...     enveloped_sin = sin_osc * decay
        ...     out = ugentools.Out.ar(bus=0, source=enveloped_sin)
        ...

    ::

        >>> synthdef = builder.build()
        >>> graph(synthdef)  # doctest: +SKIP

    """

    ### CLASS VARIABLES ###

    _active_builders = []

    __documentation_section__ = 'Main Classes'

    __slots__ = (
        '_parameters',
        '_ugens',
        '_uuid',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        name=None,
        **kwargs
        ):
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
        from supriya.tools import synthdeftools
        from supriya.tools import ugentools
        if not isinstance(ugens, collections.Sequence):
            ugens = [ugens]
        prototype = (
            ugentools.UGen,
            synthdeftools.OutputProxy,
            synthdeftools.Parameter,
            )
        for ugen in ugens:
            assert isinstance(ugen, prototype), type(ugen)
            if isinstance(ugen, synthdeftools.OutputProxy):
                ugen = ugen.source
            assert ugen._uuid == self._uuid
            if ugen not in self._ugens:
                self._ugens.append(ugen)

    def _add_parameter(self, *args):
        from supriya.tools import synthdeftools
        if 3 < len(args):
            raise ValueError(args)
        if len(args) == 1:
            assert isinstance(args[0], synthdeftools.Parameter)
            name, value, parameter_rate = \
                args[0].name, args[0], args[0].parameter_rate
        elif len(args) == 2:
            name, value = args
            if not isinstance(value, synthdeftools.Parameter):
                parameter_rate = synthdeftools.ParameterRate.SCALAR
                if name.startswith('a_'):
                    parameter_rate = synthdeftools.ParameterRate.AUDIO
                elif name.startswith('i_'):
                    parameter_rate = synthdeftools.ParameterRate.SCALAR
                elif name.startswith('t_'):
                    parameter_rate = synthdeftools.ParameterRate.TRIGGER
                else:
                    parameter_rate = synthdeftools.ParameterRate.CONTROL
            else:
                parameter_rate = value.parameter_rate
        elif len(args) == 3:
            name, value, parameter_rate = args
            parameter_rate = synthdeftools.ParameterRate.from_expr(
                parameter_rate,
                )
        else:
            raise ValueError(args)
        if not isinstance(value, synthdeftools.Parameter):
            parameter = synthdeftools.Parameter(
                name=name,
                parameter_rate=parameter_rate,
                value=value,
                )
        else:
            parameter = new(
                value,
                parameter_rate=parameter_rate,
                name=name,
                )
        assert parameter._uuid is None
        parameter._uuid = self._uuid
        self._parameters[name] = parameter
        return parameter

    ### PUBLIC METHODS ###

    def build(self, name=None, optimize=True):
        from supriya.tools import synthdeftools
        with self:
            ugens = list(self._parameters.values()) + list(self._ugens)
            ugens = copy.deepcopy(ugens)
            ugens = synthdeftools.SynthDef._flatten_ugens(ugens)
            ugens, parameters = synthdeftools.SynthDef._extract_parameters(ugens)
            (
                control_ugens,
                control_mapping,
                indexed_parameters,
                ) = synthdeftools.SynthDef._build_control_mapping(parameters)
            synthdeftools.SynthDef._remap_controls(ugens, control_mapping)
            ugens = control_ugens + ugens
            synthdef = synthdeftools.SynthDef(
                ugens,
                name=name,
                optimize=optimize,
                )
        return synthdef

    def poll_ugen(
        self,
        ugen,
        label=None,
        trigger=None,
        trigger_id=-1,
        ):
        from supriya.tools import ugentools
        if trigger is None:
            trigger = ugentools.Impulse.kr(1)
        poll = ugentools.Poll.new(
            source=ugen,
            label=label,
            trigger=trigger,
            trigger_id=trigger_id,
            )
        self._add_ugens(poll)
