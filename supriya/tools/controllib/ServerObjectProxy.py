# -*- encoding: utf-8 -*-
import abc


class ServerObjectProxy(object):
    r'''A proxy of an object on a server.

    Server objects can be allocated and freed.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    __slots__ = (
        '_server_session',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        self._server_session = None

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def allocate(self, server_session=None):
        from supriya import controllib
        assert self.server_session is None
        if server_session is None:
            server_session = controllib.Server.get_default_session()
        assert isinstance(server_session, controllib.ServerSession)
        assert server_session.is_running
        self._server_session = server_session

    @abc.abstractmethod
    def free(self):
        self._server_session = None

    ### PUBLIC PROPERTIES ###

    @property
    def server_session(self):
        return self._server_session
