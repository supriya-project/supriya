# -*- encoding: utf-8 -*-
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
        from supriya.tools import patterntools
        assert isinstance(pattern, patterntools.Pattern)
        self._pattern = pattern
        if event_template is None:
            event_template = patterntools.NoteEvent()
        elif issubclass(event_template, patterntools.Event):
            event_template = event_template()
        assert isinstance(event_template, patterntools.Event)
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
