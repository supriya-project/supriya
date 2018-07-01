import uqbar.objects
from supriya.system.SupriyaObject import SupriyaObject


class SupriyaValueObject(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        return uqbar.objects.new(self)

    def __eq__(self, expr):
        self_values = type(self), uqbar.objects.get_vars(self)
        try:
            expr_values = type(expr), uqbar.objects.get_vars(expr)
        except AttributeError:
            expr_values = type(expr), expr
        return self_values == expr_values

    def __hash__(self):
        args, var_args, kwargs = uqbar.objects.get_vars(self)
        hash_values = [type(self)]
        hash_values.append(tuple(args.items()))
        hash_values.append(tuple(var_args))
        hash_values.append(tuple(sorted(kwargs.items())))
        return hash(tuple(hash_values))
