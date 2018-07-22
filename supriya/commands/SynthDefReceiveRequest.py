from supriya.commands.Request import Request
from supriya.commands.RequestBundle import RequestBundle
from supriya.commands.RequestId import RequestId


class SynthDefReceiveRequest(Request):
    """
    A /d_recv request.

    ::

        >>> import supriya
        >>> server = supriya.Server().boot()


    ::

        >>> with supriya.SynthDefBuilder(out=0, value=0.5) as builder:
        ...     _ = supriya.ugens.Out.ar(
        ...         bus=builder['out'],
        ...         source=supriya.ugens.DC.ar(builder['value']),
        ...         )
        ...
        >>> synthdef = builder.build(name='example')

    ::

        >>> synthdef in server
        False

    ::

        >>> print(server.query_remote_nodes())
        NODE TREE 0 group
            1 group

    Allocate a synthdef, then allocate a new group and allocate a synth in that
    group using the newly allocated synthdef:

    ::

        >>> request = supriya.commands.SynthDefReceiveRequest(
        ...     synthdefs=[synthdef],
        ...     callback=supriya.commands.RequestBundle(
        ...         contents=[
        ...             supriya.commands.GroupNewRequest(
        ...                 items=[
        ...                     supriya.commands.GroupNewRequest.Item(
        ...                         node_id=1000,
        ...                         target_node_id=1,
        ...                         ),
        ...                     ],
        ...                 ),
        ...             supriya.commands.SynthNewRequest(
        ...                 node_id=1001,
        ...                 synthdef=synthdef,
        ...                 target_node_id=1000,
        ...                 ),
        ...             ],
        ...         ),
        ...     )

    ::

        >>> with server.osc_io.capture() as transcript:
        ...     response = request.communicate(server=server)
        ...     _ = server.sync()
        ...
        >>> response
        DoneResponse(
            action=('/d_recv',),
            )

    ::

        >>> for entry in transcript:
        ...     entry
        ...
        ('S', OscMessage(5, bytearray(b'SCgf...example...'), OscBundle(
            contents=(
                OscMessage(21, 1000, 0, 1),
                OscMessage(9, 'example', 1001, 0, 1000),
                ),
            )))
        ('R', OscMessage('/n_go', 1000, 1, -1, -1, 1, -1, -1))
        ('R', OscMessage('/n_go', 1001, 1000, -1, -1, 0))
        ('R', OscMessage('/done', '/d_recv'))
        ('S', OscMessage(52, 0))
        ('R', OscMessage('/synced', 0))

    ::

        >>> print(server.query_remote_nodes(True))
        NODE TREE 0 group
            1 group
                1000 group
                    1001 example
                        out: 0.0, value: 0.5

    ::

        >>> print(server.query_local_nodes(True))
        NODE TREE 0 group
            1 group
                1000 group
                    1001 example
                        out: 0.0, value: 0.5

    ::

        >>> synthdef in server
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_callback',
        '_synthdefs',
        '_use_anonymous_names',
        )

    request_id = RequestId.SYNTHDEF_RECEIVE

    ### INITIALIZER ###

    def __init__(
        self,
        callback=None,
        synthdefs=None,
        use_anonymous_names=None,
    ):
        import supriya.synthdefs
        Request.__init__(self)
        if callback is not None:
            assert isinstance(callback, (Request, RequestBundle))
        self._callback = callback
        if synthdefs:
            prototype = supriya.synthdefs.SynthDef
            if isinstance(synthdefs, prototype):
                synthdefs = (synthdefs,)
            assert all(isinstance(x, prototype) for x in synthdefs)
            synthdefs = tuple(synthdefs)
        self._synthdefs = synthdefs
        if use_anonymous_names is not None:
            use_anonymous_names = bool(use_anonymous_names)
        self._use_anonymous_names = use_anonymous_names

    ### PRIVATE METHODS ###

    def _apply_local(self, server):
        for synthdef in self.synthdefs:
            synthdef._register_with_local_server(server)

    ### PUBLIC METHODS ###

    def to_osc(self, with_request_name=False):
        import supriya.synthdefs
        if with_request_name:
            request_id = self.request_name
        else:
            request_id = int(self.request_id)
        compiled_synthdefs = supriya.synthdefs.SynthDefCompiler.compile_synthdefs(
            self.synthdefs,
            use_anonymous_names=self.use_anonymous_names,
            )
        compiled_synthdefs = bytearray(compiled_synthdefs)
        contents = [
            request_id,
            compiled_synthdefs,
            ]
        if self.callback:
            contents.append(self.callback.to_osc())
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def callback(self):
        return self._callback

    @property
    def response_patterns(self):
        return [['/done', '/d_recv']]

    @property
    def synthdefs(self):
        return self._synthdefs

    @property
    def use_anonymous_names(self):
        return self._use_anonymous_names
