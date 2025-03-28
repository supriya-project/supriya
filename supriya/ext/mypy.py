from typing import Callable
from typing import Type as TypingType

from mypy.nodes import ARG_OPT, Argument, AssignmentStmt, CallExpr, RefExpr, Var
from mypy.plugin import ClassDefContext, Plugin
from mypy.plugins.common import _get_bool_argument, _get_decorator_bool_argument
from mypy.types import NoneType


class UGenTransformer:
    def __init__(self, ctx: ClassDefContext) -> None:
        self._ctx = ctx

    def collect_params(self) -> list[tuple[str, bool]]:
        cls = self._ctx.cls
        params = []
        for stmt in cls.defs.body:
            if not isinstance(stmt, AssignmentStmt):
                continue
            expr = stmt.rvalue
            if (
                isinstance(expr, CallExpr)
                and isinstance(expr.callee, RefExpr)
                and expr.callee.fullname in ["supriya.ugens.core.param"]
            ):
                params.append(
                    (
                        getattr(stmt.lvalues[0], "name", ""),
                        _get_bool_argument(self._ctx, expr, "unexpanded", False),
                    )
                )
        return params

    def transform(self) -> bool:
        # is_classmethod flag is not released yet
        from mypy.plugins.common import add_attribute_to_class, add_method_to_class

        api = self._ctx.api
        cls = self._ctx.cls
        info = self._ctx.cls.info

        SupportsIntType = api.named_type("typing.SupportsInt")
        CalculationRateType = api.named_type("supriya.enums.CalculationRate")
        UGenOperableType = api.named_type("supriya.ugens.core.UGenOperable")
        UGenScalarType = api.named_type("supriya.ugens.core.UGenScalar")
        UGenVectorType = api.named_type("supriya.ugens.core.UGenVector")
        # api.named_type() breaks for these... why?
        UGenRecursiveInputTypeSym = api.lookup_fully_qualified(
            "supriya.ugens.core.UGenRecursiveInput"
        )
        UGenScalarInputTypeSym = api.lookup_fully_qualified(
            "supriya.ugens.core.UGenScalarInput"
        )
        UGenVectorInputTypeSym = api.lookup_fully_qualified(
            "supriya.ugens.core.UGenVectorInput"
        )

        UGenRecursiveInputType = getattr(UGenRecursiveInputTypeSym.node, "target")
        UGenScalarInputType = getattr(UGenScalarInputTypeSym.node, "target")
        UGenVectorInputType = getattr(UGenVectorInputTypeSym.node, "target")

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
        init_args = [
            Argument(
                variable=Var("calculation_rate", CalculationRateType),
                type_annotation=CalculationRateType,
                initializer=None,
                kind=ARG_OPT,
            ),
            Argument(
                variable=Var("special_index", SupportsIntType),
                type_annotation=SupportsIntType,
                initializer=None,
                kind=ARG_OPT,
            ),
        ]
        rate_args = []
        for name, unexpanded in self.collect_params():
            init_type = UGenVectorInputType if unexpanded else UGenScalarInputType
            init_args.append(
                Argument(
                    variable=Var(name, init_type),
                    type_annotation=init_type,
                    initializer=None,
                    kind=ARG_OPT,
                )
            )
            rate_args.append(
                Argument(
                    variable=Var(name, UGenRecursiveInputType),
                    type_annotation=UGenRecursiveInputType,
                    initializer=None,
                    kind=ARG_OPT,
                )
            )
            add_attribute_to_class(
                api=api,
                cls=cls,
                name=name,
                typ=UGenVectorType if unexpanded else UGenScalarType,
                override_allow_incompatible=True,
            )
        if (
            decorator_arguments["is_multichannel"]
            and not decorator_arguments["fixed_channel_count"]
        ):
            channel_count_arg = Argument(
                variable=Var("channel_count", SupportsIntType),
                type_annotation=SupportsIntType,
                initializer=None,
                kind=ARG_OPT,
            )
            init_args.append(channel_count_arg)
            rate_args.append(channel_count_arg)
        for name in ["ar", "kr", "ir", "dr", "new"]:
            if not decorator_arguments[name] or name in info.names:
                continue
            add_method_to_class(
                api=api,
                cls=cls,
                name=name,
                args=rate_args,
                return_type=UGenOperableType,
                is_classmethod=True,
            )
        if "__init__" not in info.names:
            add_method_to_class(
                api=api,
                cls=cls,
                name="__init__",
                args=init_args,
                return_type=NoneType(),
            )
        return True


def _ugen_hook(ctx: ClassDefContext) -> bool:
    return UGenTransformer(ctx).transform()


class SupriyaPlugin(Plugin):
    def get_class_decorator_hook_2(
        self, fullname: str
    ) -> Callable[[ClassDefContext], bool] | None:
        if fullname == "supriya.ugens.core.ugen":
            return _ugen_hook
        return None


def plugin(version: str) -> TypingType[SupriyaPlugin]:
    return SupriyaPlugin
