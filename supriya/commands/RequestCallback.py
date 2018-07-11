from supriya.system.SupriyaObject import SupriyaObject


class RequestCallback(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_is_one_shot',
        '_request',
        '_response_specification',
        )

    def __init__(
        self,
        is_one_shot=False,
        request=None,
        response_specification=None,
    ):
        self._is_one_shot = bool(is_one_shot)
        self._request = request
        self._response_specification = response_specification

    ### SPECIAL METHODS ###

    def __call__(self, response):
        self.request._set_response(response)

    ### PUBLIC METHODS ###

    def matches(self, expr):
        specification = self.response_specification.get(type(expr), None)
        if specification is not None:
            for key, value in specification.items():
                if getattr(expr, key) != value:
                    return False
        return True

    ### PUBLIC PROPERTIES ###

    @property
    def is_one_shot(self):
        return self._is_one_shot

    @property
    def prototype(self):
        return tuple(self.response_specification.keys())

    @property
    def request(self):
        return self._request

    @property
    def response_specification(self):
        return self._response_specification
