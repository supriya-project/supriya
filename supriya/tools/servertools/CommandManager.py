# -*- encoding: utf-8 -*-
from supriya.tools import osctools


class CommandManager(object):

    ### PUBLIC METHODS ###

    @staticmethod
    def make_buffer_allocate_message(
        buffer_id,
        frame_count,
        channel_count=1,
        completion_message=None,
        ):
        from supriya.tools import servertools
        command_type = servertools.CommandNumber.from_expr('buffer_allocate')
        command_type = int(command_type)
        buffer_id = int(buffer_id)
        frame_count = int(frame_count)
        channel_count = int(channel_count)
        if completion_message is not None:
            prototype = (osctools.OscBundle, osctools.OscMessage)
            assert isinstance(completion_message, prototype)
            message = osctools.OscMessage(
                command_type,
                buffer_id,
                frame_count,
                channel_count,
                bytearray(completion_message.to_datagram())
                )
        else:
            message = osctools.OscMessage(
                command_type,
                buffer_id,
                frame_count,
                channel_count,
                )
        return message

    @staticmethod
    def make_buffer_allocate_read_message():
        raise NotImplementedError

    @staticmethod
    def make_buffer_allocate_read_channel_message():
        raise NotImplementedError

    @staticmethod
    def make_buffer_close_message(buffer_id):
        from supriya.tools import servertools
        command_type = servertools.CommandNumber.from_expr('buffer_close')
        command_type = int(command_type)
        buffer_id = int(buffer_id)
        message = osctools.OscMessage(
            command_type,
            buffer_id,
            )
        return message

    @staticmethod
    def make_buffer_fill_message():
        raise NotImplementedError

    @staticmethod
    def make_buffer_free_message(
        buffer_id,
        completion_message=None,
        ):
        from supriya.tools import servertools
        command_type = servertools.CommandNumber.from_expr('buffer_free')
        command_type = int(command_type)
        buffer_id = int(buffer_id)
        contents = [
            command_type,
            buffer_id,
            ]
        if completion_message is not None:
            prototype = (osctools.OscBundle, osctools.OscMessage)
            assert isinstance(completion_message, prototype)
            contents.append(bytearray(completion_message.to_datagram()))
        message = osctools.OscMessage(*contents)
        return message

    @staticmethod
    def make_buffer_generate_message():
        raise NotImplementedError

    @staticmethod
    def make_buffer_get_message():
        raise NotImplementedError

    @staticmethod
    def make_buffer_get_contiguous_message():
        raise NotImplementedError

    @staticmethod
    def make_buffer_query_message(*buffer_ids):
        from supriya.tools import servertools
        command_type = servertools.CommandNumber.from_expr('buffer_query')
        command_type = int(command_type)
        buffer_ids = [int(x) for x in buffer_ids]
        message = osctools.OscMessage(
            command_type,
            *buffer_ids
            )
        return message

    @staticmethod
    def make_buffer_read_message():
        raise NotImplementedError

    @staticmethod
    def make_buffer_read_contiguous_message():
        raise NotImplementedError

    @staticmethod
    def make_buffer_set_message():
        raise NotImplementedError

    @staticmethod
    def make_buffer_set_contiguous_message():
        raise NotImplementedError

    @staticmethod
    def make_buffer_write_message():
        raise NotImplementedError

    @staticmethod
    def make_buffer_zero_message(
        buffer_id,
        completion_message=None,
        ):
        from supriya.tools import servertools
        command_type = servertools.CommandNumber.from_expr('buffer_zero')
        command_type = int(command_type)
        buffer_id = int(buffer_id)
        contents = [
            command_type,
            buffer_id,
            ]
        if completion_message is not None:
            prototype = (osctools.OscBundle, osctools.OscMessage)
            assert isinstance(completion_message, prototype)
            contents.append(bytearray(completion_message.to_datagram()))
        message = osctools.OscMessage(*contents)
        return message

    @staticmethod
    def make_dump_osc_message(osc_status):
        from supriya.tools import servertools
        command_type = servertools.CommandNumber.from_expr('dump_osc')
        command_type = int(command_type)
        osc_status = int(osc_status)
        assert 0 <= osc_status <= 4
        message = osctools.OscMessage(
            command_type,
            osc_status,
            )
        return message

    @staticmethod
    def make_group_new_message(
        add_action=None,
        node_id=None,
        target_node_id=None,
        ):
        r'''Makes a /g_new message.

        ::

            >>> from supriya.tools import servertools
            >>> servertools.CommandManager.make_group_new_message(
            ...     add_action=servertools.AddAction['ADD_TO_TAIL'],
            ...     node_id=1001,
            ...     target_node_id=1000,
            ...     )
            OscMessage(21, 1001, 1, 1000)

        '''
        from supriya.tools import servertools
        command_type = servertools.CommandNumber.from_expr('group_new')
        command_type = int(command_type)
        add_action = int(add_action)
        node_id = int(node_id)
        target_node_id = int(target_node_id)
        message = osctools.OscMessage(
            command_type,
            node_id,
            add_action,
            target_node_id,
            )
        return message

    @staticmethod
    def make_group_query_tree_message(node_id, include_controls=False):
        from supriya.tools import servertools
        command_type = servertools.CommandNumber.from_expr('group_query_tree')
        command_type = int(command_type)
        node_id = int(node_id)
        include_controls = int(bool(include_controls))
        message = osctools.OscMessage(
            command_type,
            node_id,
            include_controls,
            )
        return message

    @staticmethod
    def make_node_free_message(node_id):
        from supriya.tools import servertools
        command_type = servertools.CommandNumber.from_expr('node_free')
        command_type = int(command_type)
        node_id = int(node_id)
        message = osctools.OscMessage(
            command_type,
            node_id,
            )
        return message

    @staticmethod
    def make_node_set_message(node_id, **settings):
        from supriya.tools import servertools
        command_type = servertools.CommandNumber.from_expr('node_set')
        command_type = int(command_type)
        node_id = int(node_id)
        contents = []
        for name, value in sorted(settings.items()):
            contents.append(name)
            contents.append(float(value))
        message = osctools.OscMessage(
            command_type,
            node_id,
            *contents
            )
        return message

    @staticmethod
    def make_node_map_to_control_bus_message(node_id, **settings):
        from supriya.tools import servertools
        command_type = servertools.CommandNumber.from_expr(
            'node_map_to_control_bus')
        command_type = int(command_type)
        node_id = int(node_id)
        contents = []
        for name, bus in sorted(settings.items()):
            contents.append(name)
            contents.append(float(bus))
        message = osctools.OscMessage(
            command_type,
            node_id,
            *contents
            )
        return message

    @staticmethod
    def make_node_map_to_audio_bus_message(node_id, **settings):
        from supriya.tools import servertools
        command_type = servertools.CommandNumber.from_expr(
            'node_map_to_audio_bus')
        command_type = int(command_type)
        node_id = int(node_id)
        contents = []
        for name, bus in sorted(settings.items()):
            contents.append(name)
            contents.append(float(bus))
        message = osctools.OscMessage(
            command_type,
            node_id,
            *contents
            )
        return message

    @staticmethod
    def make_notify_message(notify_status):
        from supriya.tools import servertools
        command_type = servertools.CommandNumber.from_expr('notify')
        command_type = int(command_type)
        notify_status = int(bool(notify_status))
        message = osctools.OscMessage(
            command_type,
            notify_status,
            )
        return message

    @staticmethod
    def make_release_message(node_id):
        from supriya.tools import servertools
        command_type = servertools.CommandNumber.from_expr('node_set')
        command_type = int(command_type)
        node_id = int(node_id)
        message = osctools.OscMessage(
            command_type,
            node_id,
            'gate',
            0,
            )
        return message

    @staticmethod
    def make_status_message():
        from supriya.tools import servertools
        command_type = servertools.CommandNumber.from_expr('status')
        command_type = int(command_type)
        message = osctools.OscMessage(
            command_type,
            )
        return message

    @staticmethod
    def make_sync_message(sync_id):
        from supriya.tools import servertools
        command_type = servertools.CommandNumber.from_expr('sync')
        command_type = int(command_type)
        sync_id = int(sync_id)
        message = osctools.OscMessage(
            command_type,
            sync_id,
            )
        return message

    @staticmethod
    def make_synthdef_free_message(
        synthdef=None,
        ):
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        prototype = (
            synthdeftools.SynthDef,
            str,
            )
        assert isinstance(synthdef, prototype)
        prototype = synthdeftools.SynthDef
        if isinstance(synthdef, prototype):
            synthdef = synthdef.name or synthdef.anonymous_name
        command_type = servertools.CommandNumber.from_expr('synthdef_free')
        message = osctools.OscMessage(
            command_type,
            synthdef,
            )
        return message

    @staticmethod
    def make_synthdef_receive_message(
        synthdef=None,
        ):
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        prototype = (
            synthdeftools.SynthDef,
            bytes,
            bytearray,
            )
        assert isinstance(synthdef, prototype)
        prototype = synthdeftools.SynthDef
        if isinstance(synthdef, prototype):
            synthdef = synthdef.compile()
        synthdef = bytearray(synthdef)
        command_type = servertools.CommandNumber.from_expr('synthdef_receive')
        message = osctools.OscMessage(
            command_type,
            synthdef,
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

            >>> from supriya.tools import servertools
            >>> servertools.CommandManager.make_synth_new_message(
            ...     add_action=servertools.AddAction['ADD_TO_TAIL'],
            ...     node_id=1001,
            ...     synthdef_name='test',
            ...     target_node_id=1000,
            ...     frequency=443,
            ...     phase=0.2,
            ...     )
            OscMessage(9, 'test', 1001, 1, 1000, 'frequency', 443, 'phase', 0.2)

        '''
        from supriya.tools import servertools
        command_type = servertools.CommandNumber.from_expr('synth_new')
        command_type = int(command_type)
        add_action = int(add_action)
        node_id = int(node_id)
        target_node_id = int(target_node_id)
        arguments = []
        for key, value in sorted(kwargs.items()):
            arguments.append(key)
            arguments.append(value)
        message = osctools.OscMessage(
            command_type,
            synthdef_name,
            node_id,
            add_action,
            target_node_id,
            *arguments
            )
        return message

    @staticmethod
    def make_quit_message():
        from supriya.tools import servertools
        command_type = servertools.CommandNumber.from_expr('quit')
        command_type = int(command_type)
        message = osctools.OscMessage(
            command_type,
            )
        return message
