from .Receive import Receive


class TrackReceive(Receive):

    ### PUBLIC PROPERTIES ###

    @property
    def preceding_bus_group(self):
        return self.parent.input_bus_group

    @property
    def succeeding_bus_group(self):
        return self.parent.bus_group
