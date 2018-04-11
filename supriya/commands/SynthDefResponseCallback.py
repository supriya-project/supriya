from supriya.commands.ResponseCallback import ResponseCallback


class SynthDefResponseCallback(ResponseCallback):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_server',
        )

    ### INITIALIZER ###

    def __init__(self, server):
        import supriya.commands
        import supriya.realtime
        ResponseCallback.__init__(
            self,
            #address_pattern='/d_removed',
            procedure=self.__call__,
            prototype=(
                supriya.commands.SynthDefRemovedResponse,
                ),
            )
        assert isinstance(server, supriya.realtime.Server)
        self._server = server

    ### SPECIAL METHODS ###

    def __call__(self, response):
        synthdef_name = response.synthdef_name
        synthdef = self._server._synthdefs.get(synthdef_name)
        if synthdef is None:
            return
        synthdef._handle_response(response)

    ### PUBLIC PROPERTIES ###

    @property
    def server(self):
        return self._server
