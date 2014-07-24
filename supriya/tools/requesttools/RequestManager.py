# -*- encoding: utf-8 -*-
from supriya.tools import osctools


class RequestManager(object):

    ### PUBLIC METHODS ###

    @staticmethod
    def make_node_free_message(node_id):
        r'''Makes a /n_free message.

        ::

            >>> from supriya.tools import requesttools
            >>> manager = requesttools.RequestManager
            >>> message = manager.make_node_free_message(1000)
            >>> message
            OscMessage(11, 1000)

        ::

            >>> message.address == requesttools.RequestId.NODE_FREE
            True

        Returns OSC message.
        '''
        from supriya.tools import requesttools
        request_id = requesttools.RequestId.NODE_FREE
        request_id = int(request_id)
        node_id = int(node_id)
        message = osctools.OscMessage(
            request_id,
            node_id,
            )
        return message

    @staticmethod
    def make_node_set_message(node_id, **settings):
        r'''Makes a /n_set message.

        ::

            >>> from supriya.tools import requesttools
            >>> manager = requesttools.RequestManager
            >>> message = manager.make_node_set_message(
            ...     1000,
            ...     frequency=443.1,
            ...     phase=0.5,
            ...     amplitude=0.1,
            ...     )
            >>> message
            OscMessage(15, 1000, 'amplitude', 0.1, 'frequency', 443.1, 'phase', 0.5)

        ::

            >>> message.address == requesttools.RequestId.NODE_SET
            True

        Returns OSC message.
        '''
        from supriya.tools import requesttools
        request_id = requesttools.RequestId.NODE_SET
        request_id = int(request_id)
        node_id = int(node_id)
        contents = []
        for name, value in sorted(settings.items()):
            contents.append(name)
            contents.append(float(value))
        message = osctools.OscMessage(
            request_id,
            node_id,
            *contents
            )
        return message

    @staticmethod
    def make_node_map_to_control_bus_message(node_id, **settings):
        r'''Makes a /n_map message.

        ::

            >>> from supriya.tools import requesttools
            >>> from supriya.tools import servertools
            >>> manager = requesttools.RequestManager
            >>> message = manager.make_node_map_to_control_bus_message(
            ...     1000,
            ...     frequency=servertools.Bus(9, 'control'),
            ...     phase=servertools.Bus(10, 'control'),
            ...     amplitude=servertools.Bus(11, 'control'),
            ...     )
            >>> message
            OscMessage(14, 1000, 'amplitude', 11, 'frequency', 9, 'phase', 10)

        ::

            >>> message.address == \
            ...     requesttools.RequestId.NODE_MAP_TO_CONTROL_BUS
            True

        Returns OSC message.
        '''
        from supriya.tools import requesttools
        request_id = requesttools.RequestId.NODE_MAP_TO_CONTROL_BUS
        request_id = int(request_id)
        node_id = int(node_id)
        contents = []
        for name, bus in sorted(settings.items()):
            contents.append(name)
            contents.append(int(bus))
        message = osctools.OscMessage(
            request_id,
            node_id,
            *contents
            )
        return message

    @staticmethod
    def make_node_map_to_audio_bus_message(node_id, **settings):
        r'''Makes a /n_mapa message.

        ::

            >>> from supriya.tools import requesttools
            >>> from supriya.tools import servertools
            >>> manager = requesttools.RequestManager
            >>> message = manager.make_node_map_to_audio_bus_message(
            ...     1000,
            ...     frequency=servertools.Bus(9, 'audio'),
            ...     phase=servertools.Bus(10, 'audio'),
            ...     amplitude=servertools.Bus(11, 'audio'),
            ...     )
            >>> message
            OscMessage(60, 1000, 'amplitude', 11, 'frequency', 9, 'phase', 10)

        ::

            >>> message.address == \
            ...     requesttools.RequestId.NODE_MAP_TO_AUDIO_BUS
            True

        Returns OSC message.
        '''
        from supriya.tools import requesttools
        request_id = requesttools.RequestId.NODE_MAP_TO_AUDIO_BUS
        request_id = int(request_id)
        node_id = int(node_id)
        contents = []
        for name, bus in sorted(settings.items()):
            contents.append(name)
            contents.append(int(bus))
        message = osctools.OscMessage(
            request_id,
            node_id,
            *contents
            )
        return message

    @staticmethod
    def make_synth_new_message(
        add_action=None,
        node_id=None,
        synthdef_name=None,
        target_node_id=None,
        **kwargs
        ):
        r'''Makes a /s_new message.

        ::

            >>> from supriya.tools import requesttools
            >>> from supriya.tools import servertools
            >>> manager = requesttools.RequestManager
            >>> message = manager.make_synth_new_message(
            ...     add_action=servertools.AddAction['ADD_TO_TAIL'],
            ...     node_id=1001,
            ...     synthdef_name='test',
            ...     target_node_id=1000,
            ...     frequency=443,
            ...     phase=0.2,
            ...     )
            >>> message
            OscMessage(9, 'test', 1001, 1, 1000, 'frequency', 443, 'phase', 0.2)

        ::

            >>> message.address == requesttools.RequestId.SYNTH_NEW
            True

        Returns OSC message.
        '''
        from supriya.tools import requesttools
        request_id = requesttools.RequestId.SYNTH_NEW
        request_id = int(request_id)
        add_action = int(add_action)
        node_id = int(node_id)
        target_node_id = int(target_node_id)
        arguments = []
        for key, value in sorted(kwargs.items()):
            arguments.append(key)
            arguments.append(value)
        message = osctools.OscMessage(
            request_id,
            synthdef_name,
            node_id,
            add_action,
            target_node_id,
            *arguments
            )
        return message
