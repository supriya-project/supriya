import dataclasses
from typing import TYPE_CHECKING, SupportsFloat

from .specs import SpecFactory

if TYPE_CHECKING:
    from .components import Component


@dataclasses.dataclass
class Field:
    default: SupportsFloat

    def __call__(self, value: SupportsFloat) -> float:
        raise NotImplementedError


@dataclasses.dataclass
class IntField(Field):
    default: int = 0
    minimum: int | None = None
    maximum: int | None = None

    def __call__(self, value: SupportsFloat) -> float:
        value_ = int(float(value))
        if self.minimum is not None and value_ < self.minimum:
            value_ = self.minimum
        if self.maximum is not None and value_ > self.maximum:
            value_ = self.maximum
        return float(value)


@dataclasses.dataclass
class FloatField(Field):
    default: float = 0.0
    minimum: float | None = None
    maximum: float | None = None

    def __call__(self, value: SupportsFloat) -> float:
        value_ = float(value)
        if self.minimum is not None and value_ < self.minimum:
            value_ = self.minimum
        if self.maximum is not None and value_ > self.maximum:
            value_ = self.maximum
        return value_


@dataclasses.dataclass
class BoolField(Field):
    default: bool = False

    def __call__(self, value: SupportsFloat) -> float:
        return float(bool(float(value)))


class Parameter:
    def __init__(
        self,
        *,
        component: "Component",
        field: Field,
        has_bus: bool,
        name: str,
    ) -> None:
        self._component = component
        self._name = name
        self._has_bus = has_bus
        self._field = field
        self._value: float = self._field(self._field.default)

    def _resolve_specs(self, spec_factory: SpecFactory) -> SpecFactory:
        if not self._has_bus:
            return spec_factory
        spec_factory.add_control_bus(
            channel_count=1,
            default=self._value,
            name=self.name,
        )
        return spec_factory

    def set(self, value: float) -> None:
        value_ = self._field(value)
        if self._name in self._component._local_artifacts.control_buses:
            self._component._local_artifacts.control_buses[self._name].set(
                value_, use_shared_memory=True
            )
        else:
            self._value = value_

    @property
    def component(self) -> "Component":
        return self._component

    @property
    def field(self) -> Field:
        return self._field

    @property
    def has_bus(self) -> bool:
        return self._has_bus

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> float:
        return self._value
