# -*- encoding: utf-8 -*-
from supriya.library import osclib


class ServerCommandManager(object):

    ### PUBLIC METHODS ###

    @staticmethod
    def make_dump_osc_message(osc_status):
        from supriya.library import controllib
        command_type = controllib.ServerCommandType.from_expr('dump_osc')
        osc_status = int(osc_status)
        assert 0 <= osc_status <= 4
        message = osclib.OscMessage(
            command_type,
            osc_status,
            )
        return message

    @staticmethod
    def make_notify_message(notify_status):
        from supriya.library import controllib
        command_type = controllib.ServerCommandType.from_expr('notify')
        notify_status = int(bool(notify_status))
        message = osclib.OscMessage(
            command_type,
            notify_status,
            )
        return message

    @staticmethod
    def make_status_message():
        from supriya.library import controllib
        command_type = controllib.ServerCommandType.from_expr('status')
        message = osclib.OscMessage(
            command_type,
            )
        return message

    @staticmethod
    def make_sync_message(sync_id):
        from supriya.library import controllib
        command_type = controllib.ServerCommandType.from_expr('sync')
        sync_id = int(sync_id)
        message = osclib.OscMessage(
            command_type,
            sync_id,
            )
        return message

    @staticmethod
    def make_quit_message():
        from supriya.library import controllib
        command_type = controllib.ServerCommandType.from_expr('quit')
        message = osclib.OscMessage(
            command_type,
            )
        return message
