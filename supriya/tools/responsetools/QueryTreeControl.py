# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class QueryTreeControl(SupriyaValueObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_control_value',
        '_control_name_or_index',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        control_name_or_index=None,
        control_value=None,
        ):
        self._control_value = control_value
        self._control_name_or_index = control_name_or_index

    ### SPECIAL METHODS ###

    def __str__(self):
        key = self._control_name_or_index
        value = self._control_value
        try:
            value = round(value, 6)
        except:
            pass
        string = '{}: {}'.format(key, value)
        return string

    ### PUBLIC METHODS ###

    @classmethod
    def from_control(cls, control):
        from supriya.tools import servertools
        control_name = control.name
        if isinstance(control.value, servertools.Bus):
            control_value = str(control.value)
        else:
            control_value = float(control.value)
        return cls(
            control_value=control_value,
            control_name_or_index=control_name,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def control_name_or_index(self):
        return self._control_name_or_index

    @property
    def control_value(self):
        return self._control_value
