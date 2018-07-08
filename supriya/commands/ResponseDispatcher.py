from supriya.system.Dispatcher import Dispatcher


class ResponseDispatcher(Dispatcher):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PRIVATE METHODS ###

    def _coerce_input(self, expr):
        import supriya.commands
        if not isinstance(expr, supriya.commands.Response):
            response = self._handle_message(expr)
        if not isinstance(response, tuple):
            response = (response,)
        return response

    def _handle_message(self, osc_message):
        import supriya.commands
        response_handlers = {
            '/b_info': supriya.commands.BufferInfoResponse,
            '/b_set': supriya.commands.BufferSetResponse,
            '/b_setn': supriya.commands.BufferSetContiguousResponse,
            '/c_set': supriya.commands.ControlBusSetResponse,
            '/c_setn': supriya.commands.ControlBusSetContiguousResponse,
            '/d_removed': supriya.commands.SynthDefRemovedResponse,
            '/done': supriya.commands.DoneResponse,
            '/fail': supriya.commands.FailResponse,
            '/g_queryTree.reply': supriya.commands.QueryTreeResponse,
            '/n_end': supriya.commands.NodeInfoResponse,
            '/n_go': supriya.commands.NodeInfoResponse,
            '/n_info': supriya.commands.NodeInfoResponse,
            '/n_move': supriya.commands.NodeInfoResponse,
            '/n_off': supriya.commands.NodeInfoResponse,
            '/n_on': supriya.commands.NodeInfoResponse,
            '/n_set': supriya.commands.NodeSetResponse,
            '/n_setn': supriya.commands.NodeSetContiguousResponse,
            '/status.reply': supriya.commands.StatusResponse,
            '/synced': supriya.commands.SyncedResponse,
            '/tr': supriya.commands.TriggerResponse,
            }
        class_ = response_handlers.get(osc_message.address)
        if class_:
            return class_.from_osc_message(osc_message)

    ### PUBLIC PROPERTIES ###

    @property
    def callback_class(self):
        import supriya.commands
        prototype = (
            supriya.commands.RequestCallback,
            supriya.commands.ResponseCallback,
            )
        return prototype
