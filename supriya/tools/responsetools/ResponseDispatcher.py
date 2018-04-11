from supriya.tools.systemtools.Dispatcher import Dispatcher


class ResponseDispatcher(Dispatcher):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PRIVATE METHODS ###

    def _coerce_input(self, expr):
        from supriya.tools import responsetools
        if not isinstance(expr, responsetools.Response):
            response = responsetools.ResponseManager.handle_message(expr)
        if not isinstance(response, tuple):
            response = (response,)
        return response

    ### PUBLIC PROPERTIES ###

    @property
    def callback_class(self):
        import supriya.commands
        from supriya.tools import responsetools
        prototype = (
            supriya.commands.RequestCallback,
            responsetools.ResponseCallback,
            )
        return prototype
