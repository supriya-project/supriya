# -*- encoding: utf-8 -*-
import abc


class ServerObjectProxy(object):
    r'''A proxy of an object on a server.

    Server objects can be allocated and freed.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    __slots__ = (
        '_session',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        self._session = None

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def allocate(self, session=None):
        from supriya import servertools
        assert self.session is None
        if session is None:
            session = servertools.Server.get_default_session()
        assert isinstance(session, servertools.Session)
        assert session.is_running
        self._session = session

    @abc.abstractmethod
    def free(self):
        self._session = None

    ### PUBLIC PROPERTIES ###

    @property
    def session(self):
        return self._session
