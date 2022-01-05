import abc
import functools

from uqbar.objects import get_repr

from supriya.system import SupriyaObject


class SessionObject(SupriyaObject):
    """
    A non-realtime session object, analogous to ServerObject.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, session):
        import supriya.nonrealtime

        prototype = (supriya.nonrealtime.Session, type(None))
        assert isinstance(session, prototype)
        self._session = session

    ### SPECIAL METHODS ###

    def __repr__(self):
        return get_repr(self, multiline=False)

    ### PUBLIC METHODS ###

    @staticmethod
    def require_offset(function):
        @functools.wraps(function)
        def wrapper(self, *args, **kwargs):
            import supriya.nonrealtime

            if isinstance(self, supriya.nonrealtime.Session):
                session = self
            else:
                session = self.session
            if "offset" not in kwargs or kwargs["offset"] is None:
                if not session._active_moments:
                    raise ValueError("No active moment.")
                offset = session._active_moments[-1].offset
                kwargs["offset"] = offset
            if isinstance(self, SessionObject):
                if not (self.start_offset <= kwargs["offset"] <= self.stop_offset):
                    raise ValueError(
                        "Offset {} must intersect [{}, {}]".format(
                            float(offset), self.start_offset, self.stop_offset
                        )
                    )
            with session.at(kwargs["offset"]):
                return function(self, *args, **kwargs)

        return wrapper

    ### PUBLIC PROPERTIES ###

    @property
    def session(self):
        return self._session
