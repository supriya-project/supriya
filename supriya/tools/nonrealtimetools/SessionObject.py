# -*- encoding: utf-8 -*-
import abc
import functools
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class SessionObject(SupriyaObject):
    """
    A non-realtime session object, analogous to ServerObjectProxy.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Session Internals'

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(
        self,
        session,
        ):
        from supriya.tools import nonrealtimetools
        prototype = (
            nonrealtimetools.Session,
            type(None),
            )
        assert isinstance(session, prototype)
        self._session = session

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        from abjad.tools import systemtools
        from supriya.tools import nonrealtimetools
        agent = systemtools.StorageFormatAgent(self)
        names = agent.signature_positional_names
        values = (agent._get(_) for _ in names)
        values = [
            _ for _ in values
            if not isinstance(_, nonrealtimetools.Session)
            ]
        return systemtools.FormatSpecification(
            client=self,
            storage_format_args_values=values,
            )

    ### PUBLIC METHODS ###

    @staticmethod
    def require_offset(function):
        @functools.wraps(function)
        def wrapper(self, *args, **kwargs):
            from supriya.tools import nonrealtimetools
            if isinstance(self, nonrealtimetools.Session):
                session = self
            else:
                session = self.session
            if 'offset' not in kwargs or kwargs['offset'] is None:
                if not session._active_moments:
                    raise ValueError('No active moment.')
                offset = session._active_moments[-1].offset
                kwargs['offset'] = offset
            if isinstance(self, SessionObject):
                if not (self.start_offset <= kwargs['offset'] <= self.stop_offset):
                    raise ValueError('Offset {} must intersect [{}, {}]'.format(
                        float(offset), self.start_offset, self.stop_offset))
            with session.at(kwargs['offset']):
                return function(self, *args, **kwargs)
        return wrapper

    ### PUBLIC PROPERTIES ###

    @property
    def session(self):
        return self._session
