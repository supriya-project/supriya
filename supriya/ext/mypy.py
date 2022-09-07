from typing import Callable, Optional
from typing import Type as TypingType

from mypy.plugin import ClassDefContext, Plugin
from mypy.plugins.common import _get_decorator_bool_argument


class UGenTransformer:
    def __init__(self, ctx: ClassDefContext) -> None:
        self._ctx = ctx

    def transform(self) -> bool:
        decorator_arguments = {
            "ar": _get_decorator_bool_argument(self._ctx, "ar", True),
            "kr": _get_decorator_bool_argument(self._ctx, "kr", True),
            "ir": _get_decorator_bool_argument(self._ctx, "ir", False),
            "dr": _get_decorator_bool_argument(self._ctx, "dr", False),
            "new": _get_decorator_bool_argument(self._ctx, "new", False),
            "is_multichannel": _get_decorator_bool_argument(
                self._ctx, "is_multichannel", True
            ),
            "fixed_channel_count": _get_decorator_bool_argument(
                self._ctx, "fixed_channel_count", True
            ),
        }
        print(self._ctx.cls.info, decorator_arguments)
        return False


def _ugen_hook(ctx: ClassDefContext):
    UGenTransformer(ctx).transform()


class SupriyaPlugin(Plugin):
    def get_class_decorator_hook(
        self, fullname: str
    ) -> Optional[Callable[[ClassDefContext], None]]:
        if fullname == "supriya.ugens.decorators.ugen":
            return _ugen_hook
        return None


def plugin(version: str) -> TypingType[SupriyaPlugin]:
    return SupriyaPlugin
