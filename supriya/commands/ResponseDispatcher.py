from supriya.system.Dispatcher import Dispatcher


class ResponseDispatcher(Dispatcher):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PRIVATE METHODS ###

    def _coerce_input(self, expr):
        import supriya.commands
        if not isinstance(expr, supriya.commands.Response):
            response = supriya.commands.ResponseManager.handle_message(expr)
        if not isinstance(response, tuple):
            response = (response,)
        return response

    ### PUBLIC PROPERTIES ###

    @property
    def callback_class(self):
        import supriya.commands
        import supriya.commands
        prototype = (
            supriya.commands.RequestCallback,
            supriya.commands.ResponseCallback,
            )
        return prototype
