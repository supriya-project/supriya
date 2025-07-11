from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .components import Component


class BusParameter:
    def __init__(self, component: "Component", name: str) -> None:
        self._component = component
        self._name = name

    def set(self, value: float) -> None:
        self._component._artifacts.control_buses[self._name].set(
            value, use_shared_memory=True
        )
