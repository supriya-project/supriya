from supriya import utils
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class SupriyaValueObject(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        return utils.new(self)

    def __eq__(self, expr):
        self_values = type(self), utils.get_object_vars(self)
        expr_values = type(expr), utils.get_object_vars(expr)
        return self_values == expr_values

    def __hash__(self):
        args, var_args, kwargs = utils.get_object_vars(self)
        hash_values = [type(self)]
        hash_values.append(tuple(args.items()))
        hash_values.append(tuple(var_args))
        hash_values.append(tuple(sorted(kwargs.items())))
        return hash(tuple(hash_values))

    def __repr__(self):
        import supriya.utils
        return supriya.utils.get_object_repr(self, multiline=True)
