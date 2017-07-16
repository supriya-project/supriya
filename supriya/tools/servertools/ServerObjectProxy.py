import abc
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class ServerObjectProxy(SupriyaObject):
    """
    A proxy of an object on a server.

    Server objects can be allocated and freed.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_server',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        self._server = None

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def allocate(
        self,
        server=None,
        ):
        from supriya import servertools
        assert self.server is None, (self, self.server)
        server = server or servertools.Server.get_default_server()
        assert isinstance(server, servertools.Server)
        assert server.is_running
        self._server = server

    @abc.abstractmethod
    def free(self):
        self._server = None

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def is_allocated(self):
        raise NotImplementedError

    @property
    def server(self):
        return self._server
