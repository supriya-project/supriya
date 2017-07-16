from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class Response(SupriyaValueObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_osc_message',
        )

    _address = None

    ### INITIALIZER ###

    def __init__(
        self,
        osc_message=None,
        ):
        self._osc_message = osc_message

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.FormatSpecification(
            client=self,
            repr_is_indented=True,
            )

    ### PUBLIC METHODS ###

    def to_dict(self):
        result = {}
        for key, value in self.__getstate__().items():
            key = key[1:]
            if key == 'osc_message':
                continue
            result[key] = value
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def osc_message(self):
        return self._osc_message
