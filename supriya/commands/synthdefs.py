import pathlib
from typing import TYPE_CHECKING, Union

import supriya.osc
from supriya.enums import RequestId

from .bases import Request, RequestBundle, Response

if TYPE_CHECKING:
    from supriya.synthdefs import SynthDef


class SynthDefFreeAllRequest(Request):
    ### CLASS VARIABLES ###

    request_id = RequestId.SYNTHDEF_FREE_ALL

    ### INITIALIZER ###

    def __init__(self):
        Request.__init__(self)

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        return supriya.osc.OscMessage("/d_freeAll")


class SynthDefFreeRequest(Request):
    """
    A /d_free request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.SynthDefFreeRequest("test")
        >>> request
        SynthDefFreeRequest(
            'test',
        )

    ::

        >>> request.to_osc()
        OscMessage('/d_free', 'test')

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.SYNTHDEF_FREE

    ### INITIALIZER ###

    def __init__(self, *synthdefs: Union["SynthDef", str]):
        Request.__init__(self)
        self._synthdefs = synthdefs

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        from ..synthdefs import SynthDef

        return supriya.osc.OscMessage(
            self.request_name,
            *(
                synthdef.actual_name
                if isinstance(synthdef, SynthDef)
                else str(synthdef)
                for synthdef in self.synthdefs
            ),
        )

    ### PUBLIC PROPERTIES ###

    @property
    def synthdefs(self):
        return self._synthdefs


class SynthDefLoadDirectoryRequest(Request):
    """
    A /d_loadDir request.
    """

    ### CLASS VARIABLES ###

    request_id = RequestId.SYNTHDEF_LOAD_DIR

    ### INITIALIZER ###

    def __init__(self, callback=None, path=None):
        Request.__init__(self)
        if callback is not None:
            assert isinstance(callback, (Request, RequestBundle))
        self._callback = callback
        self._path = pathlib.Path(path).absolute()

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        contents = [request_id, str(self.path)]
        if self.callback:
            contents.append(self.callback.to_osc(with_placeholders=with_placeholders))
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def callback(self):
        return self._callback

    @property
    def response_patterns(self):
        return ["/done", "/d_loadDir"], None

    @property
    def path(self):
        return self._path


class SynthDefLoadRequest(Request):
    """
    A /d_load request.
    """

    ### CLASS VARIABLES ###

    request_id = RequestId.SYNTHDEF_LOAD

    ### INITIALIZER ###

    def __init__(self, callback=None, path=None):
        Request.__init__(self)
        if callback is not None:
            assert isinstance(callback, (Request, RequestBundle))
        self._callback = callback
        self._path = pathlib.Path(path).absolute()

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        contents = [request_id, str(self.path)]
        if self.callback:
            contents.append(self.callback.to_osc(with_placeholders=with_placeholders))
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def callback(self):
        return self._callback

    @property
    def response_patterns(self):
        return ["/done", "/d_load"], None

    @property
    def path(self):
        return self._path


class SynthDefReceiveRequest(Request):
    """
    A /d_recv request.

    ::

        >>> server = supriya.Server().boot()


    ::

        >>> with supriya.SynthDefBuilder(out=0, value=0.5) as builder:
        ...     _ = supriya.ugens.Out.ar(
        ...         bus=builder["out"],
        ...         source=supriya.ugens.DC.ar(source=builder["value"]),
        ...     )
        ...
        >>> synthdef = builder.build(name="example")

    ::

        >>> synthdef in server
        False

    ::

        >>> print(server.query())
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
        ...                     ),
        ...                 ],
        ...             ),
        ...             supriya.commands.SynthNewRequest(
        ...                 node_id=1001,
        ...                 synthdef=synthdef,
        ...                 target_node_id=1000,
        ...             ),
        ...         ],
        ...     ),
        ... )

    ::

        >>> with server.osc_protocol.capture() as transcript:
        ...     response = request.communicate(server=server)
        ...     _ = server.sync()
        ...
        >>> response
        DoneResponse(
            action=('/d_recv',),
        )

    ::

        >>> for entry in transcript:
        ...     (entry.label, entry.message)
        ...
        ('S', OscMessage('/d_recv', b'SCgf...example...', OscBundle(
            contents=(
                OscMessage('/g_new', 1000, 0, 1),
                OscMessage('/s_new', 'example', 1001, 0, 1000),
            ),
        )))
        ('R', OscMessage('/n_go', 1000, 1, -1, -1, 1, -1, -1))
        ('R', OscMessage('/n_go', 1001, 1000, -1, -1, 0))
        ('R', OscMessage('/done', '/d_recv'))
        ('S', OscMessage('/sync', 0))
        ('R', OscMessage('/synced', 0))

    ::

        >>> print(server.query())
        NODE TREE 0 group
            1 group
                1000 group
                    1001 example
                        out: 0.0, value: 0.5

    ::

        >>> print(server.root_node)
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

    request_id = RequestId.SYNTHDEF_RECEIVE

    ### INITIALIZER ###

    def __init__(self, callback=None, synthdefs=None, use_anonymous_names=None):
        from ..synthdefs import SynthDef

        Request.__init__(self)
        if callback is not None:
            assert isinstance(callback, (Request, RequestBundle))
        self._callback = callback
        if synthdefs:
            prototype = SynthDef
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

    def to_osc(self, *, with_placeholders=False):
        from ..synthdefs import SynthDefCompiler

        request_id = self.request_name
        compiled_synthdefs = SynthDefCompiler.compile_synthdefs(
            self.synthdefs, use_anonymous_names=self.use_anonymous_names
        )
        contents = [request_id, compiled_synthdefs]
        if self.callback:
            contents.append(self.callback.to_osc(with_placeholders=with_placeholders))
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def callback(self):
        return self._callback

    @property
    def response_patterns(self):
        return ["/done", "/d_recv"], None

    @property
    def synthdefs(self):
        return self._synthdefs

    @property
    def use_anonymous_names(self):
        return self._use_anonymous_names


class SynthDefRemovedResponse(Response):
    ### INITIALIZER ###

    def __init__(self, synthdef_name=None):
        Response.__init__(self)
        self._synthdef_name = synthdef_name

    ### PUBLIC METHODS ###

    @classmethod
    def from_osc_message(cls, osc_message):
        synthdef_name = osc_message.contents[0]
        response = cls(synthdef_name=synthdef_name)
        return response

    ### PUBLIC PROPERTIES ###

    @property
    def synthdef_name(self):
        return self._synthdef_name
