from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class ControlBusSetContiguousItem(SupriyaValueObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_bus_values',
        '_starting_bus_id',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        starting_bus_id=None,
        bus_values=None
        ):
        self._bus_values = bus_values
        self._starting_bus_id = starting_bus_id

    ### PUBLIC PROPERTIES ###

    @property
    def bus_values(self):
        return self._bus_values

    @property
    def starting_bus_id(self):
        return self._starting_bus_id
