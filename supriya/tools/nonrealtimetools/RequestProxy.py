# -*- encoding: utf-8 -*-
from supriya.tools.systemtools import SupriyaValueObject


class RequestProxy(SupriyaValueObject):

    __slots__ = (
        '_request_type',
        '_request_arguments',
        '_timestep',
        )

    def __init__(
        self,
        timestep,
        request_type,
        **request_arguments
        ):
        self._timestep = timestep
        self._request_type = request_type
        self._request_arguments = tuple(sorted(request_arguments.items()))
