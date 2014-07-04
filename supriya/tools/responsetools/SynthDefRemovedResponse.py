# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class SynthDefRemovedResponse(SupriyaValueObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_synthdef_name',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        synthdef_name=None,
        ):
        self._synthdef_name = synthdef_name

    ### PUBLIC PROPERTIES ###

    @property
    def synthdef_name(self):
        return self._synthdef_name
