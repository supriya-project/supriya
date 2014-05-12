from supriya.library.audio.UGen import UGen


class Control(UGen):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_control_names',
        )

    ### INITIALIZER ###

    def __init__(self, control_names):
        UGen.__init__(self, UGen.Rate.CONTROL_RATE)
        self._control_names = tuple(sorted(control_names))

    ### SPECIAL METHODS ###

    def __getitem__(self, i):
        from supriya import audio
        if type(i) == int:
            if len(self.control_names) == 1:
                return self
            else:
                return audio.OutputProxy(self, i)
        else:
            return self[self._get_control_index(i)]

    def __len__(self):
        return len(self.controlnames)

    ### PRIVATE METHODS ###

    def _get_control_index(self, controlname):
        return self._control_names.index(controlname)

    def _get_outputs(self):
        return [self.calculation_rate] * len(self.control_names)

    ### PUBLIC PROPERTIES ###

    @property
    def control_names(self):
        return self._control_names

    @property
    def controls(self):
        from supriya import audio
        if len(self.control_names) == 1:
            result = self
        else:
            result = [
                audio.OutputProxy(self, i)
                for i in range(len(self.control_names))
                ]
        return result

    @property
    def outputs(self):
        return [self.calculation_rate for _ in self.control_names]
