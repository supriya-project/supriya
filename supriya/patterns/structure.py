import uuid

from uqbar.objects import new

from supriya.patterns.bases import EventPattern


class Pbus(EventPattern):

    ### INITIALIZER ###

    def __init__(
        self, pattern, calculation_rate="audio", channel_count=None, release_time=0.25
    ):
        import supriya.synthdefs

        self._pattern = pattern
        calculation_rate = supriya.CalculationRate.from_expr(calculation_rate)
        assert calculation_rate in (
            supriya.CalculationRate.AUDIO,
            supriya.CalculationRate.CONTROL,
        )
        self._calculation_rate = calculation_rate
        if channel_count is not None:
            channel_count = int(channel_count)
            assert 0 < channel_count
        self._channel_count = channel_count
        release_time = float(release_time)
        assert 0 <= release_time
        self._release_time = release_time

    ### PRIVATE METHODS ###

    def _coerce_iterator_output(self, expr, state):
        import supriya.assets.synthdefs
        import supriya.patterns

        expr = super(Pbus, self)._coerce_iterator_output(expr)
        if isinstance(expr, supriya.patterns.NoteEvent) or not expr.get("is_stop"):
            kwargs = {}
            if expr.get("target_node") is None:
                kwargs["target_node"] = state["group_uuid"]
            prototype = (supriya.patterns.NoteEvent, supriya.patterns.SynthEvent)
            if isinstance(expr, prototype):
                synthdef = expr.get("synthdef") or supriya.assets.synthdefs.default
                parameter_names = synthdef.parameter_names
                if expr.get("out") is None and "out" in parameter_names:
                    kwargs["out"] = state["bus_uuid"]
                if expr.get("in_") is None and "in_" in parameter_names:
                    kwargs["in_"] = state["bus_uuid"]
            expr = new(expr, **kwargs)
        return expr

    def _iterate(self, state=None):
        return iter(self.pattern)

    def _setup_state(self):
        return {
            "bus_uuid": uuid.uuid4(),
            "link_uuid": uuid.uuid4(),
            "group_uuid": uuid.uuid4(),
        }

    def _setup_peripherals(self, initial_expr, state):
        import supriya.assets.synthdefs
        import supriya.patterns
        import supriya.synthdefs

        channel_count = self.channel_count
        if channel_count is None:
            synthdef = initial_expr.get("synthdef") or supriya.assets.synthdefs.default
            channel_count = synthdef.audio_output_channel_count
        if self.calculation_rate == supriya.CalculationRate.AUDIO:
            link_synthdef_name = "system_link_audio_{}".format(channel_count)
        else:
            link_synthdef_name = "system_link_control_{}".format(channel_count)
        link_synthdef = getattr(supriya.assets.synthdefs, link_synthdef_name)
        start_bus_event = supriya.patterns.BusEvent(
            calculation_rate=self.calculation_rate,
            channel_count=channel_count,
            uuid=state["bus_uuid"],
        )
        start_group_event = supriya.patterns.GroupEvent(uuid=state["group_uuid"])
        start_link_event = supriya.patterns.SynthEvent(
            add_action="ADD_AFTER",
            amplitude=1.0,
            fade_time=self.release_time,
            in_=state["bus_uuid"],
            synthdef=link_synthdef,
            target_node=state["group_uuid"],
            uuid=state["link_uuid"],
        )
        stop_link_event = supriya.patterns.SynthEvent(
            uuid=state["link_uuid"], is_stop=True
        )
        stop_group_event = supriya.patterns.GroupEvent(
            uuid=state["group_uuid"], is_stop=True
        )
        stop_bus_event = supriya.patterns.BusEvent(uuid=state["bus_uuid"], is_stop=True)
        peripheral_starts = [start_bus_event, start_group_event, start_link_event]
        peripheral_stops = [stop_link_event]
        delta = self._release_time or 0
        if delta:
            peripheral_stops.append(supriya.patterns.NullEvent(delta=delta))
        peripheral_stops.extend([stop_group_event, stop_bus_event])
        return peripheral_starts, peripheral_stops

    ### PUBLIC PROPERTIES ###

    @property
    def arity(self):
        return self._pattern.arity

    @property
    def calculation_rate(self):
        return self._calculation_rate

    @property
    def channel_count(self):
        return self._channel_count

    @property
    def is_infinite(self):
        return self._pattern.is_infinite

    @property
    def pattern(self):
        return self._pattern

    @property
    def release_time(self):
        return self._release_time


class Pfx(EventPattern):

    ### INITIALIZER ###

    def __init__(self, pattern, synthdef, release_time=0.25, **settings):
        import supriya.synthdefs

        self._pattern = pattern
        assert isinstance(synthdef, supriya.synthdefs.SynthDef)
        self._synthdef = synthdef
        release_time = float(release_time)
        assert 0 <= release_time
        self._release_time = release_time
        self._settings = tuple(sorted(settings.items()))

    ### PRIVATE METHODS ###

    def _iterate(self, state=None):
        return iter(self.pattern)

    def _setup_peripherals(self, initial_expr, state):
        import supriya.patterns

        start_synth_event = supriya.patterns.SynthEvent(
            add_action="ADD_TO_TAIL",
            synthdef=self.synthdef,
            uuid=state["synth_uuid"],
            **self.settings,
        )
        stop_synth_event = supriya.patterns.SynthEvent(
            uuid=state["synth_uuid"], is_stop=True
        )
        peripheral_starts = [start_synth_event]
        peripheral_stops = []
        delta = self._release_time or 0
        if delta:
            peripheral_stops.append(supriya.patterns.NullEvent(delta=delta))
        peripheral_stops.append(stop_synth_event)
        return peripheral_starts, peripheral_stops

    def _setup_state(self):
        return {"synth_uuid": uuid.uuid4()}

    ### PUBLIC PROPERTIES ###

    @property
    def arity(self):
        return self._pattern.arity

    @property
    def channel_count(self):
        return self._channel_count

    @property
    def is_infinite(self):
        return self._pattern.is_infinite

    @property
    def pattern(self):
        return self._pattern

    @property
    def release_time(self):
        return self._release_time

    @property
    def synthdef(self):
        return self._synthdef

    @property
    def settings(self):
        return dict(self._settings)


class Pgroup(EventPattern):

    ### INITIALIZER ###

    def __init__(self, pattern, release_time=0.25):
        self._pattern = pattern
        release_time = float(release_time)
        assert 0 <= release_time
        self._release_time = release_time

    ### PRIVATE METHODS ###

    def _coerce_iterator_output(self, expr, state):
        import supriya.patterns

        expr = super(Pgroup, self)._coerce_iterator_output(expr)
        if isinstance(expr, supriya.patterns.NoteEvent) or not expr.get("is_stop"):
            kwargs = {}
            if expr.get("target_node") is None:
                kwargs["target_node"] = state["group_uuid"]
            expr = new(expr, **kwargs)
        return expr

    def _iterate(self, state=None):
        return iter(self.pattern)

    def _setup_state(self):
        return {"group_uuid": uuid.uuid4()}

    def _setup_peripherals(self, initial_expr, state):
        import supriya.patterns

        start_group_event = supriya.patterns.GroupEvent(
            add_action="ADD_TO_HEAD", uuid=state["group_uuid"]
        )
        stop_group_event = supriya.patterns.GroupEvent(
            uuid=state["group_uuid"], is_stop=True
        )
        peripheral_starts = [start_group_event]
        peripheral_stops = []
        delta = self._release_time or 0
        if delta:
            peripheral_stops.append(supriya.patterns.NullEvent(delta=delta))
        peripheral_stops.append(stop_group_event)
        return peripheral_starts, peripheral_stops

    ### PUBLIC PROPERTIES ###

    @property
    def arity(self):
        return self._pattern.arity

    @property
    def is_infinite(self):
        return self._pattern.is_infinite

    @property
    def pattern(self):
        return self._pattern

    @property
    def release_time(self):
        return self._release_time
