from supriya.system.SupriyaObject import SupriyaObject


class ResponseCallback(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_is_one_shot',
        '_procedure',
        '_prototype',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        procedure=None,
        prototype=None,
        is_one_shot=False,
    ):
        #import supriya.commands
        assert callable(procedure)
        if prototype is not None:
            if not isinstance(prototype, tuple):
                prototype = (prototype,)
            #prototype = supriya.commands.Response
            #assert all(issubclass(x, prototype) for x in prototype)
        self._procedure = procedure
        self._prototype = prototype
        self._is_one_shot = bool(is_one_shot)

    ### SPECIAL METHODS ###

    def __call__(self, message):
        self._procedure(message)

    ### PUBLIC METHODS ###

    def matches(self, response):
        return True

    ### PUBLIC PROPERTIES ###

    @property
    def is_one_shot(self):
        return self._is_one_shot

    @property
    def procedure(self):
        return self._procedure

    @property
    def prototype(self):
        return self._prototype
