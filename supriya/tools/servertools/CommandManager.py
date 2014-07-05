# -*- encoding: utf-8 -*-
from supriya.tools import osctools


class CommandManager(object):

    ### PUBLIC METHODS ###

    @staticmethod
    def make_buffer_allocate_message(
        buffer_id=None,
        frame_count=None,
        channel_count=1,
        completion_message=None,
        ):
        r'''Makes a /b_alloc message.

        ::

            >>> from supriya.tools import servertools
            >>> manager = servertools.CommandManager
            >>> message = manager.make_buffer_allocate_message(
            ...    buffer_id=23,
            ...    frame_count=512,
            ...    channel_count=2,
            ...    )
            >>> message
            OscMessage(28, 23, 512, 2)

        ::

            >>> message.address == servertools.CommandNumber.BUFFER_ALLOCATE
            True

        Returns OSC message.
        '''
        from supriya.tools import servertools
        command_number = servertools.CommandNumber.BUFFER_ALLOCATE
        command_number = int(command_number)
        buffer_id = int(buffer_id)
        frame_count = int(frame_count)
        channel_count = int(channel_count)
        contents = [
            command_number,
            buffer_id,
            frame_count,
            channel_count,
            ]
        if completion_message is not None:
            prototype = (osctools.OscBundle, osctools.OscMessage)
            assert isinstance(completion_message, prototype)
            completion_message = bytearray(completion_message.to_datagram())
            contents.append(completion_message)
        message = osctools.OscMessage(*contents)
        return message

    @staticmethod
    def make_buffer_allocate_read_message():
        r'''Makes a /b_allocRead message.

        Returns OSC message.
        '''
        raise NotImplementedError

    @staticmethod
    def make_buffer_allocate_read_channel_message():
        r'''Makes a /b_allocReadChannel message.

        Returns OSC message.
        '''
        raise NotImplementedError

    @staticmethod
    def make_buffer_close_message(buffer_id):
        r'''Makes a /b_close message.

        ::

            >>> from supriya.tools import servertools
            >>> manager = servertools.CommandManager
            >>> message = manager.make_buffer_close_message(
            ...     buffer_id=23,
            ...     )
            >>> message
            OscMessage(33, 23)

        ::

            >>> message.address == servertools.CommandNumber.BUFFER_CLOSE
            True

        Returns OSC message.
        '''
        from supriya.tools import servertools
        command_number = servertools.CommandNumber.BUFFER_CLOSE
        command_number = int(command_number)
        buffer_id = int(buffer_id)
        message = osctools.OscMessage(
            command_number,
            buffer_id,
            )
        return message

    @staticmethod
    def make_buffer_fill_message(
        buffer_id=None,
        index_count_value_triples=None,
        ):
        r'''Makes a /b_fill message.

        ::

            >>> from supriya.tools import servertools
            >>> manager = servertools.CommandManager
            >>> message = manager.make_buffer_fill_message(
            ...     buffer_id=23,
            ...     index_count_value_triples=(
            ...         (0, 8, 0.1),
            ...         (11, 4, 0.2),
            ...         ),
            ...     )
            >>> message
            OscMessage(37, 23, 0, 8, 0.1, 11, 4, 0.2)

        ::

            >>> message.address == servertools.CommandNumber.BUFFER_FILL
            True

        Returns OSC message.
        '''
        from supriya.tools import servertools
        command_number = servertools.CommandNumber.BUFFER_FILL
        command_number = int(command_number)
        buffer_id = int(buffer_id)
        contents = [
            command_number,
            buffer_id,
            ]
        for index, count, value in index_count_value_triples:
            contents.append(int(index))
            contents.append(int(count))
            contents.append(float(value))
        message = osctools.OscMessage(*contents)
        return message

    @staticmethod
    def make_buffer_free_message(
        buffer_id,
        completion_message=None,
        ):
        r'''Makes a /b_free message.

        ::

            >>> from supriya.tools import servertools
            >>> manager = servertools.CommandManager
            >>> message = manager.make_buffer_free_message(23)
            >>> message
            OscMessage(32, 23)

        ::

            >>> message.address == servertools.CommandNumber.BUFFER_FREE
            True

        Returns OSC message.
        '''
        from supriya.tools import servertools
        command_number = servertools.CommandNumber.BUFFER_FREE
        command_number = int(command_number)
        buffer_id = int(buffer_id)
        contents = [
            command_number,
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
        r'''Makes a /b_gen message.

        Returns OSC message.
        '''
        raise NotImplementedError

    @staticmethod
    def make_buffer_get_message(
        buffer_id=None,
        indices=None,
        ):
        r'''Makes a /b_get message.

        ::

            >>> from supriya.tools import servertools
            >>> manager = servertools.CommandManager
            >>> message = manager.make_buffer_get_message(
            ...     buffer_id=23,
            ...     indices=(0, 4, 8, 16),
            ...     )
            >>> message
            OscMessage(42, 23, 0, 4, 8, 16)

        ::

            >>> message.address == servertools.CommandNumber.BUFFER_GET
            True

        Returns OSC message.
        '''
        from supriya.tools import servertools
        command_number = servertools.CommandNumber.BUFFER_GET
        command_number = int(command_number)
        buffer_id = int(buffer_id)
        contents = [
            command_number,
            buffer_id,
            ]
        if indices:
            for index in indices:
                contents.append(int(index))
        message = osctools.OscMessage(*contents)
        return message

    @staticmethod
    def make_buffer_get_contiguous_message(
        buffer_id=None,
        index_count_pairs=None
        ):
        r'''Makes a /b_getn message.

        ::

            >>> from supriya.tools import servertools
            >>> manager = servertools.CommandManager
            >>> message = manager.make_buffer_get_contiguous_message(
            ...     buffer_id=23,
            ...     index_count_pairs=[(0, 3), (8, 11)],
            ...     )
            >>> message
            OscMessage(43, 23, 0, 3, 8, 11)

        ::

            >>> message.address == \
            ...     servertools.CommandNumber.BUFFER_GET_CONTIGUOUS
            True

        Returns OSC message.
        '''
        from supriya.tools import servertools
        command_number = servertools.CommandNumber.BUFFER_GET_CONTIGUOUS
        command_number = int(command_number)
        buffer_id = int(buffer_id)
        contents = [
            command_number,
            buffer_id,
            ]
        if index_count_pairs:
            for index, count in index_count_pairs:
                contents.append(int(index))
                contents.append(int(count))
        message = osctools.OscMessage(*contents)
        return message

    @staticmethod
    def make_buffer_query_message(
        *buffer_ids
        ):
        r'''Makes a /b_query message.

            >>> from supriya.tools import servertools
            >>> manager = servertools.CommandManager
            >>> message = manager.make_buffer_query_message(1, 23, 41)
            >>> message
            OscMessage(47, 1, 23, 41)

        ::

            >>> message.address == servertools.CommandNumber.BUFFER_QUERY
            True

        Returns OSC message.
        '''
        from supriya.tools import servertools
        command_number = servertools.CommandNumber.BUFFER_QUERY
        command_number = int(command_number)
        contents = [
            command_number,
            ]
        for buffer_id in buffer_ids:
            contents.append(int(buffer_id))
        message = osctools.OscMessage(*contents)
        return message

    @staticmethod
    def make_buffer_read_message():
        r'''Makes a /b_read message.

        Returns OSC message.
        '''
        raise NotImplementedError

    @staticmethod
    def make_buffer_read_channel_message():
        r'''Makes a /b_readChannel message.

        Returns OSC message.
        '''
        raise NotImplementedError

    @staticmethod
    def make_buffer_set_message(
        buffer_id=None,
        index_value_pairs=None,
        ):
        r'''Makes a /b_set message.

        ::

            >>> from supriya.tools import servertools
            >>> manager = servertools.CommandManager
            >>> message = manager.make_buffer_set_message(
            ...     buffer_id=23,
            ...     index_value_pairs=(
            ...         (0, 1.0),
            ...         (10, 13.2),
            ...         (17, 19.3),
            ...         ),
            ...     )
            >>> message
            OscMessage(35, 23, 0, 1.0, 10, 13.2, 17, 19.3)

        ::

            >>> message.address == servertools.CommandNumber.BUFFER_SET
            True

        Returns OSC message.
        '''
        from supriya.tools import servertools
        command_number = servertools.CommandNumber.BUFFER_SET
        command_number = int(command_number)
        buffer_id = int(buffer_id)
        contents = [
            command_number,
            buffer_id,
            ]
        if index_value_pairs:
            for index, value in index_value_pairs:
                contents.append(int(index))
                contents.append(float(value))
        message = osctools.OscMessage(*contents)
        return message

    @staticmethod
    def make_buffer_set_contiguous_message(
        buffer_id=None,
        index_values_pairs=None,
        ):
        r'''Makes a /b_setn message.

        ::

            >>> from supriya.tools import servertools
            >>> manager = servertools.CommandManager
            >>> message = manager.make_buffer_set_contiguous_message(
            ...     buffer_id=23,
            ...     index_values_pairs=(
            ...         (0, (1, 2, 3)),
            ...         (10, (17.1, 18.2))
            ...         ),
            ...     )
            >>> message
            OscMessage(36, 23, 0, 3, 1.0, 2.0, 3.0, 10, 2, 17.1, 18.2)

        ::

            >>> message.address == \
            ...     servertools.CommandNumber.BUFFER_SET_CONTIGUOUS
            True

        Returns OSC message.
        '''
        from supriya.tools import servertools
        command_number = servertools.CommandNumber.BUFFER_SET_CONTIGUOUS
        command_number = int(command_number)
        buffer_id = int(buffer_id)
        contents = [
            command_number,
            buffer_id,
            ]
        if index_values_pairs:
            for index, values in index_values_pairs:
                if not values:
                    continue
                contents.append(int(index))
                contents.append(len(values))
                for value in values:
                    contents.append(float(value))
        message = osctools.OscMessage(*contents)
        return message

    @staticmethod
    def make_buffer_write_message(
        buffer_id=None,
        file_path=None,
        header_format='aiff',
        sample_format='int24',
        frame_count=None,
        starting_frame=None,
        leave_open=False,
        completion_message=None,
        ):
        r'''Makes a /b_write message.

        ::

            >>> from supriya.tools import servertools
            >>> from supriya.tools import soundfiletools
            >>> manager = servertools.CommandManager
            >>> message = manager.make_buffer_write_message(
            ...     buffer_id=23,
            ...     file_path='test.aiff',
            ...     header_format=soundfiletools.HeaderFormat.AIFF,
            ...     sample_format=soundfiletools.SampleFormat.INT24,
            ...     )
            >>> message
            OscMessage(31, 23, 'test.aiff', 'aiff', 'int24', -1, 0)

        ::

            >>> message.address == servertools.CommandNumber.BUFFER_WRITE
            True

        Returns OSC message.
        '''
        from supriya.tools import servertools
        from supriya.tools import soundfiletools
        command_number = servertools.CommandNumber.BUFFER_WRITE
        command_number = int(command_number)
        buffer_id = int(buffer_id)
        file_path = str(file_path)
        header_format = soundfiletools.HeaderFormat.from_expr(header_format)
        header_format = header_format.name.lower()
        sample_format = soundfiletools.SampleFormat.from_expr(sample_format)
        sample_format = sample_format.name.lower()
        if frame_count is None:
            frame_count = -1
        frame_count = int(frame_count)
        assert -1 <= frame_count
        if starting_frame is None:
            starting_frame = 0
        starting_frame = int(starting_frame)
        assert 0 <= starting_frame
        leave_open = int(bool(leave_open))
        contents = [
            command_number,
            buffer_id,
            file_path,
            header_format,
            sample_format,
            frame_count,
            leave_open,
            ]
        if completion_message is not None:
            prototype = (osctools.OscBundle, osctools.OscMessage)
            assert isinstance(completion_message, prototype)
            contents.append(bytearray(completion_message.to_datagram()))
        message = osctools.OscMessage(*contents)
        return message

    @staticmethod
    def make_buffer_zero_message(
        buffer_id=None,
        completion_message=None,
        ):
        r'''Makes a /b_zero message.

        ::

            >>> from supriya.tools import servertools
            >>> manager = servertools.CommandManager
            >>> message = manager.make_buffer_zero_message(23)
            >>> message
            OscMessage(34, 23)

        ::

            >>> message.address == servertools.CommandNumber.BUFFER_ZERO
            True

        Returns OSC message.
        '''
        from supriya.tools import servertools
        command_number = servertools.CommandNumber.BUFFER_ZERO
        command_number = int(command_number)
        buffer_id = int(buffer_id)
        contents = [
            command_number,
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
        r'''Makes a /dumpOSC message.

        ::

            >>> from supriya.tools import servertools
            >>> manager = servertools.CommandManager
            >>> message = manager.make_dump_osc_message(1)
            >>> message
            OscMessage(39, 1)

        ::

            >>> message.address == servertools.CommandNumber.DUMP_OSC
            True

        Returns OSC message.
        '''
        from supriya.tools import servertools
        command_number = servertools.CommandNumber.DUMP_OSC
        command_number = int(command_number)
        osc_status = int(osc_status)
        assert 0 <= osc_status <= 4
        message = osctools.OscMessage(
            command_number,
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
            >>> manager = servertools.CommandManager
            >>> message = manager.make_group_new_message(
            ...     add_action=servertools.AddAction['ADD_TO_TAIL'],
            ...     node_id=1001,
            ...     target_node_id=1000,
            ...     )
            >>> message
            OscMessage(21, 1001, 1, 1000)

        ::

            >>> message.address == servertools.CommandNumber.GROUP_NEW
            True

        Returns OSC message.
        '''
        from supriya.tools import servertools
        command_number = servertools.CommandNumber.GROUP_NEW
        command_number = int(command_number)
        add_action = int(add_action)
        node_id = int(node_id)
        target_node_id = int(target_node_id)
        message = osctools.OscMessage(
            command_number,
            node_id,
            add_action,
            target_node_id,
            )
        return message

    @staticmethod
    def make_group_query_tree_message(
        node_id=None,
        include_controls=False,
        ):
        r'''Makes a /g_queryTree message.

        ::

            >>> from supriya.tools import servertools
            >>> manager = servertools.CommandManager
            >>> message = manager.make_group_query_tree_message(
            ...     node_id=0,
            ...     include_controls=True,
            ...     )
            >>> message
            OscMessage(57, 0, 1)

        ::

            >>> message.address == servertools.CommandNumber.GROUP_QUERY_TREE
            True

        Returns OSC message.
        '''
        from supriya.tools import servertools
        command_number = servertools.CommandNumber.GROUP_QUERY_TREE
        command_number = int(command_number)
        node_id = int(node_id)
        include_controls = int(bool(include_controls))
        message = osctools.OscMessage(
            command_number,
            node_id,
            include_controls,
            )
        return message

    @staticmethod
    def make_node_free_message(node_id):
        r'''Makes a /n_free message.

        ::

            >>> from supriya.tools import servertools
            >>> manager = servertools.CommandManager
            >>> message = manager.make_node_free_message(1000)
            >>> message
            OscMessage(11, 1000)

        ::

            >>> message.address == servertools.CommandNumber.NODE_FREE
            True

        Returns OSC message.
        '''
        from supriya.tools import servertools
        command_number = servertools.CommandNumber.NODE_FREE
        command_number = int(command_number)
        node_id = int(node_id)
        message = osctools.OscMessage(
            command_number,
            node_id,
            )
        return message

    @staticmethod
    def make_node_set_message(node_id, **settings):
        r'''Makes a /n_set message.

        ::

            >>> from supriya.tools import servertools
            >>> manager = servertools.CommandManager
            >>> message = manager.make_node_set_message(
            ...     1000,
            ...     frequency=443.1,
            ...     phase=0.5,
            ...     amplitude=0.1,
            ...     )
            >>> message
            OscMessage(15, 1000, 'amplitude', 0.1, 'frequency', 443.1, 'phase', 0.5)

        ::

            >>> message.address == servertools.CommandNumber.NODE_SET
            True

        Returns OSC message.
        '''
        from supriya.tools import servertools
        command_number = servertools.CommandNumber.NODE_SET
        command_number = int(command_number)
        node_id = int(node_id)
        contents = []
        for name, value in sorted(settings.items()):
            contents.append(name)
            contents.append(float(value))
        message = osctools.OscMessage(
            command_number,
            node_id,
            *contents
            )
        return message

    @staticmethod
    def make_node_map_to_control_bus_message(node_id, **settings):
        r'''Makes a /n_map message.

        ::

            >>> from supriya.tools import servertools
            >>> manager = servertools.CommandManager
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
            ...     servertools.CommandNumber.NODE_MAP_TO_CONTROL_BUS
            True

        Returns OSC message.
        '''
        from supriya.tools import servertools
        command_number = servertools.CommandNumber.NODE_MAP_TO_CONTROL_BUS
        command_number = int(command_number)
        node_id = int(node_id)
        contents = []
        for name, bus in sorted(settings.items()):
            contents.append(name)
            contents.append(int(bus))
        message = osctools.OscMessage(
            command_number,
            node_id,
            *contents
            )
        return message

    @staticmethod
    def make_node_map_to_audio_bus_message(node_id, **settings):
        r'''Makes a /n_mapa message.

        ::

            >>> from supriya.tools import servertools
            >>> manager = servertools.CommandManager
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
            ...     servertools.CommandNumber.NODE_MAP_TO_AUDIO_BUS
            True

        Returns OSC message.
        '''
        from supriya.tools import servertools
        command_number = servertools.CommandNumber.NODE_MAP_TO_AUDIO_BUS
        command_number = int(command_number)
        node_id = int(node_id)
        contents = []
        for name, bus in sorted(settings.items()):
            contents.append(name)
            contents.append(int(bus))
        message = osctools.OscMessage(
            command_number,
            node_id,
            *contents
            )
        return message

    @staticmethod
    def make_node_release_message(node_id):
        r'''Makes a node release message.

        ..  note:: This assumes that the node has a control named *gate*.

        ::

            >>> from supriya.tools import servertools
            >>> manager = servertools.CommandManager
            >>> message = manager.make_node_release_message(1000)
            >>> message
            OscMessage(15, 1000, 'gate', 0)

        ::

            >>> message.address == servertools.CommandNumber.NODE_SET
            True

        Returns OSC message.
        '''
        from supriya.tools import servertools
        command_number = servertools.CommandNumber.NODE_SET
        command_number = int(command_number)
        node_id = int(node_id)
        message = osctools.OscMessage(
            command_number,
            node_id,
            'gate',
            0,
            )
        return message

    @staticmethod
    def make_notify_message(notify_status):
        r'''Makes a /notify message.

        ::

            >>> from supriya.tools import servertools
            >>> manager = servertools.CommandManager
            >>> message = manager.make_notify_message(True)
            >>> message
            OscMessage(1, 1)

        ::

            >>> message.address == servertools.CommandNumber.NOTIFY
            True

        Returns OSC message.
        '''
        from supriya.tools import servertools
        command_number = servertools.CommandNumber.NOTIFY
        command_number = int(command_number)
        notify_status = int(bool(notify_status))
        message = osctools.OscMessage(
            command_number,
            notify_status,
            )
        return message

    @staticmethod
    def make_status_message():
        r'''Makes a /status message

        ::

            >>> from supriya.tools import servertools
            >>> manager = servertools.CommandManager
            >>> message = manager.make_status_message()
            >>> message
            OscMessage(2)

        ::

            >>> message.address == servertools.CommandNumber.STATUS
            True

        Returns OSC message.
        '''
        from supriya.tools import servertools
        command_number = servertools.CommandNumber.STATUS
        command_number = int(command_number)
        message = osctools.OscMessage(
            command_number,
            )
        return message

    @staticmethod
    def make_sync_message(sync_id):
        r'''Makes a /sync message.

        ::

            >>> from supriya.tools import servertools
            >>> manager = servertools.CommandManager
            >>> message = manager.make_sync_message(1999)
            >>> message
            OscMessage(52, 1999)

        ::

            >>> message.address == servertools.CommandNumber.SYNC
            True

        Returns OSC message.
        '''
        from supriya.tools import servertools
        command_number = servertools.CommandNumber.SYNC
        command_number = int(command_number)
        sync_id = int(sync_id)
        message = osctools.OscMessage(
            command_number,
            sync_id,
            )
        return message

    @staticmethod
    def make_synthdef_free_message(
        synthdef=None,
        ):
        r'''Makes a /d_free message.

        ::

            >>> from supriya.tools import servertools
            >>> manager = servertools.CommandManager
            >>> message = manager.make_synthdef_free_message('test')
            >>> message
            OscMessage(53, 'test')

        ::

            >>> message.address == servertools.CommandNumber.SYNTHDEF_FREE
            True

        Returns OSC message.
        '''
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        prototype = (
            synthdeftools.SynthDef,
            str,
            )
        assert isinstance(synthdef, prototype)
        prototype = synthdeftools.SynthDef
        if isinstance(synthdef, prototype):
            synthdef = synthdef.actual_name
        command_number = servertools.CommandNumber.SYNTHDEF_FREE
        command_number = int(command_number)
        message = osctools.OscMessage(
            command_number,
            synthdef,
            )
        return message

    @staticmethod
    def make_synthdef_receive_message(
        *synthdefs
        ):
        r'''Makes a /d_recv message.

        Returns OSC message.
        '''
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        command_number = servertools.CommandNumber.SYNTHDEF_RECEIVE
        command_number = int(command_number)
        compiled_synthdefs = synthdeftools.SynthDefCompiler.compile_synthdefs(
            synthdefs,
            )
        compiled_synthdefs = bytearray(compiled_synthdefs)
        message = osctools.OscMessage(
            command_number,
            compiled_synthdefs,
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
            >>> manager = servertools.CommandManager
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

            >>> message.address == servertools.CommandNumber.SYNTH_NEW
            True

        Returns OSC message.
        '''
        from supriya.tools import servertools
        command_number = servertools.CommandNumber.SYNTH_NEW
        command_number = int(command_number)
        add_action = int(add_action)
        node_id = int(node_id)
        target_node_id = int(target_node_id)
        arguments = []
        for key, value in sorted(kwargs.items()):
            arguments.append(key)
            arguments.append(value)
        message = osctools.OscMessage(
            command_number,
            synthdef_name,
            node_id,
            add_action,
            target_node_id,
            *arguments
            )
        return message

    @staticmethod
    def make_quit_message():
        r'''Makes a /quit message.

        ::

            >>> from supriya.tools import servertools
            >>> manager = servertools.CommandManager
            >>> message = manager.make_quit_message()
            >>> message
            OscMessage(3)

        ::

            >>> message.address == servertools.CommandNumber.QUIT
            True

        Returns OSC message.
        '''
        from supriya.tools import servertools
        command_number = servertools.CommandNumber.QUIT
        command_number = int(command_number)
        message = osctools.OscMessage(
            command_number,
            )
        return message
