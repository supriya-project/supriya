# -*- encoding: utf-8 -*-
from supriya.tools import osctools


class RequestManager(object):

    ### PUBLIC METHODS ###

    @staticmethod
    def make_buffer_set_message(
        buffer_id=None,
        index_value_pairs=None,
        ):
        r'''Makes a /b_set message.

        ::

            >>> from supriya.tools import requesttools
            >>> manager = requesttools.RequestManager
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

            >>> message.address == requesttools.RequestId.BUFFER_SET
            True

        Returns OSC message.
        '''
        from supriya.tools import requesttools
        request = requesttools.BufferSetRequest(
            buffer_id=buffer_id,
            index_value_pairs=index_value_pairs,
            )
        message = request.to_osc_message()
        return message

    @staticmethod
    def make_buffer_set_contiguous_message(
        buffer_id=None,
        index_values_pairs=None,
        ):
        r'''Makes a /b_setn message.

        ::

            >>> from supriya.tools import requesttools
            >>> manager = requesttools.RequestManager
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
            ...     requesttools.RequestId.BUFFER_SET_CONTIGUOUS
            True

        Returns OSC message.
        '''
        from supriya.tools import requesttools
        request = requesttools.BufferSetContiguousRequest(
            buffer_id=buffer_id,
            index_values_pairs=index_values_pairs,
            )
        message = request.to_osc_message()
        return message

    @staticmethod
    def make_buffer_write_message(
        buffer_id=None,
        completion_message=None,
        file_path=None,
        frame_count=None,
        header_format='aiff',
        leave_open=False,
        sample_format='int24',
        starting_frame=None,
        ):
        r'''Makes a /b_write message.

        ::

            >>> from supriya.tools import requesttools
            >>> from supriya.tools import soundfiletools
            >>> manager = requesttools.RequestManager
            >>> message = manager.make_buffer_write_message(
            ...     buffer_id=23,
            ...     file_path='test.aiff',
            ...     header_format=soundfiletools.HeaderFormat.AIFF,
            ...     sample_format=soundfiletools.SampleFormat.INT24,
            ...     )
            >>> message
            OscMessage(31, 23, 'test.aiff', 'aiff', 'int24', -1, 0, 0)

        ::

            >>> message.address == requesttools.RequestId.BUFFER_WRITE
            True

        Returns OSC message.
        '''
        from supriya.tools import requesttools
        request = requesttools.BufferWriteRequest(
            buffer_id=buffer_id,
            completion_message=completion_message,
            file_path=file_path,
            frame_count=frame_count,
            header_format=header_format,
            leave_open=leave_open,
            sample_format=sample_format,
            starting_frame=starting_frame,
            )
        message = request.to_osc_message()
        return message

    @staticmethod
    def make_buffer_zero_message(
        buffer_id=None,
        completion_message=None,
        ):
        r'''Makes a /b_zero message.

        ::

            >>> from supriya.tools import requesttools
            >>> manager = requesttools.RequestManager
            >>> message = manager.make_buffer_zero_message(23)
            >>> message
            OscMessage(34, 23)

        ::

            >>> message.address == requesttools.RequestId.BUFFER_ZERO
            True

        Returns OSC message.
        '''
        from supriya.tools import requesttools
        request = requesttools.BufferZeroRequest(
            buffer_id=buffer_id,
            completion_message=completion_message,
            )
        message = request.to_osc_message()
        return message

    @staticmethod
    def make_control_bus_fill_message(
        index_count_value_triples=None,
        ):
        r'''Makes a /c_fill message.

        ::

            >>> from supriya.tools import requesttools
            >>> manager = requesttools.RequestManager
            >>> message = manager.make_control_bus_fill_message(
            ...     index_count_value_triples=[
            ...         (0, 8, 0.5),
            ...         (8, 8, 0.25),
            ...         ],
            ...     )
            >>> message
            OscMessage(27, 0, 8, 0.5, 8, 8, 0.25)

        ::

            >>> message.address == \
            ...     requesttools.RequestId.CONTROL_BUS_FILL
            True

        Returns OSC message.
        '''
        from supriya.tools import requesttools
        request_id = requesttools.RequestId.CONTROL_BUS_FILL
        request_id = int(request_id)
        contents = [request_id]
        if index_count_value_triples:
            for index, count, value in index_count_value_triples:
                index = int(index)
                count = int(count)
                value = float(value)
                assert 0 <= index
                assert 0 < count
                contents.append(index)
                contents.append(count)
                contents.append(value)
        message = osctools.OscMessage(*contents)
        return message

    @staticmethod
    def make_control_bus_get_message(
        indices=None,
        ):
        r'''Makes a /c_get message.

        ::

            >>> from supriya.tools import requesttools
            >>> manager = requesttools.RequestManager
            >>> message = manager.make_control_bus_get_message(
            ...     indices=(0, 4, 8, 12),
            ...     )
            >>> message
            OscMessage(40, 0, 4, 8, 12)

        ::

            >>> message.address == \
            ...     requesttools.RequestId.CONTROL_BUS_GET
            True

        Returns OSC message.
        '''
        from supriya.tools import requesttools
        request_id = requesttools.RequestId.CONTROL_BUS_GET
        request_id = int(request_id)
        contents = [request_id]
        if indices:
            for index in indices:
                index = int(index)
                assert 0 <= index
                contents.append(index)
        message = osctools.OscMessage(*contents)
        return message

    @staticmethod
    def make_control_bus_get_contiguous_message(
        index_count_pairs=None,
        ):
        r'''Makes a /c_getn message.

        ::

            >>> from supriya.tools import requesttools
            >>> manager = requesttools.RequestManager
            >>> message = manager.make_control_bus_get_contiguous_message(
            ...     index_count_pairs=[
            ...         (0, 2),
            ...         (4, 2),
            ...         (8, 2),
            ...         (12, 2),
            ...         ],
            ...     )
            >>> message
            OscMessage(41, 0, 2, 4, 2, 8, 2, 12, 2)

        ::

            >>> message.address == \
            ...     requesttools.RequestId.CONTROL_BUS_GET_CONTIGUOUS
            True

        Returns OSC message.
        '''
        from supriya.tools import requesttools
        request_id = requesttools.RequestId.CONTROL_BUS_GET_CONTIGUOUS
        request_id = int(request_id)
        contents = [request_id]
        if index_count_pairs:
            for index, count in index_count_pairs:
                index = int(index)
                count = int(count)
                contents.append(index)
                contents.append(count)
        message = osctools.OscMessage(*contents)
        return message

    @staticmethod
    def make_control_bus_set_message(
        index_value_pairs=None,
        ):
        r'''Makes a /c_set message.

        ::

            >>> from supriya.tools import requesttools
            >>> manager = requesttools.RequestManager
            >>> message = manager.make_control_bus_set_message(
            ...     index_value_pairs=[
            ...         (0, 0.1),
            ...         (1, 0.2),
            ...         (1, 0.3),
            ...         (1, 0.4),
            ...         ],
            ...     )
            >>> message
            OscMessage(25, 0, 0.1, 1, 0.2, 1, 0.3, 1, 0.4)

        ::

            >>> message.address == \
            ...     requesttools.RequestId.CONTROL_BUS_SET
            True

        Returns OSC message.
        '''
        from supriya.tools import requesttools
        request_id = requesttools.RequestId.CONTROL_BUS_SET
        request_id = int(request_id)
        contents = [request_id]
        if index_value_pairs:
            for index, value in index_value_pairs:
                index = int(index)
                assert 0 <= index
                value = float(value)
                contents.append(index)
                contents.append(value)
        message = osctools.OscMessage(*contents)
        return message

    @staticmethod
    def make_control_bus_set_contiguous_message(
        index_values_pairs=None,
        ):
        r'''Makes a /c_setn message.

        ::

            >>> from supriya.tools import requesttools
            >>> manager = requesttools.RequestManager
            >>> message = manager.make_control_bus_set_contiguous_message(
            ...     index_values_pairs=[
            ...         (0, (0.1, 0.2, 0.3)),
            ...         (4, (0.4, 0.5, 0.6)),
            ...         ],
            ...     )
            >>> message
            OscMessage(26, 0, 3, 0.1, 0.2, 0.3, 4, 3, 0.4, 0.5, 0.6)

        ::

            >>> message.address == \
            ...     requesttools.RequestId.CONTROL_BUS_SET_CONTIGUOUS
            True

        Returns OSC message.
        '''
        from supriya.tools import requesttools
        request_id = requesttools.RequestId.CONTROL_BUS_SET_CONTIGUOUS
        request_id = int(request_id)
        contents = [request_id]
        if index_values_pairs:
            for index, values in index_values_pairs:
                index = int(index)
                assert 0 <= index
                count = len(values)
                if not count:
                    continue
                contents.append(index)
                contents.append(count)
                for value in values:
                    value = float(value)
                    contents.append(value)
        message = osctools.OscMessage(*contents)
        return message

    @staticmethod
    def make_dump_osc_message(osc_status):
        r'''Makes a /dumpOSC message.

        ::

            >>> from supriya.tools import requesttools
            >>> manager = requesttools.RequestManager
            >>> message = manager.make_dump_osc_message(1)
            >>> message
            OscMessage(39, 1)

        ::

            >>> message.address == requesttools.RequestId.DUMP_OSC
            True

        Returns OSC message.
        '''
        from supriya.tools import requesttools
        request_id = requesttools.RequestId.DUMP_OSC
        request_id = int(request_id)
        osc_status = int(osc_status)
        assert 0 <= osc_status <= 4
        message = osctools.OscMessage(
            request_id,
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

            >>> from supriya.tools import requesttools
            >>> from supriya.tools import servertools
            >>> manager = requesttools.RequestManager
            >>> message = manager.make_group_new_message(
            ...     add_action=servertools.AddAction['ADD_TO_TAIL'],
            ...     node_id=1001,
            ...     target_node_id=1000,
            ...     )
            >>> message
            OscMessage(21, 1001, 1, 1000)

        ::

            >>> message.address == requesttools.RequestId.GROUP_NEW
            True

        Returns OSC message.
        '''
        from supriya.tools import requesttools
        request_id = requesttools.RequestId.GROUP_NEW
        request_id = int(request_id)
        add_action = int(add_action)
        node_id = int(node_id)
        target_node_id = int(target_node_id)
        message = osctools.OscMessage(
            request_id,
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

            >>> from supriya.tools import requesttools
            >>> manager = requesttools.RequestManager
            >>> message = manager.make_group_query_tree_message(
            ...     node_id=0,
            ...     include_controls=True,
            ...     )
            >>> message
            OscMessage(57, 0, 1)

        ::

            >>> message.address == requesttools.RequestId.GROUP_QUERY_TREE
            True

        Returns OSC message.
        '''
        from supriya.tools import requesttools
        request_id = requesttools.RequestId.GROUP_QUERY_TREE
        request_id = int(request_id)
        node_id = int(node_id)
        include_controls = int(bool(include_controls))
        message = osctools.OscMessage(
            request_id,
            node_id,
            include_controls,
            )
        return message

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
    def make_node_release_message(node_id):
        r'''Makes a node release message.

        ..  note:: This assumes that the node has a control named *gate*.

        ::

            >>> from supriya.tools import requesttools
            >>> manager = requesttools.RequestManager
            >>> message = manager.make_node_release_message(1000)
            >>> message
            OscMessage(15, 1000, 'gate', 0)

        ::

            >>> message.address == requesttools.RequestId.NODE_SET
            True

        Returns OSC message.
        '''
        from supriya.tools import requesttools
        request_id = requesttools.RequestId.NODE_SET
        request_id = int(request_id)
        node_id = int(node_id)
        message = osctools.OscMessage(
            request_id,
            node_id,
            'gate',
            0,
            )
        return message

    @staticmethod
    def make_notify_message(notify_status):
        r'''Makes a /notify message.

        ::

            >>> from supriya.tools import requesttools
            >>> manager = requesttools.RequestManager
            >>> message = manager.make_notify_message(True)
            >>> message
            OscMessage(1, 1)

        ::

            >>> message.address == requesttools.RequestId.NOTIFY
            True

        Returns OSC message.
        '''
        from supriya.tools import requesttools
        request = requesttools.NotifyRequest(
            notify_status=notify_status,
            )
        message = request.to_osc_message()
        return message

    @staticmethod
    def make_status_message():
        r'''Makes a /status message

        ::

            >>> from supriya.tools import requesttools
            >>> manager = requesttools.RequestManager
            >>> message = manager.make_status_message()
            >>> message
            OscMessage(2)

        ::

            >>> message.address == requesttools.RequestId.STATUS
            True

        Returns OSC message.
        '''
        from supriya.tools import requesttools
        request = requesttools.StatusRequest()
        message = request.to_osc_message() 
        return message

    @staticmethod
    def make_synthdef_free_message(
        synthdef=None,
        ):
        r'''Makes a /d_free message.

        ::

            >>> from supriya.tools import requesttools
            >>> manager = requesttools.RequestManager
            >>> message = manager.make_synthdef_free_message('test')
            >>> message
            OscMessage(53, 'test')

        ::

            >>> message.address == requesttools.RequestId.SYNTHDEF_FREE
            True

        Returns OSC message.
        '''
        from supriya.tools import requesttools
        from supriya.tools import synthdeftools
        prototype = (
            synthdeftools.SynthDef,
            str,
            )
        assert isinstance(synthdef, prototype)
        prototype = synthdeftools.SynthDef
        if isinstance(synthdef, prototype):
            synthdef = synthdef.actual_name
        request_id = requesttools.RequestId.SYNTHDEF_FREE
        request_id = int(request_id)
        message = osctools.OscMessage(
            request_id,
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
        from supriya.tools import requesttools
        from supriya.tools import synthdeftools
        request_id = requesttools.RequestId.SYNTHDEF_RECEIVE
        request_id = int(request_id)
        compiled_synthdefs = synthdeftools.SynthDefCompiler.compile_synthdefs(
            synthdefs,
            )
        compiled_synthdefs = bytearray(compiled_synthdefs)
        message = osctools.OscMessage(
            request_id,
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

    @staticmethod
    def make_quit_message():
        r'''Makes a /quit message.

        ::

            >>> from supriya.tools import requesttools
            >>> manager = requesttools.RequestManager
            >>> message = manager.make_quit_message()
            >>> message
            OscMessage(3)

        ::

            >>> message.address == requesttools.RequestId.QUIT
            True

        Returns OSC message.
        '''
        from supriya.tools import requesttools
        request = requesttools.QuitRequest()
        message = request.to_osc_message()
        return message