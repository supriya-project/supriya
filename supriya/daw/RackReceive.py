from .Receive import Receive


class RackReceive(Receive):
    @property
    def preceding_bus_group(self):
        return self.parent.bus_group

    @property
    def succeeding_bus_group(self):
        return self.parent.bus_group
