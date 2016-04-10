# -*- encoding: utf-8 -*-
from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class SynthNewRequest(Request):
    r'''A /s_new request.

    ::

        >>> from supriya.tools import requesttools
        >>> from supriya.tools import servertools
        >>> request = requesttools.SynthNewRequest(
        ...     add_action=servertools.AddAction.ADD_TO_TAIL,
        ...     node_id=1001,
        ...     synthdef='test',
        ...     target_node_id=1000,
        ...     frequency=443,
        ...     phase=0.2
        ...     )
        >>> request
        SynthNewRequest(
            add_action=AddAction.ADD_TO_TAIL,
            node_id=1001,
            synthdef='test',
            target_node_id=1000,
            frequency=443,
            phase=0.2
            )

    ::

        >>> message = request.to_osc_message()
        >>> message
        OscMessage(9, 'test', 1001, 1, 1000, 'frequency', 443, 'phase', 0.2)

    ::

        >>> message.address == requesttools.RequestId.SYNTH_NEW
        True

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_add_action',
        '_node_id',
        '_synthdef',
        '_target_node_id',
        '_kwargs',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        add_action=None,
        node_id=None,
        synthdef=None,
        target_node_id=None,
        **kwargs
        ):
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        Request.__init__(self)
        self._add_action = servertools.AddAction.from_expr(add_action)
        self._node_id = node_id
        prototype = (str, synthdeftools.SynthDef)
        assert isinstance(synthdef, prototype)
        self._synthdef = synthdef
        self._target_node_id = target_node_id
        self._kwargs = kwargs

    ### SPECIAL METHODS ###

    def __getattr__(self, name):
        if name in self._kwargs:
            return self._kwargs[name]
        return object.__getattr__(self, name)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        from abjad.tools import systemtools
        agent = systemtools.StorageFormatAgent(self)
        names = agent.signature_keyword_names
        names.extend(sorted(self._kwargs))
        return systemtools.FormatSpecification(
            client=self,
            repr_is_indented=True,
            storage_format_kwargs_names=names,
            )

    ### PUBLIC METHODS ###

    def to_osc_message(self, with_textual_osc_command=False):
        from supriya.tools import synthdeftools
        if with_textual_osc_command:
            request_id = self.request_command
        else:
            request_id = int(self.request_id)
        synthdef = self.synthdef
        if isinstance(synthdef, synthdeftools.SynthDef):
            synthdef = synthdef.actual_name
        node_id = int(self.node_id)
        add_action = int(self.add_action)
        target_node_id = int(self.target_node_id)
        contents = [
            request_id,
            synthdef,
            node_id,
            add_action,
            target_node_id,
            ]
        for key, value in sorted(self._kwargs.items()):
            contents.append(key)
            contents.append(value)
        message = osctools.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def add_action(self):
        return self._add_action

    @property
    def node_id(self):
        return self._node_id

    @property
    def response_specification(self):
        from supriya.tools import responsetools
        return {
            responsetools.NodeInfoResponse: {
                'action': responsetools.NodeAction.NODE_CREATED,
                'node_id': self.node_id,
                },
            }

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.SYNTH_NEW

    @property
    def synthdef(self):
        return self._synthdef

    @property
    def target_node_id(self):
        return self._target_node_id
