from supriya.library.audiolib.MultiOutUGen import MultiOutUGen


class Control(MultiOutUGen):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_channel_count',
        '_control_names',
        )

    ### INITIALIZER ###

    def __init__(self, control_names):
        self._control_names = tuple(sorted(control_names))
        MultiOutUGen.__init__(
            self,
            calculation_rate=self.Rate.CONTROL_RATE,
            channel_count=len(control_names),
            )

    ### SPECIAL METHODS ###

    def __getitem__(self, i):
        from supriya import audiolib
        if type(i) == int:
            if len(self.control_names) == 1:
                return self
            else:
                return audiolib.OutputProxy(self, i)
        else:
            return self[self._get_control_index(i)]

    def __len__(self):
        return len(self.control_names)

    ### PRIVATE METHODS ###

    def _get_control_index(self, control_name):
        return self._control_names.index(control_name)

    def _get_outputs(self):
        return [self.calculation_rate] * len(self)

    ### PUBLIC PROPERTIES ###

    @property
    def control_names(self):
        return self._control_names

    @property
    def controls(self):
        from supriya import audiolib
        if len(self.control_names) == 1:
            result = self
        else:
            result = [
                audiolib.OutputProxy(self, i)
                for i in range(len(self.control_names))
                ]
        return result
