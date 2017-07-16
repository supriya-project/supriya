from supriya.tools.systemtools import Bindable
from supriya.tools.systemtools import SupriyaObject


class BindableFloat(SupriyaObject):

    def __init__(self, value):
        self.value = float(value)

    ### SPECIAL METHODS ###

    @Bindable(rebroadcast=True)
    def __call__(self, value):
        self.value = float(value)
        return value

    def __add__(self, expr):
        return float(self) + expr

    def __div__(self, expr):
        return float(self) / expr

    def __eq__(self, expr):
        return float(self) == float(expr)

    def __float__(self):
        return self.value

    def __hash__(self):
        return id(self)

    def __lt__(self, expr):
        return float(self) < float(expr)

    def __mod__(self, expr):
        return float(self) % expr

    def __mul__(self, expr):
        return float(self) * expr

    def __radd__(self, expr):
        return expr + float(self)

    def __rdiv__(self, expr):
        return expr / float(self)

    def __rmod__(self, expr):
        return expr % float(self)

    def __rmul__(self, expr):
        return expr * float(self)

    def __rsub__(self, expr):
        return expr - float(self)

    def __sub__(self, expr):
        return float(self) - expr

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        from supriya import new
        spec = super(BindableFloat, self)._get_format_specification()
        return new(
            spec,
            repr_is_indented=False,
            storage_format_is_indented=False,
            )
