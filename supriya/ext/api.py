import enum
import inspect
from typing import List, Tuple, cast

from uqbar.apis import ModuleDocumenter, SummarizingClassDocumenter


class SupriyaClassDocumenter(SummarizingClassDocumenter):

    ignored_special_methods: Tuple[str, ...] = (
        "__delattr__",
        "__dict__",
        "__eq__",
        "__getattribute__",
        "__getnewargs__",
        "__getstate__",
        "__hash__",
        "__init__",
        "__new__",
        "__postinit__",
        "__reduce__",
        "__reduce_ex__",
        "__repr__",
        "__setattr__",
        "__setstate__",
        "__sizeof__",
        "__str__",
        "__subclasshook__",
        "fromkeys",
        "pipe_cloexec",
    )

    def __str__(self) -> str:
        name = getattr(self.client, "__name__")
        if issubclass(self.client, Exception):  # type: ignore
            return ".. autoexception:: {}".format(name)
        result = [".. autoclass:: {}".format(name), "   :show-inheritance:"]
        if issubclass(self.client, enum.Enum):  # type: ignore
            result.extend(["   :members:", "   :undoc-members:"])
        result.append("")
        for attr in sorted(
            inspect.classify_class_attrs(cast(type, self.client)), key=lambda x: x.name
        ):
            if attr.defining_class is not self.client:
                continue
            if attr.name.startswith("_") and not attr.name.startswith("__"):
                continue
            if attr.name.startswith("__") and attr.name in self.ignored_special_methods:
                continue
            if attr.kind in ("method", "class method", "static method"):
                result.append(f"   .. automethod:: {attr.name}")
            elif attr.kind in ("property"):
                result.append(f"   .. autoproperty:: {attr.name}")
        return "\n".join(result)


class SupriyaModuleDocumenter(ModuleDocumenter):
    def _build_toc(self, documenters, **kwargs) -> List[str]:
        result: List[str] = []
        if not documenters:
            return result
        result.extend(["", ".. toctree::", "   :hidden:"])
        result.append("")
        module_documenters = [_ for _ in documenters if isinstance(_, type(self))]
        for module_documenter in module_documenters:
            path = self._build_toc_path(module_documenter)
            if path:
                result.append("   {}".format(path))
        return result
