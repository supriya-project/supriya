import abc


class Slot:

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, name, track, synthdef, **kwargs):
        import supriya.live

        self._name = str(name)
        assert isinstance(track, supriya.live.Track)
        self._track = track
        self._group = supriya.realtime.Group()
        if isinstance(synthdef, supriya.synthdefs.SynthDefFactory):
            synthdef = synthdef.build(channel_count=self._track.channel_count)
        if synthdef is not None:
            assert isinstance(synthdef, supriya.synthdefs.SynthDef)
        self._synthdef = synthdef
        self._bindable_namespace = self._setup_bindable_namespace(**kwargs)

    ### SPECIAL METHODS ###

    def __getitem__(self, key):
        return self._bindable_namespace.proxies[key]

    def __setitem__(self, key, value):
        self._bindable_namespace[key] = value

    ### PRIVATE METHODS ###

    def _allocate(self):
        self._track.instrument_group.append(self.group)
        if self._synthdef is not None and not self._synthdef.is_allocated:
            self._synthdef.allocate()

    def _as_node_target(self):
        return self.group

    @abc.abstractmethod
    def _setup_bindable_namespace(self, **kwargs):
        raise NotImplementedError

    def _free(self):
        self.play(False)
        self._track.instrument_group.remove(self.group)

    ### PUBLIC PROPERTIES ###

    @property
    def bindable_namespace(self):
        return self._bindable_namespace

    @property
    def group(self):
        return self._group

    @property
    def is_allocated(self):
        return self.track.is_allocated

    @property
    def name(self):
        return self._name

    @property
    def synth(self):
        return self._synth

    @property
    def synthdef(self):
        return self._synthdef

    @property
    def synth_kwargs(self):
        return dict(
            target_node=self,
            in_=int(self.track.output_bus_group),
            out=int(self.track.output_bus_group),
        )

    @property
    def track(self):
        return self._track
