from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class EventPlayer(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_cumulative_time',
        '_event_template',
        '_iterator',
        '_pattern',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pattern,
        event_template=None,
        ):
        import supriya.patterns
        assert isinstance(pattern, supriya.patterns.Pattern)
        self._pattern = pattern
        if event_template is None:
            event_template = supriya.patterns.NoteEvent()
        elif issubclass(event_template, supriya.patterns.Event):
            event_template = event_template()
        assert isinstance(event_template, supriya.patterns.Event)
        self._event_template = event_template
        self._cumulative_time = 0
        self._iterator = None

    ### PUBLIC PROPERTIES ###

    @property
    def event_template(self):
        return self._event_template

    @property
    def pattern(self):
        return self._pattern
