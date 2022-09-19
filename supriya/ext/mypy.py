from typing import Callable, Optional
from typing import Type as TypingType

from mypy.nodes import ARG_OPT, Argument, AssignmentStmt, CallExpr, RefExpr, Var
from mypy.plugin import ClassDefContext, Plugin
from mypy.plugins.common import _get_decorator_bool_argument
from mypy.typeops import make_simplified_union
from mypy.types import NoneType


class UGenTransformer:
    def __init__(self, ctx: ClassDefContext) -> None:
        self._ctx = ctx

    def collect_params(self):
        cls = self._ctx.cls
        params = []
        for stmt in cls.defs.body:
            if not isinstance(stmt, AssignmentStmt):
                continue
            expr = stmt.rvalue
            if (
                isinstance(expr, CallExpr)
                and isinstance(expr.callee, RefExpr)
                and expr.callee.fullname in ["supriya.ugens.bases.param"]
            ):
                params.append(stmt.lvalues[0].name)
        return params

    def transform(self) -> bool:
        # is_classmethod flag is not released yet
        from mypy.plugins.common import add_attribute_to_class, add_method_to_class

        api = self._ctx.api
        cls = self._ctx.cls
        info = self._ctx.cls.info

        ugen_input_type = make_simplified_union(
            [
                api.named_type("typing.SupportsFloat"),
                api.named_type("supriya.ugens.bases.UGenMethodMixin"),
            ]
        )

        decorator_arguments = {
            "ar": _get_decorator_bool_argument(self._ctx, "ar", False),
            "kr": _get_decorator_bool_argument(self._ctx, "kr", False),
            "ir": _get_decorator_bool_argument(self._ctx, "ir", False),
            "dr": _get_decorator_bool_argument(self._ctx, "dr", False),
            "new": _get_decorator_bool_argument(self._ctx, "new", False),
            "is_multichannel": _get_decorator_bool_argument(
                self._ctx, "is_multichannel", False
            ),
            "fixed_channel_count": _get_decorator_bool_argument(
                self._ctx, "fixed_channel_count", False
            ),
        }
        args = []
        for name in self.collect_params():
            args.append(
                Argument(
                    variable=Var(name, ugen_input_type),
                    type_annotation=ugen_input_type,
                    initializer=None,
                    kind=ARG_OPT,
                )
            )
            add_attribute_to_class(
                api=api,
                cls=cls,
                name=name,
                typ=ugen_input_type,
                override_allow_incompatible=True,
            )
        if (
            decorator_arguments["is_multichannel"]
            and not decorator_arguments["fixed_channel_count"]
        ):
            args.append(
                Argument(
                    variable=Var("channel_count", api.named_type("typing.SupportsInt")),
                    type_annotation=api.named_type("typing.SupportsInt"),
                    initializer=None,
                    kind=ARG_OPT,
                )
            )
        for name in ["ar", "kr", "ir", "dr", "new"]:
            if not decorator_arguments[name] or name in info.names:
                continue
            add_method_to_class(
                api=api,
                cls=cls,
                name=name,
                args=args,
                return_type=api.named_type("supriya.ugens.bases.UGenMethodMixin"),
                is_classmethod=True,
            )
        if "__init__" not in info.names:
            add_method_to_class(
                api=api, cls=cls, name="__init__", args=args, return_type=NoneType()
            )
        return False


def _ugen_hook(ctx: ClassDefContext):
    UGenTransformer(ctx).transform()


class SupriyaPlugin(Plugin):
    def get_class_decorator_hook(
        self, fullname: str
    ) -> Optional[Callable[[ClassDefContext], None]]:
        if fullname == "supriya.ugens.bases.ugen":
            return _ugen_hook
        return None


def plugin(version: str) -> TypingType[SupriyaPlugin]:
    return SupriyaPlugin
