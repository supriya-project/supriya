# -*- encoding: utf-8 -*-
from supriya.tools.requesttools.Request import Request


class GroupFreeAllRequest(Request):

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(
        self,
        ):
        pass

    ### PUBLIC METHODS ###

    def to_osc_message(self):
        from supriya.tools import requesttools
        manager = requesttools.RequestManager
        message = manager.make_group_free_all_message()
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def response_prototype(self):
        return None

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.GROUP_FREE_ALL