# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class GroupControl(SupriyaObject):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Server Internals'

    __slots__ = (
        '_binding_sources',
        '_client',
        '_name',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        client=None,
        name=None,
        ):
        self._binding_sources = set()
        self._client = client
        self._name = str(name)

    ### SPECIAL METHODS ###

    def __str__(self):
        return self.name

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=(
                'name',
                ),
            )

    ### PUBLIC METHODS ###

    def set(self, expr):
        from supriya.tools import requesttools
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        if isinstance(expr, servertools.Bus):
            if expr.calculation_rate == synthdeftools.CalculationRate.CONTROL:
                request = requesttools.NodeMapToControlBusRequest(
                    self.node,
                    **{self.name: expr}
                    )
            else:
                request = requesttools.NodeMapToAudioBusRequest(
                    self.node,
                    **{self.name: expr}
                    )
        else:
            expr = float(expr)
            request = requesttools.NodeSetRequest(
                self.node,
                **{self.name: expr}
                )
        if self.node.is_allocated:
            request.communicate(server=self.node.server)

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        return self._client

    @property
    def group(self):
        return self.client.client

    @property
    def name(self):
        return self._name

    @property
    def node(self):
        return self.client.client