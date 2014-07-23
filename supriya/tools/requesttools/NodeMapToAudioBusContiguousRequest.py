# -*- encoding: utf-8 -*-
from supriya.tools.requesttools.Request import Request


class NodeMapToAudioBusContiguousRequest(Request):

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(
        self,
        ):
        pass

    ### PUBLIC METHODS ###

    def as_osc_message(self):
        from supriya.tools import servertools
        manager = servertools.CommandManager
        message = manager.make_node_map_to_audio_bus_contiguous_message()
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def response_prototype(self):
        return None

    @property
    def request_number(self):
        from supriya.tools import servertools
        return servertools.RequestId.NODE_MAP_TO_AUDIO_BUS_CONTIGUOUS