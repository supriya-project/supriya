# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class Control(MultiOutUGen):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_channel_count',
        '_control_names',
        )

    ### INITIALIZER ###

    def __init__(self, control_names):
        from supriya.tools import synthdeftools
        self._control_names = tuple(sorted(control_names))
        MultiOutUGen.__init__(
            self,
            rate=synthdeftools.Rate.CONTROL,
            channel_count=len(control_names),
            )

    ### SPECIAL METHODS ###

    def __getitem__(self, i):
        from supriya import synthdeftools
        if type(i) == int:
            if len(self.control_names) == 1:
                return self
            else:
                return synthdeftools.OutputProxy(self, i)
        else:
            return self[self._get_control_index(i)]

    def __len__(self):
        return len(self.control_names)

    ### PRIVATE METHODS ###

    def _get_control_index(self, control_name):
        return self._control_names.index(control_name)

    def _get_outputs(self):
        return [self.rate] * len(self)

    ### PUBLIC PROPERTIES ###

    @property
    def control_names(self):
        return self._control_names

    @property
    def controls(self):
        from supriya import synthdeftools
        if len(self.control_names) == 1:
            result = self
        else:
            result = [
                synthdeftools.OutputProxy(self, i)
                for i in range(len(self.control_names))
                ]
        return result
