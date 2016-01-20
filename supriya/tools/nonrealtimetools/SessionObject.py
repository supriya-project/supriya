# -*- encoding: utf-8 -*-
import abc
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class SessionObject(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(
        self,
        session,
        ):
        from supriya.tools import nonrealtimetools
        prototype = (
            nonrealtimetools.NRTSession,
            type(None),
            )
        assert isinstance(session, prototype)
        self._session = session

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        from supriya.tools import nonrealtimetools
        manager = systemtools.StorageFormatManager
        positional_argument_values = list(
            manager.get_positional_argument_values(self))
        for value in positional_argument_values[:]:
            if isinstance(value, nonrealtimetools.Session):
                positional_argument_values.remove(value)
        return systemtools.StorageFormatSpecification(
            self,
            is_bracketed=True,
            positional_argument_values=positional_argument_values,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def session(self):
        return self._session
